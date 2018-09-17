import time
import Grid
import math
from BaseAI import BaseAI
INF = float('inf')
NUM_SET = (2, 4)
TIME_LIMIT = 0.2
MAX_DEPTH = 150

class PlayerAI(BaseAI):
    def __init__(self):
        self.start_time, self.max_depth, self.timeout = 0.0, 0, False
    def children(self,grid):
        vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)
        children = []
        for x in vecIndex:
            gridCopy = grid.clone()
            if gridCopy.move(x):
                children.append((x, gridCopy))
        return children
    def heuristic(self,grid):#maxcell+average+freetiles+smoothness+monotonicity
        MAX_WEIGHT=1.0
        AVERAGE_WEIGHT=1.0
        FREETILES_WEIGHT=1.0
        SMOOTHNESS_WEIGHT=1.0
        MONOTONICITY_WEIGHT = 0.5
        SIZE = 4
        maxc,avec,numb,smoothness = 0,0,0,0
        monotonicityrow = [0]*SIZE
        monotonicitycol = [0]*SIZE
        varow,varcol = 0,0
        for i in range(SIZE):
            for j in range(SIZE):
                cell = grid.map[i][j]
                avec += cell
                if cell == 0:
                    numb += 1
                elif cell > maxc:
                    maxc = cell
                if j > 0:
                    varow = cell - grid.map[i][j-1]
                    if varow == 0:
                        smoothness += 1
                    elif varow > 0:
                        varow = math.log(abs(varow), 2)
                        monotonicityrow[i-1] += 1
                        smoothness -= varow
                    else:
                        varow = -math.log(abs(varow), 2)
                        monotonicityrow[i-1] += -1
                        smoothness += varow
                if i > 0:
                    varcol = cell - grid.map[i-1][j]
                    if varcol == 0:
                        smoothness += 1
                    elif varcol > 0:
                        varcol = math.log(abs(varcol), 2)
                        monotonicitycol[j-1] += varcol
                        smoothness -= varcol
                    else:
                        varcol = math.log(abs(varcol), 2)
                        monotonicitycol[j-1] -= varcol
                        smoothness -= varcol
        
        maxc = math.log(maxc,2)
        avec = math.log(float(avec) / (SIZE**2 - numb), 2)
        monotonicity = sum(map(abs, monotonicityrow)) + sum(map(abs, monotonicitycol))
        #assign weight
        heuristic =  MAX_WEIGHT * maxc + AVERAGE_WEIGHT * avec + FREETILES_WEIGHT * numb \
            + SMOOTHNESS_WEIGHT * smoothness + MONOTONICITY_WEIGHT * monotonicity
        return heuristic
    def getMove(self,grid):
        self.start_time = time.clock()
        best_move = None
        for self.depth_limit in range(MAX_DEPTH):
            tmp_best = self.maximize(grid, -INF, INF, self.depth_limit)[0]
            if time.clock() - self.start_time > TIME_LIMIT:
                break
            best_move = tmp_best if tmp_best is not None else best_move
        return best_move
    def maximize(self, grid, alpha, beta, depth):
        if time.clock() - self.start_time > TIME_LIMIT:
            return None, -INF
        if depth < 0:
            return None, self.heuristic(grid)

        best_move, max_utility = None, -INF
        for move, child in self.children(grid):
            utility = self.chance(child, alpha, beta, depth - 1)
            if utility > max_utility:
                max_utility = utility
                best_move = move
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility

        return best_move, max_utility
    def chance(self, grid, alpha, beta, depth):
        if time.clock() - self.start_time > TIME_LIMIT:
            return -INF
        if depth < 0:
            return self.heuristic(grid)
        return 0.9*self.minimize(grid,alpha,beta,depth-1,2)+0.1*self.minimize(grid,alpha,beta,depth-1,4)
    def minimize(self, grid, alpha, beta,depth,value):
        if time.clock() - self.start_time > TIME_LIMIT:
            return -INF
        min_utility = INF
        if depth < 0:
            return self.heuristic(grid)
        for cell in grid.getAvailableCells():
            child = grid.clone()
            child.setCellValue(cell, value)
            move, utility = self.maximize(child, alpha,beta, depth - 1)
            if utility < min_utility:
                min_utility = utility
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility
        return min_utility

