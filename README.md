# Game of Life
A simulation of Conway's Game of Life in Python using pygame

## Rules of the Game

```
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
```
(from [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life))

## Prerequisites

If Python 3 is present on the system, the required modules can be installed with
```sh
pip install -r requirements.txt
```

## Usage

The file can be run using
```sh
py GameOfLife.py
```
