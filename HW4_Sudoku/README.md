# Homework 4: CSPs

## I. Introduction

**Usage**:

```
python driver.py <input_string>
```

The objective of Sudoku is to fill a 9x9 grid with the numbers 1-9 so that each column, row, and 3x
sub-grid (or box) contains one of each digit.  Sudoku has 81  **variables** , i.e. 81 tiles. The variables are named by  **row**  and  **column** , and are  **valued**  from 1 to 9 subject to the constraints that no two cells in the same row, column, or box may be the same.
The problem here was framed in terms of  **variables** ,  **domains** , and  **constraints.** We suggest representing a Sudoku board with a Python dictionary, where each key is a variable name based on location, and value of the tile placed there. Using variable names  **Al** ...  **A9... I1... I9,**  the board above has:

- _sudoku_dict_ [" **B1** "] =  **9** , and
- _sudoku_dict_ [" **E9** "] =  **8** .
  We give value  **zero**  to a tile that has not yet been filled.

**Methodologies:**

Implemented  **backtracking**  search using the  **minimum remaining value**  heuristic and apply  **forward checking**  to reduce variables domains.

## II. Input

The  input string  is represented as:
003020600900305001001806400008102900700000008006708200002609500800203009005010300
Which is equivalent to:

| 0    | 0    | 3    | 0    | 2    | 0    | 6    | 0    | 0    |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 9    | 0    | 0    | 3    | 0    | 5    | 0    | 0    | 1    |
| 0    | 0    | 1    | 8    | 0    | 6    | 4    | 0    | 0    |
| 0    | 0    | 8    | 1    | 0    | 2    | 9    | 0    | 0    |
| 7    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 8    |
| 0    | 0    | 6    | 7    | 0    | 8    | 2    | 0    | 0    |
| 0    | 0    | 2    | 6    | 0    | 9    | 5    | 0    | 0    |
| 8    | 0    | 0    | 2    | 0    | 3    | 0    | 0    | 9    |
| 0    | 0    | 5    | 0    | 1    | 0    | 3    | 0    | 0    |

## II. Output

The program will generate output.txt, containing a single line of text representing the finished Sudoku
board. E.g.:
483921657967345821251876493548132976729564138136798245372689514814253769695417382

