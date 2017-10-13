# Artificial Intelligence Nanodegree
# Intelligent Sudoku Solver

# Naming 

**`Rows`** are indexed by letter from A to I: `[A, B, C, D, E, F, G, H, I]`

**`Columns`** are indexed by numbers from 1 to 9: `[1, 2, 3, 4, 5, 6, 7, 8, 9]`

**`Boxes`** are 3x3 units and there are 9 of them on the board

**`Units`** are the complete rows, columns, and 3x3 squares, 27 of them in total. 

**`Peers`** are all other cells that belong to common unit

# Encoding
At first the board is represented in the following format.
```
. . 3 |. 2 . |6 . . 
9 . . |3 . 5 |. . 1 
. . 1 |8 . 6 |4 . . 
------+------+------
. . 8 |1 . 2 |9 . . 
7 . . |. . . |. . 8 
. . 6 |7 . 8 |2 . . 
------+------+------
. . 2 |6 . 9 |5 . . 
8 . . |2 . 3 |. . 9 
. . 5 |. 1 . |3 . .
```
Then every empty cell (`.`) is replaced by the string of all digits (`123456789`).
```
123456789 123456789     3     |123456789     2     123456789 |    6     123456789 123456789 
    9     123456789 123456789 |    3     123456789     5     |123456789 123456789     1     
123456789 123456789     1     |    8     123456789     6     |    4     123456789 123456789 
------------------------------+------------------------------+------------------------------
123456789 123456789     8     |    1     123456789     2     |    9     123456789 123456789 
    7     123456789 123456789 |123456789 123456789 123456789 |123456789 123456789     8     
123456789 123456789     6     |    7     123456789     8     |    2     123456789 123456789 
------------------------------+------------------------------+------------------------------
123456789 123456789     2     |    6     123456789     9     |    5     123456789 123456789 
    8     123456789 123456789 |    2     123456789     3     |123456789 123456789     9     
```
The algorithm will be using this representation of the grid, to solve the puzzle. 

## Techniques used

The agent uses **Elimination**, **Only Choice**, **Naked Twins** and **Depth First Search** to solve the puzzle.

### Eliminate
For every single cell on the board that already has a value assigned to it. **Eliminate** goes over other cells in goes over all of its peers that have the same value and erases it from there as that value can appear only once in that unit. 

### Only Choice
In unit among all cells if the one cell has a value that only present in that cell and not any others, then it is concluded that this cell is only the one that can hold that value, so the value is assigned to it.

### Naked Twins
Two cells that are found inside the unit and have a length of two are called locked cells. Constraint propagation imposes that two digits cannot be assigned to any other cell other than those two. So all the cells in the unit are to be visited and digits are to be removed from them.  

### Depth-first search 
DFS is an algorithm for traversing or searching tree or graph data structures. One starts at the root and explores as far as possible along each branch before backtracking - [Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)

### Additional version of Sudoku: Diagonal
A diagonal version of Sudoku enforces to add indexes of diagonal boxes to the set of units so that during elimination diagonals are also considered. More of such constraints allow reducing the number of branches, which reduces the size of a problem and leads to a shorter path to the desired solution.  


# Installation

This project requires **Python 3**. 

Optionally, you can also install **`pygame`** if you want to see visualization. 

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

# Code

* `solutions.py` - Contains the implementation of algorithms that solve Sudoku puzzle.
* `solution_test.py` - Unit tests for the correctness of algorithms.
* `PySudoku.py` and `visualize.py` are used for visualization. (However start `solutions.py` not these two, as it will call visualization automatically.)


# Example
Exectuion of `python solutions.py`, will produce terminal output of the solved puzzle:
```
2 6 7 |9 4 5 |3 8 1 
8 5 3 |7 1 6 |2 4 9 
4 9 1 |8 2 3 |5 7 6 
------+------+------
5 7 6 |4 3 8 |1 9 2 
3 8 4 |1 9 2 |6 5 7 
1 2 9 |6 5 7 |4 3 8 
------+------+------
6 4 2 |3 7 9 |8 1 5 
9 3 5 |2 8 1 |7 6 4 
7 1 8 |5 6 4 |9 2 3 
```
and run the visualisation that will look like following
![Image of Yaktocat](images/sudoku.gif)

(visualization delay is made for purpose, puzzle is solved instantly as you can see from the terminal at right)