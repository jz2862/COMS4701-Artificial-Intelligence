# Homework 1: Search Algorithms

### I. Introduction

The N-puzzle game consists of a board holding N = m^2 − 1 distinct movable tiles, plus one empty space.
There is one tile for each number in the set {1, ..., m^2 − 1}. In this assignment, we will represent the blank space with the number 0 and focus on the m = 3 case (8-puzzle).

In this combinatorial search problem, the aim is to get from any initial board state to the configuration with all tiles arranged in ascending order ⟨0, 1,..., m^2 − 1⟩ -- this is your goal state. The search space is the set of all possible states reachable from the initial state. Each move consists of swapping the empty space with a component in one of the four directions {‘Up’, ‘Down’, ‘Left’, ‘Right’}.

Give each move a cost of one. Thus, the total cost of a path will be equal to the number of moves made.

### II.Input

driver.py  solves any 8-puzzle board when given an arbitrary starting configuration. The program will be executed as follows:

```python
python driver.py <method> <board>
EXAMPLE:
python driver.py dfs 1,2,5,3,4,0,6,7,8
```

The method argument will be one of the following:

* bfs (Breadth-First Search)
* dfs (Depth-First Search)
* ast (A-Star Search)

### III.Outputs

**Output.txt, containing the following statistics:**

path_to_goal: the sequence of moves taken to reach the goal
cost_of_path: the number of moves taken to reach the goal
nodes_expanded: the number of nodes that have been expanded
search_depth: the depth within the search tree when the goal node is found
max_search_depth: the maximum depth of the search tree in the lifetime of the algorithm
running_time: the total running time of the search instance, reported in seconds
max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the  **ru_maxrss**  attribute in the  **resource**  module, reported in megabytes

```
path_to_goal: ['Up', 'Left', 'Left']
cost_of_path: 3
nodes_expanded: 10
search_depth: 3
max_search_depth: 4
running_time: 0.
max_ram_usage: 0.
```
