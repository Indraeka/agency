#!/usr/bin/env python3
"""Lotto Max / Lotto 6/49 analyst.

Three stages, run in order for each game:

  1. OBSERVE  - frequency, gaps, pairs, sums, odd/even, repeats. Every pattern
                statistic is compared with a Monte Carlo null (fair draws from
                the same pool schedule) so "pattern" and "noise" can be told apart.
  2. LEARN    - walk-forward backtest: each strategy only sees draws before the
                one it is scored on. Mean matches/ticket vs the hypergeometric
                expectation says whether any strategy has an edge.
  3. PICK     - two tickets per game:
                  A "pattern"    - highest ensemble score with a typical shape
                  B "anti-crowd" - numbers other players under-pick, so a win
                                   is shared with fewer people

Usage:  python3 analyze.py [--sims 4000] [--seed-extra TEXT]
Writes report.md and picks.json next to this file.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

GAMES = {
    "lottomax": {
        "label": "Lotto Max",
        "k": 7,
        "weekdays": {1, 4},  # Tue, Fri
        # Pool grew from 50 to 52 numbers on this draw: it is the first draw
        # with a 51/52 in the data and the first one lottomaxnumbers.com lists
        # under the new "MaxPlus" format.
        "pools": [("0000-00-00", 50), ("2026-04-14", 52)],
    },
    "lotto649": {
        "label": "Lotto 6/49",
        "k": 6,
        "weekdays": {2, 5},  # Wed, Sat
        "pools": [("0000-00-00", 49)],
    },
}


# --------------------------------------------------------------------------- data
def load(game: str):
    rows = list(csv.DictReader((HERE / "data" / f"{game}.csv").open()))
    k = GAMES[game]["k"]
    dates = [r["date"] for r in rows]
    main = np.array([[int(r[f"n{i}"]) for i in range(1, k + 1)] for r in rows])
    bonus = np.array([int(r["bonus"]) for r in rows])
    pools = np.array([pool_on(game, d) for d in dates])
    return dates, main, bonus, pools


def pool_on(game: str, date: str) -> int:
    size = None
    for start, n in GAMES[game]["pools"]:
        if date >= start:
            size = n
    return size


def onehot(main: np.ndarray, width: int) -> np.ndarray:
    m = np.zeros((len(main), width + 1), dtype=np.int16)
    np.put_along_axis(m, main, 1, axis=1)
    return m[:, 1:]


def simulate(pools: np.ndarray, k: int, sims: int, rng) -> np.ndarray:
    """sims x draws x k array of fair draws following the real pool schedule."""
    width = pools.max()
    keys = rng.random((sims, len(pools), width))
    keys[:, np.arange(width)[None, :] >= pools[:, None]] = 2.0  # exclude balls not in pool
    return np.sort(np.argpartition(keys, k, axis=2)[:, :, :k] + 1, axis=2)


# ------------------------------------------------------------------------ observe
def stats_of(main: np.ndarray, pools: np.ndarray) -> dict:
    """Pattern statistics for one history (real or simulated)."""
    k = main.shape[1]
    width = pools.max()
    hot = onehot(main, width)
    counts = hot.sum(0)
    exp = (k / pools)[:, None] * (np.arange(1, width + 1)[None, :] <= pools[:, None])
    e = exp.sum(0)
    var = (exp * (1 - exp)).sum(0)
    z = (counts - e) / np.sqrt(var)
    pair = hot.T.astype(np.int32) @ hot
    np.fill_diagonal(pair, 0)
    gaps = np.diff(main, axis=1)
    return {
        "chi2": float(((counts - e) ** 2 / e).sum()),
        "max_abs_z": float(np.abs(z).max()),
        "repeat_prev": float((hot[1:] * hot[:-1]).sum(1).mean()),
        "max_pair": float(pair.max()),
        "mean_sum": float(main.sum(1).mean()),
        "sd_sum": float(main.sum(1).std()),
        "mean_odd": float((main % 2).sum(1).mean()),
        "consecutive_rate": float((gaps == 1).any(1).mean()),
        "_counts": counts,
        "_z": z,
        "_pair": pair,
    }


TESTS = [
    ("chi2", "Frequency chi-square (are some numbers favoured?)"),
    ("max_abs_z", "Most extreme hot/cold number, |z|"),
    ("repeat_prev", "Numbers repeated from previous draw (avg)"),
    ("max_pair", "Most frequent pair, times drawn together"),
    ("mean_sum", "Average sum of main numbers"),
    ("sd_sum", "Spread (SD) of sums"),
    ("mean_odd", "Average count of odd numbers"),
    ("consecutive_rate", "Share of draws with a consecutive pair"),
]


def observe(main, pools, sims, rng) -> dict:
    real = stats_of(main, pools)
    null = {key: [] for key, _ in TESTS}
    for sim in simulate(pools, main.shape[1], sims, rng):
        s = stats_of(sim, pools)
        for key in null:
            null[key].append(s[key])
    out = []
    for key, label in TESTS:
        dist = np.array(null[key])
        lo = (dist <= real[key]).mean()
        hi = (dist >= real[key]).mean()
        out.append(
            {
                "key": key,
                "label": label,
                "observed": real[key],
                "null_mean": float(dist.mean()),
                "null_lo": float(np.quantile(dist, 0.025)),
                "null_hi": float(np.quantile(dist, 0.975)),
                "p": float(min(1.0, 2 * min(lo, hi))),
            }
        )
    return {"real": real, "tests": out}


def last_seen_gap(main: np.ndarray, width: int) -> np.ndarray:
    """Draws since each number last appeared (len(main) if never)."""
    gap = np.full(width, len(main))
    for age, row in enumerate(main[::-1]):
        for n in row:
            if gap[n - 1] == len(main):
                gap[n - 1] = age
    return gap


# -------------------------------------------------------------------------- learn
def scores(main: np.ndarray, pools: np.ndarray, pool_now: int) -> dict:
    """Per-number scores from history only. Higher = strategy prefers it."""
    k = main.shape[1]
    width = pools.max()
    hot = onehot(main, width).astype(float)
    exp = (k / pools)[:, None] * (np.arange(1, width + 1)[None, :] <= pools[:, None])

    def z(sl):
        e = exp[sl].sum(0)
        v = (exp[sl] * (1 - exp[sl])).sum(0)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = (hot[sl].sum(0) - e) / np.sqrt(v)
        return np.nan_to_num(out)

    long_z = z(slice(None))
    recent_z = z(slice(-40, None))
    gap = last_seen_gap(main, width).astype(float)
    overdue = (gap - gap[:pool_now].mean()) / (gap[:pool_now].std() or 1)
    s = {
        "hot": recent_z,
        "cold": -long_z,
        "overdue": overdue,
        "ensemble": 0.5 * long_z + 0.3 * recent_z + 0.2 * overdue,
    }
    for v in s.values():
        v[pool_now:] = -np.inf  # numbers not in play
    return s


def backtest(main, pools, warmup=100) -> list[dict]:
    k = main.shape[1]
    hits = {name: [] for name in ("hot", "cold", "overdue", "ensemble")}
    exp, var = [], []
    for t in range(warmup, len(main)):
        n = pools[t]
        sc = scores(main[:t], pools[:t], n)
        drawn = set(main[t].tolist())
        for name, v in sc.items():
            pick = np.argsort(-v, kind="stable")[:k] + 1
            hits[name].append(len(drawn.intersection(pick.tolist())))
        exp.append(k * k / n)
        var.append(k * (k / n) * (1 - k / n) * (n - k) / (n - 1))
    e, se = float(np.mean(exp)), float(np.sqrt(np.sum(var)) / len(exp))
    return [
        {
            "strategy": name,
            "draws": len(h),
            "mean_matches": float(np.mean(h)),
            "expected_random": e,
            "z": (float(np.mean(h)) - e) / se,
            "best_single_ticket": int(max(h)),
        }
        for name, h in hits.items()
    ]


# --------------------------------------------------------------------------- pick
def shape_ok(ticket, main_hist, pool) -> bool:
    """Reject shapes that are rare in real draws (keeps the middle ~80%)."""
    t = np.array(ticket)
    k = len(t)
    scale = (pool + 1) / 2 * k  # rescale history sums to the current pool
    sums = main_hist.sum(1)
    lo, hi = np.quantile(sums, [0.10, 0.90])
    lo, hi = lo / sums.mean() * scale, hi / sums.mean() * scale
    odd = int((t % 2).sum())
    runs = np.diff(t) == 1
    longest_run = max((len(list(g)) for v, g in itertools.groupby(runs) if v), default=0)
    return (
        lo <= t.sum() <= hi
        and 2 <= odd <= k - 2
        and longest_run <= 1
        and len({(n - 1) // 10 for n in ticket}) >= 4
    )


def popularity(n: int) -> float:
    """Rough relative popularity of a number among human-picked tickets.

    Based on the well-documented player biases (birthdays -> 1..31, months ->
    1..12, 'lucky' 7/3/11/13, and neglect of high numbers). Not OLG data: the
    lottery corporations do not publish pick distributions.
    """
    p = 1.0
    if n <= 31:
        p += 0.35
    if n <= 12:
        p += 0.25
    if n in (3, 7, 11, 13, 17, 21, 23, 27):
        p += 0.20
    if n % 10 == 0:
        p -= 0.10
    if n >= 40:
        p -= 0.10
    return p


def is_patterned(ticket) -> bool:
    d = np.diff(ticket)
    return len(set(d.tolist())) <= 2 or len({n % 10 for n in ticket}) <= 3


def pick_pattern(score: np.ndarray, main_hist, pool, k, rng):
    """Best-scoring ticket among shape-valid candidates sampled toward high scores."""
    s = score[:pool]
    w = np.exp((s - s.max()) * 1.2)
    w /= w.sum()
    best, best_val = None, -np.inf
    for _ in range(40000):
        t = tuple(sorted((rng.choice(pool, size=k, replace=False, p=w) + 1).tolist()))
        if not shape_ok(t, main_hist, pool):
            continue
        val = float(s[np.array(t) - 1].sum())
        if val > best_val:
            best, best_val = t, val
    return list(best)


def pick_anticrowd(exclude, main_hist, pool, k, rng):
    """Least 'popular' shape-relaxed ticket, disjoint from `exclude`."""
    pop = np.array([popularity(n) for n in range(1, pool + 1)])
    avail = np.array([n for n in range(1, pool + 1) if n not in exclude])
    w = 1 / pop[avail - 1] ** 3
    w /= w.sum()
    best, best_val = None, np.inf
    for _ in range(40000):
        t = tuple(sorted(rng.choice(avail, size=k, replace=False, p=w).tolist()))
        arr = np.array(t)
        if is_patterned(arr) or (np.diff(arr) == 1).sum() > 1:
            continue
        decades = Counter((n - 1) // 10 for n in t)
        if (arr > 31).sum() < k - 2 or len(decades) < 3 or max(decades.values()) > 3:
            continue
        # tiny random jitter so the result is not always the same 'obvious' corner
        val = float(pop[arr - 1].sum()) + rng.random() * 0.3
        if val < best_val:
            best, best_val = t, val
    return list(best)


def next_draw(last: str, weekdays, today: dt.date) -> str:
    day = max(dt.date.fromisoformat(last), today - dt.timedelta(days=1)) + dt.timedelta(days=1)
    while day.weekday() not in weekdays:
        day += dt.timedelta(days=1)
    return day.isoformat()


# ------------------------------------------------------------------------- report
def bar(v, vmax, width=24):
    return "#" * max(1, round(width * v / vmax))


def fmt_ticket(t):
    return " ".join(f"{n:02d}" for n in t)


def run_game(game: str, sims: int, seed_extra: str, today: dt.date) -> tuple[dict, str]:
    cfg = GAMES[game]
    dates, main, bonus, pools = load(game)
    k, pool_now = cfg["k"], int(pools[-1])
    seed = int(hashlib.sha256(f"{game}|{dates[-1]}|{seed_extra}".encode()).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed)

    obs = observe(main, pools, sims, rng)
    bt = backtest(main, pools)
    sc = scores(main, pools, pool_now)
    real = obs["real"]
    counts, z = real["_counts"], real["_z"]
    gap = last_seen_gap(main, pools.max())

    set_a = pick_pattern(sc["ensemble"], main, pool_now, k, rng)
    set_b = pick_anticrowd(set(set_a), main, pool_now, k, rng)
    draw_date = next_draw(dates[-1], cfg["weekdays"], today)

    order = np.argsort(-z[:pool_now], kind="stable")
    hot = [(int(i + 1), int(counts[i]), float(z[i])) for i in order[:8]]
    cold = [(int(i + 1), int(counts[i]), float(z[i])) for i in order[::-1][:8]]
    overdue = [(int(i + 1), int(gap[i])) for i in np.argsort(-gap[:pool_now], kind="stable")[:8]]
    pair = real["_pair"]
    iu = np.triu_indices_from(pair, 1)
    top_pairs = sorted(zip(pair[iu].tolist(), (iu[0] + 1).tolist(), (iu[1] + 1).tolist()), reverse=True)[:5]
    sig = [t for t in obs["tests"] if t["p"] < 0.05]
    odds = 1
    for i in range(k):
        odds = odds * (pool_now - i) // (i + 1)

    L = [f"## {cfg['label']}", ""]
    L.append(f"- Draws analysed: **{len(dates)}** ({dates[0]} to {dates[-1]}), {k} main numbers from 1-{pool_now}")
    if len(cfg["pools"]) > 1:
        L.append(f"- Pool changed from {cfg['pools'][0][1]} to {cfg['pools'][1][1]} numbers on {cfg['pools'][1][0]}; "
                 "all statistics are exposure-adjusted for it")
    L.append(f"- Jackpot odds per line: 1 in {odds:,}")
    L += ["", f"### Picks for the {draw_date} draw", "",
          "| Set | Numbers | Basis |", "|---|---|---|",
          f"| A - pattern | **{fmt_ticket(set_a)}** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |",
          f"| B - anti-crowd | **{fmt_ticket(set_b)}** | numbers human players under-pick; no overlap with A |", ""]

    L += ["### 1. Observe - is anything non-random?", "",
          "| Statistic | Observed | Fair-draw 95% range | p |", "|---|---|---|---|"]
    for t in obs["tests"]:
        flag = " (!)" if t["p"] < 0.05 else ""
        L.append(f"| {t['label']} | {t['observed']:.2f} | {t['null_lo']:.2f} - {t['null_hi']:.2f} | {t['p']:.2f}{flag} |")
    L += ["", (f"{len(sig)} of {len(TESTS)} statistics fall outside the fair-draw range at p<0.05 "
               f"(about {0.05 * len(TESTS):.1f} expected by chance alone)."), ""]

    L += ["Hot numbers (drawn more than expected):", "", "```"]
    L += [f"{n:>2}  {c:>3}x  z={zz:+.2f}  {bar(c, counts.max())}" for n, c, zz in hot]
    L += ["```", "", "Cold numbers (drawn less than expected):", "", "```"]
    L += [f"{n:>2}  {c:>3}x  z={zz:+.2f}  {bar(c, counts.max())}" for n, c, zz in cold]
    L += ["```", "",
          "Most overdue (draws since last seen): " + ", ".join(f"{n} ({g})" for n, g in overdue), "",
          "Most frequent pairs: " + ", ".join(f"{a}-{b} ({c}x)" for c, a, b in top_pairs), ""]

    L += ["### 2. Learn - does any strategy beat random?", "",
          f"Walk-forward over the last {bt[0]['draws']} draws; each pick uses only earlier draws.", "",
          "| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |", "|---|---|---|---|---|"]
    for b in bt:
        L.append(f"| {b['strategy']} | {b['mean_matches']:.3f} | {b['expected_random']:.3f} | {b['z']:+.2f} | {b['best_single_ticket']} of {k} |")
    edge = [b for b in bt if abs(b["z"]) > 2.5]
    L += ["", ("No strategy differs from random by more than noise (|z| < 2.5 for all)." if not edge else
               "Flagged: " + ", ".join(b["strategy"] for b in edge) + " differ from random by |z| > 2.5; "
               "with 4 strategies tested, treat this as a lead to re-test, not a finding."), ""]

    result = {
        "game": cfg["label"], "next_draw": draw_date, "draws_analysed": len(dates),
        "data_range": [dates[0], dates[-1]], "pool": pool_now, "jackpot_odds": odds,
        "set_a_pattern": set_a, "set_b_anticrowd": set_b,
        "tests": obs["tests"], "backtest": bt,
        "hot": hot, "cold": cold, "overdue": overdue,
    }
    return result, "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=4000, help="Monte Carlo fair-draw histories")
    ap.add_argument("--seed-extra", default="", help="change to get a different (equally valid) pair of tickets")
    args = ap.parse_args()
    today = dt.date.today()

    results, sections = {}, []
    for game in GAMES:
        res, text = run_game(game, args.sims, args.seed_extra, today)
        results[game] = res
        sections.append(text)

    flags = [f"{r['game']}: {t['label']} (p={t['p']:.2f})"
             for r in results.values() for t in r["tests"] if t["p"] < 0.05]
    edges = [f"{r['game']}: {b['strategy']}" for r in results.values() for b in r["backtest"] if abs(b["z"]) > 2.5]
    n_tests = len(TESTS) * len(results)
    verdict = (
        f"Of {n_tests} pattern statistics, {len(flags)} fall outside the fair-draw range at p<0.05 "
        f"(about {0.05 * n_tests:.1f} expected from noise alone)"
        + (": " + "; ".join(flags) + ". " if flags else ". ")
        + ("No strategy back-tests better than chance. " if not edges else
           "Strategies flagged for re-testing: " + ", ".join(edges) + ". ")
    )
    head = [
        "# OLG Lotto Max & Lotto 6/49 - analyst report", "",
        f"Generated {today.isoformat()} by `analyze.py` from `data/*.csv` (refresh with `fetch.py`).", "",
        "**Read this first.** " + verdict
        + "Unless a strategy is flagged above, Set A has the same chance of winning as any other ticket. "
        "Set B also has the same chance of winning, but is built so that a win is less likely to be split.", "",
    ]
    (HERE / "report.md").write_text("\n".join(head + sections) + "\n")
    (HERE / "picks.json").write_text(json.dumps(results, indent=2) + "\n")

    for res in results.values():
        print(f"{res['game']}  (next draw {res['next_draw']}, {res['draws_analysed']} draws analysed)")
        print(f"  Set A pattern    : {fmt_ticket(res['set_a_pattern'])}")
        print(f"  Set B anti-crowd : {fmt_ticket(res['set_b_anticrowd'])}")
    print("Full analysis: report.md")


if __name__ == "__main__":
    main()
