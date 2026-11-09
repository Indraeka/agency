#!/usr/bin/env python3
"""Download Lotto Max and Lotto 6/49 draw history into data/*.csv.

Sources (both public results archives; OLG itself publishes no bulk export):
  * lotteryextreme.com  - month-by-month archive, both games (primary)
  * lottomaxnumbers.com - year-by-year archive, Lotto Max only (cross-check)

Every Lotto Max draw is compared across the two sources; any disagreement is
printed and the run fails, so a scraping bug cannot silently poison the data.

Usage:  python3 fetch.py [--years 3]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

DATA = Path(__file__).parent / "data"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

GAMES = {
    # name: (lotteryextreme slug, main balls per draw, draw weekdays Mon=0)
    "lottomax": ("lottomax", 7, {1, 4}),
    "lotto649": ("lotto649", 6, {2, 5}),
}


def http(url: str, data: dict | None = None, tries: int = 4) -> str:
    body = urllib.parse.urlencode(data).encode() if data else None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=body, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - retry any transport error
            if attempt == tries - 1:
                raise
            print(f"  retry {url}: {exc}", file=sys.stderr)
            time.sleep(2 ** (attempt + 1))
    raise AssertionError("unreachable")


def months_back(start: dt.date, end: dt.date):
    y, m = end.year, end.month
    while (y, m) >= (start.year, start.month):
        yield f"{y:04d}-{m:02d}"
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)


ROW = re.compile(
    r"\((\d{4}-\d{2}-\d{2}) \w{3}\).*?<ul class='displayball'[^>]*>(.*?)</ul>", re.S
)


def fetch_lotteryextreme(game: str, start: dt.date, end: dt.date) -> dict:
    slug, n_main, _ = GAMES[game]
    url = f"https://www.lotteryextreme.com/canada/{slug}-results"
    draws = {}
    for ym in months_back(start, end):
        html = http(url, {"mode": "month", "year_month": ym})
        found = 0
        for date, balls in ROW.findall(html):
            if not date.startswith(ym):
                continue
            main_part, _, bonus_part = balls.partition('class="dbx"')
            main = [int(x) for x in re.findall(r"<li>(\d+)", main_part)]
            bonus = [int(x) for x in re.findall(r"<li>(\d+)", bonus_part)]
            if len(main) != n_main or len(bonus) != 1:
                raise ValueError(f"{game} {date}: unexpected balls {main} + {bonus}")
            draws[date] = (sorted(main), bonus[0])
            found += 1
        print(f"  {game} {ym}: {found} draws")
        time.sleep(0.4)
    return draws


def fetch_lottomaxnumbers(start: dt.date, end: dt.date) -> dict:
    draws = {}
    for year in range(start.year, end.year + 1):
        html = http(f"https://www.lottomaxnumbers.com/numbers/{year}")
        for mm, dd, yy, balls in re.findall(
            r"lotto-max-result-(\d\d)-(\d\d)-(\d{4})\".*?<ul class=\"balls\">(.*?)</ul>",
            html,
            re.S,
        ):
            main = [int(x) for x in re.findall(r'class="ball ball">(\d+)', balls)]
            bonus = [int(x) for x in re.findall(r'class="ball bonus-ball">(\d+)', balls)]
            if len(main) == 7 and len(bonus) == 1:
                draws[f"{yy}-{mm}-{dd}"] = (sorted(main), bonus[0])
        time.sleep(0.4)
    return draws


def validate(game: str, draws: dict, start: dt.date, end: dt.date) -> list[str]:
    """Return a list of problems (empty = clean)."""
    _, _, weekdays = GAMES[game]
    problems = []
    for date, (main, bonus) in draws.items():
        if len(set(main)) != len(main) or bonus in main:
            problems.append(f"{date}: duplicate ball")
        if dt.date.fromisoformat(date).weekday() not in weekdays:
            problems.append(f"{date}: not a scheduled draw day")
    day = start
    while day <= end:
        if day.weekday() in weekdays and day.isoformat() not in draws:
            problems.append(f"{day}: scheduled draw missing")
        day += dt.timedelta(days=1)
    return problems


def write_csv(game: str, draws: dict) -> Path:
    DATA.mkdir(exist_ok=True)
    n_main = GAMES[game][1]
    path = DATA / f"{game}.csv"
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date"] + [f"n{i}" for i in range(1, n_main + 1)] + ["bonus"])
        for date in sorted(draws):
            main, bonus = draws[date]
            w.writerow([date] + main + [bonus])
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, default=3)
    args = ap.parse_args()
    end = dt.date.today()
    start = end.replace(year=end.year - args.years)
    ok = True

    for game in GAMES:
        print(f"Fetching {game} {start} .. {end}")
        draws = {
            d: v
            for d, v in fetch_lotteryextreme(game, start, end).items()
            if start.isoformat() <= d <= end.isoformat()
        }
        problems = validate(game, draws, start, end)

        if game == "lottomax":
            other = fetch_lottomaxnumbers(start, end)
            both = [d for d in draws if d in other]
            diffs = [d for d in both if draws[d] != other[d]]
            only_other = [d for d in other if start.isoformat() <= d <= end.isoformat() and d not in draws]
            print(f"  cross-check: {len(both)} draws compared, {len(diffs)} mismatches, "
                  f"{len(draws) - len(both)} unverified, {len(only_other)} only in 2nd source")
            problems += [f"{d}: sources disagree {draws[d]} vs {other[d]}" for d in diffs]
            problems += [f"{d}: only in lottomaxnumbers" for d in only_other]

        path = write_csv(game, draws)
        print(f"  wrote {len(draws)} draws -> {path}")
        for p in problems:
            print(f"  PROBLEM {p}")
        ok &= not problems
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
