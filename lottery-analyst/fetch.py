#!/usr/bin/env python3
"""Download Lotto Max, Lotto 6/49 and Daily Grand draw history into data/*.csv.

Sources (both public results archives; OLG itself publishes no bulk export):
  * lotteryextreme.com  - month-by-month archive, all games (primary)
  * lottomaxnumbers.com - year-by-year archive, Lotto Max only (cross-check)

Every Lotto Max draw is compared across the two sources; any disagreement is
printed and the run fails, so a scraping bug cannot silently poison the data.

Usage:  python3 fetch.py            add draws published since the last run
        python3 fetch.py --full     re-download the whole history
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import shutil
import ssl
import subprocess
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
    "dailygrand": ("dailygrand", 5, {0, 3}),
}
# Archive page name where it is not "<slug>-results".
ARCHIVE_PAGE = {"dailygrand": "dailygrand-winningnumbers"}
# Games whose extra number comes from its own pool, so it may repeat a main number
# (Daily Grand's Grand Number, 1-7). Stored in the "bonus" column like the others.
SEPARATE_EXTRA = {"dailygrand"}


def _ssl_context() -> ssl.SSLContext:
    """Certificate store for HTTPS. Python on macOS often ships without one,
    so prefer the `certifi` bundle when it is installed."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def _is_cert_error(exc: Exception) -> bool:
    return isinstance(exc, ssl.SSLCertVerificationError) or isinstance(
        getattr(exc, "reason", None), ssl.SSLCertVerificationError)


def _http_curl(url: str, data: dict | None) -> str:
    """Download with the system `curl`, which uses the operating system's own
    certificate store. Verification stays on."""
    cmd = ["curl", "-sS", "--fail", "--location", "--max-time", "40", "-A", UA]
    if data:
        cmd += ["--data", urllib.parse.urlencode(data)]
    out = subprocess.run(cmd + [url], capture_output=True, timeout=60)
    if out.returncode:
        raise OSError(f"curl failed for {url}: {out.stderr.decode('utf-8', 'replace').strip()}")
    return out.stdout.decode("utf-8", "replace")


def http(url: str, data: dict | None = None, tries: int = 4) -> str:
    body = urllib.parse.urlencode(data).encode() if data else None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=body, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40, context=_ssl_context()) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - retry any transport error
            if _is_cert_error(exc):
                # Python has no usable certificate store here (common on macOS).
                if shutil.which("curl"):
                    return _http_curl(url, data)
                raise OSError(
                    "Python cannot verify secure connections on this computer. "
                    "Fix: run  python3 -m pip install certifi  and start the app again."
                ) from exc
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
    url = f"https://www.lotteryextreme.com/canada/{ARCHIVE_PAGE.get(game, slug + '-results')}"
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
    """Return a list of problems (empty = clean).

    A scheduled draw from the last two days that is not listed yet is treated
    as "not published yet", not as a problem.
    """
    _, _, weekdays = GAMES[game]
    problems = []
    for date, (main, bonus) in draws.items():
        if len(set(main)) != len(main) or (bonus in main and game not in SEPARATE_EXTRA):
            problems.append(f"{date}: duplicate ball")
        if dt.date.fromisoformat(date).weekday() not in weekdays:
            problems.append(f"{date}: not a scheduled draw day")
    day = start
    while day <= end - dt.timedelta(days=2):
        if day.weekday() in weekdays and day.isoformat() not in draws:
            problems.append(f"{day}: scheduled draw missing")
        day += dt.timedelta(days=1)
    return problems


def read_csv(game: str) -> dict:
    path = DATA / f"{game}.csv"
    if not path.exists():
        return {}
    n_main = GAMES[game][1]
    with path.open() as fh:
        return {
            r["date"]: ([int(r[f"n{i}"]) for i in range(1, n_main + 1)], int(r["bonus"]))
            for r in csv.DictReader(fh)
        }


def refresh(years: int = 3, log=print) -> dict:
    """Add draws published since the last one on file. Returns a summary per game.

    Only the months from the last stored draw to today are downloaded. New
    Lotto Max draws are cross-checked against the second source. If anything
    looks wrong the CSV for that game is left untouched.
    """
    end = dt.date.today()
    summary = {}
    for game in GAMES:
        have = read_csv(game)
        if have:
            start, since = dt.date.fromisoformat(min(have)), dt.date.fromisoformat(max(have))
        else:
            start = since = end.replace(year=end.year - years)
        log(f"{game}: checking {since} .. {end}")
        got = fetch_lotteryextreme(game, since, end)
        new = {d: v for d, v in got.items() if d not in have and d <= end.isoformat()}
        problems = [f"{d}: differs from stored result" for d in got if d in have and got[d] != have[d]]
        merged = {**have, **new}
        problems += validate(game, merged, start, end)
        if game == "lottomax" and new:
            other = fetch_lottomaxnumbers(dt.date.fromisoformat(min(new)), end)
            problems += [f"{d}: sources disagree" for d in new if d in other and other[d] != new[d]]
            unverified = [d for d in new if d not in other]
        else:
            unverified = []
        if new and not problems:
            write_csv(game, merged)
        summary[game] = {
            "added": [{"date": d, "main": new[d][0], "bonus": new[d][1]} for d in sorted(new)],
            "saved": bool(new) and not problems,
            "total": len(merged) if not problems else len(have),
            "problems": problems,
            "unverified": unverified,
        }
    return summary


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


def full_download(years: int) -> bool:
    end = dt.date.today()
    start = end.replace(year=end.year - years)
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
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, default=3)
    ap.add_argument("--full", action="store_true", help="re-download everything instead of only new draws")
    args = ap.parse_args()
    if args.full:
        return 0 if full_download(args.years) else 1
    ok = True
    for game, s in refresh(args.years).items():
        print(f"{game}: +{len(s['added'])} new draws, {s['total']} on file")
        for d in s["added"]:
            print(f"  {d['date']}  {d['main']} + {d['bonus']}")
        for p in s["problems"]:
            print(f"  PROBLEM {p}")
        ok &= not s["problems"]
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
