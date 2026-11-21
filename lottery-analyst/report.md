# OLG Lotto Max, Lotto 6/49 & Daily Grand - analyst report

Generated 2026-11-21 by `analyze.py` from `data/*.csv` (refresh with `fetch.py`).

**Read this first.** Of 25 pattern statistics, 1 fall outside the fair-draw range at p<0.05 (about 1.2 expected from noise alone): Lotto Max: Frequency chi-square (are some numbers favoured?) (p=0.04). No strategy back-tests better than chance. Unless a strategy is flagged above, Set A has the same chance of winning as any other ticket. Set B also has the same chance of winning, but is built so that a win is less likely to be split.

## Lotto Max

- Draws analysed: **316** (2023-11-10 to 2026-11-17), 7 main numbers from 1-52
- Pool changed from 50 to 52 numbers on 2026-04-14; all statistics are exposure-adjusted for it
- Jackpot odds per line: 1 in 133,784,560

### Picks for the 2026-11-24 draw

| Set | Numbers | Basis |
|---|---|---|
| A - pattern | **06 18 28 30 41 43 50** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |
| B - anti-crowd | **32 40 45 47 49 51 52** | numbers human players under-pick; no overlap with A |

### 1. Observe - is anything non-random?

| Statistic | Observed | Fair-draw 95% range | p |
|---|---|---|---|
| Frequency chi-square (are some numbers favoured?) | 28.80 | 29.30 - 63.29 | 0.04 (!) |
| Most extreme hot/cold number, |z| | 2.26 | 1.81 - 3.59 | 0.58 |
| Numbers repeated from previous draw (avg) | 1.02 | 0.88 - 1.06 | 0.33 |
| Most frequent pair, times drawn together | 15.00 | 12.00 - 17.00 | 0.72 |
| Average sum of main numbers | 180.39 | 175.99 - 184.03 | 0.80 |
| Spread (SD) of sums | 34.92 | 33.34 - 38.77 | 0.37 |
| Average count of odd numbers | 3.39 | 3.37 - 3.64 | 0.11 |
| Share of draws with a consecutive pair | 0.59 | 0.56 - 0.67 | 0.46 |

1 of 8 statistics fall outside the fair-draw range at p<0.05 (about 0.4 expected by chance alone).

Hot numbers (drawn more than expected):

```
 6   54x  z=+1.64  ########################
36   53x  z=+1.48  ########################
 7   51x  z=+1.15  #######################
28   51x  z=+1.15  #######################
43   51x  z=+1.15  #######################
 4   50x  z=+0.99  ######################
22   50x  z=+0.99  ######################
50   50x  z=+0.99  ######################
```

Cold numbers (drawn less than expected):

```
17   30x  z=-2.26  #############
42   35x  z=-1.45  ################
27   36x  z=-1.29  ################
26   37x  z=-1.12  ################
13   38x  z=-0.96  #################
49   39x  z=-0.80  #################
19   39x  z=-0.80  #################
15   39x  z=-0.80  #################
```

Most overdue (draws since last seen): 18 (20), 45 (19), 40 (18), 14 (17), 17 (16), 42 (16), 38 (15), 49 (14)

Most frequent pairs: 22-46 (15x), 6-43 (14x), 6-30 (12x), 45-49 (11x), 32-46 (11x)

### 2. Learn - does any strategy beat random?

Walk-forward over the last 216 draws; each pick uses only earlier draws.

| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |
|---|---|---|---|---|
| hot | 0.972 | 0.969 | +0.06 | 4 of 7 |
| cold | 1.069 | 0.969 | +1.72 | 4 of 7 |
| overdue | 0.986 | 0.969 | +0.29 | 3 of 7 |
| ensemble | 0.940 | 0.969 | -0.50 | 4 of 7 |

No strategy differs from random by more than noise (|z| < 2.5 for all).

## Lotto 6/49

- Draws analysed: **316** (2023-11-11 to 2026-11-18), 6 main numbers from 1-49
- Jackpot odds per line: 1 in 13,983,816

### Picks for the 2026-11-21 draw

| Set | Numbers | Basis |
|---|---|---|
| A - pattern | **09 17 28 37 41 46** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |
| B - anti-crowd | **30 36 40 42 44 48** | numbers human players under-pick; no overlap with A |

### 1. Observe - is anything non-random?

| Statistic | Observed | Fair-draw 95% range | p |
|---|---|---|---|
| Frequency chi-square (are some numbers favoured?) | 33.56 | 27.72 - 62.40 | 0.28 |
| Most extreme hot/cold number, |z| | 2.11 | 1.77 - 3.48 | 0.43 |
| Numbers repeated from previous draw (avg) | 0.73 | 0.65 - 0.83 | 1.00 |
| Most frequent pair, times drawn together | 11.00 | 10.00 - 14.00 | 0.71 |
| Average sum of main numbers | 150.90 | 146.52 - 153.58 | 0.63 |
| Spread (SD) of sums | 32.01 | 30.26 - 35.12 | 0.58 |
| Average count of odd numbers | 3.12 | 2.93 - 3.19 | 0.39 |
| Share of draws with a consecutive pair | 0.49 | 0.44 - 0.55 | 0.97 |

0 of 8 statistics fall outside the fair-draw range at p<0.05 (about 0.4 expected by chance alone).

Hot numbers (drawn more than expected):

```
39   51x  z=+2.11  ########################
 9   49x  z=+1.77  #######################
42   48x  z=+1.60  #######################
28   46x  z=+1.25  ######################
49   46x  z=+1.25  ######################
41   45x  z=+1.08  #####################
46   45x  z=+1.08  #####################
37   44x  z=+0.91  #####################
```

Cold numbers (drawn less than expected):

```
47   28x  z=-1.84  #############
24   28x  z=-1.84  #############
19   29x  z=-1.66  ##############
43   30x  z=-1.49  ##############
31   30x  z=-1.49  ##############
 6   33x  z=-0.98  ################
38   34x  z=-0.81  ################
32   34x  z=-0.81  ################
```

Most overdue (draws since last seen): 30 (24), 24 (23), 6 (22), 14 (20), 17 (19), 48 (18), 13 (17), 32 (16)

Most frequent pairs: 18-39 (11x), 46-49 (10x), 39-41 (10x), 28-42 (10x), 26-35 (10x)

### 2. Learn - does any strategy beat random?

Walk-forward over the last 216 draws; each pick uses only earlier draws.

| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |
|---|---|---|---|---|
| hot | 0.759 | 0.735 | +0.48 | 3 of 6 |
| cold | 0.759 | 0.735 | +0.48 | 3 of 6 |
| overdue | 0.727 | 0.735 | -0.15 | 3 of 6 |
| ensemble | 0.741 | 0.735 | +0.12 | 3 of 6 |

No strategy differs from random by more than noise (|z| < 2.5 for all).

## Daily Grand

- Draws analysed: **319** (2023-11-02 to 2026-11-19), 5 main numbers from 1-49
- Jackpot odds per line: 1 in 13,348,188

### Picks for the 2026-11-23 draw

| Set | Numbers | Basis |
|---|---|---|
| A - pattern | **06 25 36 37 42 + Grand Number 6** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |
| B - anti-crowd | **20 40 45 47 48 + Grand Number 4** | numbers human players under-pick; no overlap with A |

### 1. Observe - is anything non-random?

| Statistic | Observed | Fair-draw 95% range | p |
|---|---|---|---|
| Frequency chi-square (are some numbers favoured?) | 51.31 | 28.14 - 63.10 | 0.37 |
| Most extreme hot/cold number, |z| | 3.04 | 1.75 - 3.41 | 0.27 |
| Numbers repeated from previous draw (avg) | 0.47 | 0.44 - 0.58 | 0.23 |
| Most frequent pair, times drawn together | 9.00 | 8.00 - 12.00 | 1.00 |
| Average sum of main numbers | 127.53 | 121.61 - 128.28 | 0.13 |
| Spread (SD) of sums | 29.87 | 28.00 - 32.44 | 0.77 |
| Average count of odd numbers | 2.61 | 2.43 - 2.67 | 0.37 |
| Share of draws with a consecutive pair | 0.33 | 0.31 - 0.41 | 0.27 |
| Grand Number frequency chi-square | 8.64 | 1.22 - 13.99 | 0.38 |

0 of 9 statistics fall outside the fair-draw range at p<0.05 (about 0.5 expected by chance alone).

Hot numbers (drawn more than expected):

```
42   49x  z=+3.04  ########################
37   47x  z=+2.67  #######################
 5   40x  z=+1.38  ####################
25   40x  z=+1.38  ####################
33   39x  z=+1.19  ###################
45   39x  z=+1.19  ###################
18   38x  z=+1.01  ###################
36   38x  z=+1.01  ###################
```

Cold numbers (drawn less than expected):

```
40   19x  z=-2.51  #########
15   23x  z=-1.77  ###########
 9   23x  z=-1.77  ###########
 4   23x  z=-1.77  ###########
38   24x  z=-1.58  ############
34   25x  z=-1.40  ############
26   25x  z=-1.40  ############
16   25x  z=-1.40  ############
```

Most overdue (draws since last seen): 11 (31), 4 (29), 15 (27), 49 (26), 23 (23), 34 (23), 9 (21), 31 (20)

Most frequent pairs: 37-42 (9x), 28-42 (9x), 25-42 (9x), 21-37 (9x), 35-45 (8x)

### 2. Learn - does any strategy beat random?

Walk-forward over the last 219 draws; each pick uses only earlier draws.

| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |
|---|---|---|---|---|
| hot | 0.553 | 0.510 | +0.97 | 2 of 5 |
| cold | 0.484 | 0.510 | -0.60 | 2 of 5 |
| overdue | 0.553 | 0.510 | +0.97 | 2 of 5 |
| ensemble | 0.553 | 0.510 | +0.97 | 2 of 5 |

No strategy differs from random by more than noise (|z| < 2.5 for all).

