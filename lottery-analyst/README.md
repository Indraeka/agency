# Lottery analyst - OLG Lotto Max & Lotto 6/49

Downloads three years of draw results, tests them for patterns, back-tests
number-picking strategies, and prints two sets of numbers per game for the next draw.

**Desktop:** double-click `start.bat` (Windows) or `start.command` (Mac). It installs
`numpy` if needed, starts the app and opens it in your browser. Keep the window open
while you use the page.

Or from a terminal:

```
python3 app.py        # opens http://127.0.0.1:8649
```

The page only works through this program. Opening `ui.html` directly, or from a
website, shows a "Start the app first" message.

The page has two buttons:

- **Refresh results** downloads any draws published since the last one on file and adds them to `data/*.csv`.
- **Generate numbers** produces Set A and Set B for the next draw of each game. Press it again for an alternative pair.

Each generated pair is saved to `history.json` and scored in the track record once its draw is published.

The same steps from the command line:

```
python3 fetch.py      # add new draws (--full re-downloads everything)
python3 analyze.py    # writes report.md + picks.json, prints the picks
```

Requires Python 3.10+ and `numpy`. Refreshing needs network access.

## What it does

| Stage | File | What happens |
|---|---|---|
| Collect | `fetch.py` | Scrapes lotteryextreme.com month by month for both games. Every Lotto Max draw is cross-checked against lottomaxnumbers.com; a missing scheduled draw or a disagreement fails the run. |
| Observe | `analyze.py` | Frequency, hot/cold, overdue, pairs, sums, odd/even, consecutive numbers, repeats. Each statistic is compared with thousands of simulated fair-draw histories. |
| Learn | `analyze.py` | Walk-forward back-test of hot / cold / overdue / ensemble strategies against the random expectation. |
| Interface | `app.py`, `ui.html` | Local web server and page that call the code above. Nothing is sent anywhere except the results download. |
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
