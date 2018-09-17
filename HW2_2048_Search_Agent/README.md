# Homework 2: Adversarial Search

## I.Introduction

This is an adversarial search agent to play the  **2048-puzzle**  game. 

**How to use:**

```
python GameManager.py
```

A demo of the game is available here:  **gabrielecirulli.github.io/2048** .

#### 2048 As A Two-Player Game

2048 is played on a  **4×4 grid**  with numbered tiles which can slide up, down, left, or right. This game can
be modeled as a two player game, in which the computer AI generates a 2- or 4-tile placed randomly on
the board, and the player then selects a direction to move the tiles. Note that the tiles move until they
either (1) collide with another tile, or (2) collide with the edge of the grid. If two tiles of the same number
collide in a move, they merge into a single tile valued at the sum of the two originals. The resulting tile
cannot merge with another tile again in the same move.

Usually, each role in a two-player games has a similar set of moves to choose from, and similar
objectives (e.g. chess). In 2048 however, the player roles are inherently  **asymmetric** , as the Computer AI
places tiles and the Player moves them. Adversarial search can still be applied! 

#### Search Algorithm: Expectiminimax

The tile-generating Computer AI of 2048 is not particularly adversarial as it spawns tiles irrespective of
whether a spawn is the most adversarial to the user’s progress, with a 90% probability of a 2 and 10% for
a 4 (from GameManager.py). However, our Player AI will play  **as if**  the computer is adversarial since this
proves more effective in beating the game. We will specifically use the  **expectiminimax** algorithm.

● **GameManager.py**. This is the driver program that loads Computer AI and Player AI and
begins a game where they compete with each other. 

● **Grid.py.** This module defines the Grid object, along with some useful operations:
move(), getAvailableCells(), insertTile(), and clone()

● **BaseAI.py.** This is the base class for any AI component. All AIs inherit from this module, and
implement the getMove() function, which takes a Grid object as parameter and returns a move (there are
different "moves" for different AIs).

● **ComputerAI.py.** This inherits from BaseAI. The getMove() function returns a computer action
that is a tuple (x, y) indicating the place you want to place a tile.

● **PlayerAI.py.** The PlayerAI class should inherit from BaseAI. The getMove() function to implement must return a number that indicates the player’s action. In particular,  **0 stands for "Up", 1 stands for "Down", 2 stands for "Left", and 3 stands for "Right"** . 

● **BaseDisplayer.py and Displayer.py.** These print the grid.

## II. Contributions

● Employed the  **expectiminimax algorithm**.

● Implemented  **alpha-beta pruning** . This should speed up the search process by eliminating irrelevant branches. 

● Used  **heuristic functions** and assigned  **heuristic weights**:

> Maxcell: 1.0
>
> Average: 1.0
>
> Freetiles: 1.0
>
> Smoothness: 1.0
>
> Monotonicity: 1.0



