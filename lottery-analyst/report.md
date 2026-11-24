# OLG Lotto Max, Lotto 6/49 & Daily Grand - analyst report

Generated 2026-11-24 by `analyze.py` from `data/*.csv` (refresh with `fetch.py`).

**Read this first.** Of 25 pattern statistics, 1 fall outside the fair-draw range at p<0.05 (about 1.2 expected from noise alone): Lotto Max: Frequency chi-square (are some numbers favoured?) (p=0.04). No strategy back-tests better than chance. Unless a strategy is flagged above, Set A has the same chance of winning as any other ticket. Set B also has the same chance of winning, but is built so that a win is less likely to be split.

## Lotto Max

- Draws analysed: **317** (2023-11-10 to 2026-11-20), 7 main numbers from 1-52
- Pool changed from 50 to 52 numbers on 2026-04-14; all statistics are exposure-adjusted for it
- Jackpot odds per line: 1 in 133,784,560

### Picks for the 2026-11-24 draw

| Set | Numbers | Basis |
|---|---|---|
| A - pattern | **06 23 28 30 32 43 50** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |
| B - anti-crowd | **38 40 42 46 48 51 52** | numbers human players under-pick; no overlap with A |

### 1. Observe - is anything non-random?

| Statistic | Observed | Fair-draw 95% range | p |
|---|---|---|---|
| Frequency chi-square (are some numbers favoured?) | 28.64 | 29.26 - 63.79 | 0.04 (!) |
| Most extreme hot/cold number, |z| | 2.28 | 1.79 - 3.57 | 0.75 |
| Numbers repeated from previous draw (avg) | 1.02 | 0.88 - 1.07 | 0.39 |
| Most frequent pair, times drawn together | 15.00 | 13.00 - 17.00 | 0.77 |
| Average sum of main numbers | 180.44 | 175.86 - 183.99 | 0.83 |
| Spread (SD) of sums | 34.88 | 33.44 - 38.78 | 0.36 |
| Average count of odd numbers | 3.38 | 3.37 - 3.64 | 0.10 |
| Share of draws with a consecutive pair | 0.59 | 0.56 - 0.67 | 0.40 |

1 of 8 statistics fall outside the fair-draw range at p<0.05 (about 0.4 expected by chance alone).

Hot numbers (drawn more than expected):

```
 6   55x  z=+1.78  ########################
36   53x  z=+1.46  #######################
 7   51x  z=+1.13  ######################
28   51x  z=+1.13  ######################
43   51x  z=+1.13  ######################
 4   50x  z=+0.97  ######################
22   50x  z=+0.97  ######################
50   50x  z=+0.97  ######################
```

Cold numbers (drawn less than expected):

```
17   30x  z=-2.28  #############
42   35x  z=-1.47  ###############
27   36x  z=-1.30  ################
26   37x  z=-1.14  ################
13   38x  z=-0.98  #################
49   39x  z=-0.82  #################
19   39x  z=-0.82  #################
15   39x  z=-0.82  #################
```

Most overdue (draws since last seen): 18 (21), 45 (20), 14 (18), 17 (17), 42 (17), 38 (16), 49 (15), 2 (14)

Most frequent pairs: 22-46 (15x), 6-43 (14x), 6-30 (12x), 45-49 (11x), 32-46 (11x)

### 2. Learn - does any strategy beat random?

Walk-forward over the last 217 draws; each pick uses only earlier draws.

| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |
|---|---|---|---|---|
| hot | 0.968 | 0.969 | -0.02 | 4 of 7 |
| cold | 1.065 | 0.969 | +1.64 | 4 of 7 |
| overdue | 0.986 | 0.969 | +0.30 | 3 of 7 |
| ensemble | 0.940 | 0.969 | -0.50 | 4 of 7 |

No strategy differs from random by more than noise (|z| < 2.5 for all).

## Lotto 6/49

- Draws analysed: **317** (2023-11-11 to 2026-11-21), 6 main numbers from 1-49
- Jackpot odds per line: 1 in 13,983,816

### Picks for the 2026-11-25 draw

| Set | Numbers | Basis |
|---|---|---|
| A - pattern | **09 17 18 28 37 41** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |
| B - anti-crowd | **20 34 40 44 47 49** | numbers human players under-pick; no overlap with A |

### 1. Observe - is anything non-random?

| Statistic | Observed | Fair-draw 95% range | p |
|---|---|---|---|
| Frequency chi-square (are some numbers favoured?) | 34.76 | 27.24 - 62.33 | 0.35 |
| Most extreme hot/cold number, |z| | 2.26 | 1.74 - 3.46 | 0.72 |
| Numbers repeated from previous draw (avg) | 0.73 | 0.65 - 0.82 | 0.96 |
| Most frequent pair, times drawn together | 11.00 | 10.00 - 14.00 | 0.70 |
| Average sum of main numbers | 150.87 | 146.30 - 153.64 | 0.64 |
| Spread (SD) of sums | 31.97 | 30.27 - 35.16 | 0.54 |
| Average count of odd numbers | 3.12 | 2.93 - 3.19 | 0.38 |
| Share of draws with a consecutive pair | 0.50 | 0.44 - 0.55 | 1.00 |

0 of 8 statistics fall outside the fair-draw range at p<0.05 (about 0.4 expected by chance alone).

Hot numbers (drawn more than expected):

```
39   52x  z=+2.26  ########################
 9   50x  z=+1.92  #######################
42   48x  z=+1.57  ######################
28   46x  z=+1.23  #####################
49   46x  z=+1.23  #####################
41   45x  z=+1.06  #####################
46   45x  z=+1.06  #####################
37   44x  z=+0.89  ####################
```

Cold numbers (drawn less than expected):

```
47   28x  z=-1.85  #############
24   28x  z=-1.85  #############
19   29x  z=-1.68  #############
43   30x  z=-1.51  ##############
31   30x  z=-1.51  ##############
 6   33x  z=-1.00  ###############
32   34x  z=-0.83  ################
12   34x  z=-0.83  ################
```

Most overdue (draws since last seen): 30 (25), 24 (24), 6 (23), 14 (21), 17 (20), 48 (19), 13 (18), 32 (17)

Most frequent pairs: 18-39 (11x), 46-49 (10x), 39-41 (10x), 28-42 (10x), 26-35 (10x)

### 2. Learn - does any strategy beat random?

Walk-forward over the last 217 draws; each pick uses only earlier draws.

| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |
|---|---|---|---|---|
| hot | 0.760 | 0.735 | +0.50 | 3 of 6 |
| cold | 0.756 | 0.735 | +0.41 | 3 of 6 |
| overdue | 0.724 | 0.735 | -0.22 | 3 of 6 |
| ensemble | 0.747 | 0.735 | +0.23 | 3 of 6 |

No strategy differs from random by more than noise (|z| < 2.5 for all).

## Daily Grand

- Draws analysed: **320** (2023-11-02 to 2026-11-23), 5 main numbers from 1-49
- Jackpot odds per line: 1 in 13,348,188

### Picks for the 2026-11-26 draw

| Set | Numbers | Basis |
|---|---|---|
| A - pattern | **06 25 36 37 42 + Grand Number 6** | top ensemble score (long-run + recent frequency, overdue) with a typical sum/odd-even shape |
| B - anti-crowd | **30 40 43 47 48 + Grand Number 3** | numbers human players under-pick; no overlap with A |

### 1. Observe - is anything non-random?

| Statistic | Observed | Fair-draw 95% range | p |
|---|---|---|---|
| Frequency chi-square (are some numbers favoured?) | 51.12 | 27.84 - 63.12 | 0.39 |
| Most extreme hot/cold number, |z| | 3.02 | 1.78 - 3.57 | 0.30 |
| Numbers repeated from previous draw (avg) | 0.46 | 0.44 - 0.58 | 0.20 |
| Most frequent pair, times drawn together | 9.00 | 8.00 - 12.00 | 1.00 |
| Average sum of main numbers | 127.66 | 121.78 - 128.20 | 0.10 |
| Spread (SD) of sums | 29.92 | 28.05 - 32.41 | 0.79 |
| Average count of odd numbers | 2.60 | 2.43 - 2.67 | 0.41 |
| Share of draws with a consecutive pair | 0.33 | 0.31 - 0.41 | 0.27 |
| Grand Number frequency chi-square | 8.52 | 1.21 - 14.60 | 0.41 |

0 of 9 statistics fall outside the fair-draw range at p<0.05 (about 0.5 expected by chance alone).

Hot numbers (drawn more than expected):

```
42   49x  z=+3.02  ########################
37   47x  z=+2.65  #######################
 5   40x  z=+1.36  ####################
25   40x  z=+1.36  ####################
33   39x  z=+1.17  ###################
36   39x  z=+1.17  ###################
45   39x  z=+1.17  ###################
18   38x  z=+0.99  ###################
```

Cold numbers (drawn less than expected):

```
40   19x  z=-2.52  #########
15   23x  z=-1.78  ###########
 9   23x  z=-1.78  ###########
 4   23x  z=-1.78  ###########
38   24x  z=-1.60  ############
26   25x  z=-1.41  ############
16   25x  z=-1.41  ############
34   26x  z=-1.23  #############
```

Most overdue (draws since last seen): 11 (32), 4 (30), 15 (28), 49 (27), 23 (24), 9 (22), 31 (21), 19 (20)

Most frequent pairs: 37-42 (9x), 28-42 (9x), 25-42 (9x), 21-37 (9x), 35-45 (8x)

### 2. Learn - does any strategy beat random?

Walk-forward over the last 220 draws; each pick uses only earlier draws.

| Strategy | Avg matches/ticket | Random expectation | z | Best single ticket |
|---|---|---|---|---|
| hot | 0.555 | 0.510 | +1.01 | 2 of 5 |
| cold | 0.482 | 0.510 | -0.65 | 2 of 5 |
| overdue | 0.550 | 0.510 | +0.91 | 2 of 5 |
| ensemble | 0.555 | 0.510 | +1.01 | 2 of 5 |

No strategy differs from random by more than noise (|z| < 2.5 for all).

