# Quarto AI

## Basic Game Flow
1. P1 turn start
2. P1 hands P2 a piece from the following list:
  - tall-square-hole-white    (tsh)
  - tall-square-solid-white   (tss)
  - tall-circle-hole-white    (tch)
  - tall-circle-solid-white   (tcs)
  - short-square-hole-white   (ssh)
  - short-square-solid-white  (sss)
  - short-circle-hole-white   (sch)
  - short-circle-solid-white  (scs)
3. P2 places given piece on a 4x4 grid
4. If P2 creates a 4 in a row (all: talls, shorts, squares, circles, holes, solids, or whites), P2 wins and P1 loses
5. Repeat Steps 1-4, switching "P1" for "P2" and "white" for "black", until one of the players wins or the board is full

## Terminal Commands
- q: quit, quits the game
- h: help, lists terminal commands