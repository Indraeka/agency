# OLG Lotto Max & Lotto 6/49 - analyst report

Generated 2026-11-11 by `analyze.py` from `data/*.csv` (refresh with `fetch.py`).

**Read this first.** Of 16 pattern statistics, 1 fall outside the fair-draw range at p<0.05 (about 0.8 expected from noise alone): Lotto Max: Frequency chi-square (are some numbers favoured?) (p=0.04). No strategy back-tests better than chance. Unless a strategy is flagged above, Set A has the same chance of winning as any other ticket. Set B also has the same chance of winning, but is built so that a win is less likely to be split.

## Lotto Max

- Draws analysed: **314** (2023-11-10 to 2026-11-10), 7 main numbers from 1-52
- Pool changed from 50 to 52 numbers on 2026-04-14; all statistics are exposure-adjusted for it
- Jackpot odds per line: 1 in 133,784,560

### Picks for the 2026-11-13 draw

| Set | Numbers | Basis |
|---|---|---|
| A - pattern | **06 07 30 41 43 50 52** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |
| B - anti-crowd | **32 34 40 45 48 49 51** | numbers human players under-pick; no overlap with A |

### 1. Observe - is anything non-random?

| Statistic | Observed | Fair-draw 95% range | p |
|---|---|---|---|
| Frequency chi-square (are some numbers favoured?) | 28.71 | 29.30 - 63.05 | 0.04 (!) |
| Most extreme hot/cold number, |z| | 2.22 | 1.85 - 3.53 | 0.63 |
| Numbers repeated from previous draw (avg) | 1.02 | 0.88 - 1.07 | 0.39 |
| Most frequent pair, times drawn together | 15.00 | 12.00 - 17.00 | 0.68 |
| Average sum of main numbers | 180.45 | 175.82 - 183.80 | 0.74 |
| Spread (SD) of sums | 35.02 | 33.45 - 38.72 | 0.44 |
| Average count of odd numbers | 3.39 | 3.36 - 3.64 | 0.12 |
| Share of draws with a consecutive pair | 0.59 | 0.56 - 0.67 | 0.45 |

1 of 8 statistics fall outside the fair-draw range at p<0.05 (about 0.4 expected by chance alone).

Hot numbers (drawn more than expected):

```
 6   54x  z=+1.69  ########################
36   53x  z=+1.53  ########################
 7   51x  z=+1.20  #######################
28   51x  z=+1.20  #######################
43   51x  z=+1.20  #######################
22   50x  z=+1.04  ######################
50   50x  z=+1.04  ######################
30   49x  z=+0.88  ######################
```

Cold numbers (drawn less than expected):

```
17   30x  z=-2.22  #############
42   35x  z=-1.41  ################
27   35x  z=-1.41  ################
26   37x  z=-1.08  ################
15   38x  z=-0.92  #################
13   38x  z=-0.92  #################
49   39x  z=-0.76  #################
19   39x  z=-0.76  #################
```

Most overdue (draws since last seen): 27 (30), 9 (26), 18 (18), 45 (17), 40 (16), 14 (15), 17 (14), 42 (14)

Most frequent pairs: 22-46 (15x), 6-43 (14x), 6-30 (12x), 45-49 (11x), 28-36 (11x)

### 2. Learn - does any strategy beat random?

Walk-forward over the last 214 draws; each pick uses only earlier draws.

| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |
|---|---|---|---|---|
| hot | 0.981 | 0.969 | +0.21 | 4 of 7 |
| cold | 1.070 | 0.969 | +1.72 | 4 of 7 |
| overdue | 0.986 | 0.969 | +0.29 | 3 of 7 |
| ensemble | 0.944 | 0.969 | -0.43 | 4 of 7 |

No strategy differs from random by more than noise (|z| < 2.5 for all).

## Lotto 6/49

- Draws analysed: **313** (2023-11-11 to 2026-11-07), 6 main numbers from 1-49
- Jackpot odds per line: 1 in 13,983,816

### Picks for the 2026-11-11 draw

| Set | Numbers | Basis |
|---|---|---|
| A - pattern | **09 17 37 41 42 46** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |
| B - anti-crowd | **30 38 40 44 45 48** | numbers human players under-pick; no overlap with A |

### 1. Observe - is anything non-random?

| Statistic | Observed | Fair-draw 95% range | p |
|---|---|---|---|
| Frequency chi-square (are some numbers favoured?) | 33.63 | 27.31 - 61.39 | 0.27 |
| Most extreme hot/cold number, |z| | 2.19 | 1.78 - 3.56 | 0.59 |
| Numbers repeated from previous draw (avg) | 0.74 | 0.65 - 0.82 | 0.99 |
| Most frequent pair, times drawn together | 11.00 | 10.00 - 14.00 | 0.78 |
| Average sum of main numbers | 150.88 | 146.46 - 153.70 | 0.64 |
| Spread (SD) of sums | 32.05 | 30.34 - 35.20 | 0.59 |
| Average count of odd numbers | 3.12 | 2.93 - 3.19 | 0.41 |
| Share of draws with a consecutive pair | 0.49 | 0.44 - 0.55 | 0.96 |

0 of 8 statistics fall outside the fair-draw range at p<0.05 (about 0.4 expected by chance alone).

Hot numbers (drawn more than expected):

```
39   51x  z=+2.19  ########################
 9   48x  z=+1.67  #######################
42   47x  z=+1.50  ######################
28   45x  z=+1.15  #####################
41   45x  z=+1.15  #####################
46   45x  z=+1.15  #####################
49   45x  z=+1.15  #####################
15   43x  z=+0.81  ####################
```

Cold numbers (drawn less than expected):

```
47   27x  z=-1.95  #############
24   28x  z=-1.78  #############
19   29x  z=-1.61  ##############
43   30x  z=-1.44  ##############
31   30x  z=-1.44  ##############
38   33x  z=-0.92  ################
 6   33x  z=-0.92  ################
32   34x  z=-0.75  ################
```

Most overdue (draws since last seen): 40 (43), 44 (28), 2 (21), 30 (21), 24 (20), 6 (19), 34 (18), 14 (17)

Most frequent pairs: 18-39 (11x), 46-49 (10x), 39-41 (10x), 26-35 (10x), 23-28 (10x)

### 2. Learn - does any strategy beat random?

Walk-forward over the last 213 draws; each pick uses only earlier draws.

| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |
|---|---|---|---|---|
| hot | 0.761 | 0.735 | +0.50 | 3 of 6 |
| cold | 0.765 | 0.735 | +0.59 | 3 of 6 |
| overdue | 0.723 | 0.735 | -0.22 | 3 of 6 |
| ensemble | 0.737 | 0.735 | +0.05 | 3 of 6 |

No strategy differs from random by more than noise (|z| < 2.5 for all).

