#!/usr/bin/env python
# coding:utf-8

"""
Usage:
$ python3 driver.py <81-digit-board>
$ python3 driver.py   => this assumes a 'sudokus_start.txt'

Saves output to output.txt
"""

import sys
from heapq import heappush, heappop

ROW = "ABCDEFGHI"
COL = "123456789"
TIME_LIMIT = 1.  # max seconds per board
out_filename = 'output.txt'
src_filename = 'sudokus_start.txt'


def print_board(board):
    """Helper function to print board in a square."""
    print "-----------------"
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print row


def string_to_board(s):
    """
        Helper function to convert a string to board dictionary.
        Scans board L to R, Up to Down.
    """
    return {ROW[r] + COL[c]: int(s[9 * r + c])
            for r in range(9) for c in range(9)}


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def write_solved(board, f_name=out_filename, mode='w+'):
    """
        Solve board and write to desired file, overwriting by default.
        Specify mode='a+' to append.
    """
    result = backtracking(board)
    # print result  # TODO: Comment out prints when timing runs.
    # print

    # Write board to file
    outfile = open(f_name, mode)
    outfile.write(result)
    outfile.write('\n')
    outfile.close()

    return result

def get_arcs(idx):
    arcs = []
    row_num = ord(idx[0])-ord('A')
    col_num = ord(idx[1])-ord('1')
    for i in range(row_num) + range(row_num+1, 9):
        arcs.append(ROW[i]+COL[col_num])
    for i in range(col_num) + range(col_num+1, 9):
        arcs.append(ROW[row_num]+COL[i])
    for i in range(row_num/3*3, row_num) + range(row_num+1, row_num/3*3+3):
        for j in range(col_num/3*3, col_num) + range(col_num+1, col_num/3*3+3):
            arcs.append(ROW[i]+COL[j])
    return arcs


def get_domain(idx):
    d = set([board[i] for i in get_arcs(idx)])
    return set(set(range(1, 10)) - d)


lookup_idx = {}


def create_unassigned_with_domain(board):
    global lookup_idx
    unassigned = []
    domain = {}
    for r in range(9):
        for c in range(9):
            cell = ROW[r] + COL[c]
            if board[cell] == 0:
                domain[cell] = get_domain(cell)
                # print cell, domain[cell]
                newdomain = [len(domain[cell]), cell]
                heappush(unassigned, newdomain)
                lookup_idx[cell] = newdomain
            else:
                domain[cell] = board[cell]

    return unassigned, domain


def forward_checking(idx, value, domain):
    cell_to_change = []
    for cell in get_arcs(idx):
        if domain[cell] is value:
            return False, cell_to_change
        if not isinstance(domain[cell], int):
            if value in domain[cell]:
                if len(domain[cell]) == 1:
                    return False, cell_to_change
                cell_to_change.append(cell)
    return True, cell_to_change


def bt(board, unassigned, domain):
    # print history
    # print_board(board)
    global lookup_idx
    idx = None
    while unassigned:
        num, idx = heappop(unassigned)
        if idx is not None:
            break
    if not unassigned and idx is None:
        lookup_idx = {}
        return board
    d = domain[idx]
    for value in d:
        board[idx] = value
        domain[idx] = value
        judge, cell_to_change = forward_checking(idx, value, domain)
        if judge:
            for i in cell_to_change:
                domain[i].remove(value)
                if i in lookup_idx:
                    lookup_idx[i][1] = None
                newdomain = [len(domain[i]), i]
                heappush(unassigned, newdomain)
                lookup_idx[i] = newdomain
            # if not history:
            #     history = [idx]
            # else:
            #     history.append(idx)
            result = bt(board, unassigned, domain)
            if result:
                return result
            for i in cell_to_change:
                domain[i].add(value)
            board[idx] = 0
        domain[idx] = d
    if idx in lookup_idx:
        lookup_idx[idx][1] = None
    newdomain = [len(domain[idx]), idx]
    heappush(unassigned, newdomain)
    lookup_idx[idx] = newdomain
    # history = history[:-1]

    return False


def backtracking(board):
    global lookup_idx
    unassigned, domain = create_unassigned_with_domain(board)
    board_solved = bt(board, unassigned, domain)
    return board_to_string(board_solved)


if __name__ == '__main__':
    if len(sys.argv) > 1:  # Run a single board, as done during grading
        board = string_to_board(sys.argv[1])
        write_solved(board)

    else:
        print "Running all from sudokus_start"

        #  Read boards from source.
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print "Error reading the sudoku file %s" % src_filename
            exit()

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation
            board = string_to_board(line)
            # print_board(board)  # TODO: Comment this out when timing runs.

            # Append solved board to output.txt
            write_solved(board, mode='a+')

        print "Finished all boards in file."
