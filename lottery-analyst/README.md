# Lottery analyst - OLG Lotto Max & Lotto 6/49

Downloads three years of draw results, tests them for patterns, back-tests
number-picking strategies, and prints two sets of numbers per game for the next draw.

```
python3 fetch.py      # refresh data/*.csv (needs network; numpy not required)
python3 analyze.py    # writes report.md + picks.json, prints the picks
```

Requires Python 3.10+ and `numpy`.

## What it does

| Stage | File | What happens |
|---|---|---|
| Collect | `fetch.py` | Scrapes lotteryextreme.com month by month for both games. Every Lotto Max draw is cross-checked against lottomaxnumbers.com; a missing scheduled draw or a disagreement fails the run. |
| Observe | `analyze.py` | Frequency, hot/cold, overdue, pairs, sums, odd/even, consecutive numbers, repeats. Each statistic is compared with thousands of simulated fair-draw histories. |
| Learn | `analyze.py` | Walk-forward back-test of hot / cold / overdue / ensemble strategies against the random expectation. |
| Pick | `analyze.py` | Set A: best ensemble score with a typical shape. Set B: numbers human players under-pick (reduces prize sharing), no overlap with A. |

## Limits

- Draws are independent. In the data so far no strategy beats random, so Set A
  is a principled tie-break, not an edge. `report.md` shows the evidence on every run.
- Set B's popularity model is built from published research on player habits
  (birthdays, lucky numbers), not from OLG ticket data, which is not public.
- Lotto 6/49 covers the Classic Draw only; the Gold Ball draw is a raffle with no numbers to choose.
- Lotto Max moved from 50 to 52 numbers on 2026-04-14; statistics adjust for this.
  Add any future rule change to `GAMES[...]["pools"]` in `analyze.py`.
- Picks are deterministic for a given dataset. `--seed-extra anything` gives another pair.
