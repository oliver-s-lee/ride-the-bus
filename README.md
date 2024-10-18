

# Results

All data presented here was simulated with 10,000 repeats.

|  | With ace rule |  |  | No ace rule |  |  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Num cards | Counter | Blind | Random | Counter | Blind | Random |
1 | 1.4 (± 0.7) | 1.4 (± 0.7) | 2.3 (± 1.7) | 1.3 (± 0.6) | 1.3 (± 0.6) | 2.1 (± 1.5)
2 | 2.0 (± 1.2) | 2.0 (± 1.2) | 5.3 (± 4.7) | 1.8 (± 1.1) | 1.8 (± 1.1) | 4.5 (± 4)
3 | 2.8 (± 2.0) | 2.8 (± 2.0) | 12 (± 11.6) | 2.4 (± 1.7) | 2.5 (± 1.8) | 9.5 (± 9)
4 | 3.9 (± 3.0) | 4.0 (± 3.1) | 27.9 (± 26.7) | 3.3 (± 2.6) | 3.4 (± 2.6) | 20.2 (± 19.9)
5 | 5.6 (± 4.4) | 5.8 (± 4.8) | 65 (± 65.4) | 4.5 (± 3.6) | 4.6 (± 3.7) | 43.7 (± 43.9)
6 | 7.8 (± 6.3) | 8.3 (± 7.0) | 150.5 (± 147.7) | 6.0 (± 5.0) | 6.3 (± 5.4) | 89.5 (± 89.8)
7 | 10.9 (± 8.9) | 11.9 (± 10.5) | 351.5 (± 346.5) | 8.1 (± 6.6) | 8.8 (± 7.8) | 199.1 (± 197.6)
8 | 15.2 (± 12.9) | 17.2 (± 15.0) | 804.9 (± 787.9) | 10.6 (± 9.0) | 11.9 (± 10.9) | 416.1 (± 414.5)
9 | 21.6 (± 18.8) | 25.3 (± 22.8) | 0.0 (± 0.0) | 13.9 (± 12.1) | 16.5 (± 15.0) | 872.5 (± 874.5)
10 | 30.4 (± 26.7) | 36.8 (± 33.3) | 0 (± 0) | 18.2 (± 16) | 22.7 (± 20.7) | 1894.6 (± 1878.8)
11 | 43.3 (± 38.5) | 54.8 (± 50.2) | 0 (± 0) | 24.1 (± 21.5) | 31.2 (± 29.1) | 3932.3 (± 3910.9)
12 | 60.8 (± 54.5) | 79.3 (± 72.5) | 0 (± 0) | 32.3 (± 29.6) | 43.4 (± 40.7) | 8512 (± 8526.3)
13 | 86.1 (± 78.7) | 116.5 (± 104.9) | 0 (± 0) | 42.3 (± 39) | 58.9 (± 55.2) | 17738.1 (± 18086.9)

For an average (6 card) game:
 - Playing with the ace rule makes the game 23% harder (when card counting)
 - Refusing to card count makes the game 6% harder (when playing with the ace rule)

# Fitting results

![With ace rule](./Graphs/fitted_ace.png)

![No ace rule](./Graphs/fitted_no_ace.png)

For the various game and player types, the solved equations are as follows:

| Player | With ace rule | No ace rule |
| ------ | ------------- | ----------- |
| Counter | $0.991 \texttimes \exp(0.343x)$ | $1.042 \texttimes \exp(0.287x)$
| Blind  | $0.918 \texttimes \exp(0.370x)$ | $0.957 \texttimes \exp(0.317x)$
| Random | $0.980 \texttimes \exp(0.839x)$ | $0.994 \texttimes \exp(0.754x)$