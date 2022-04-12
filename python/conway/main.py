#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


LIVE_CELL = '🔲'
DEAD_CELL = ' '


def update_cell(board, row, col):
    # Count the neighbors
    neighbor_count = 0

    for row_offset in (-1, 0, 1):
        for col_offset in (-1, 0, 1):
            if row_offset == 0 and col_offset == 0:
                continue

            new_row = row + row_offset
            if new_row < 0 or new_row >= len(board):
                continue

            # We assume here that every row has the same length, and that
            # this condition is validated by the calling function.
            new_col = col + col_offset
            if new_col < 0 or new_col >= len(board[0]):
                continue

            if board[new_row][new_col] == LIVE_CELL:
                neighbor_count += 1
            elif board[new_row][new_col] != DEAD_CELL:
                raise ValueError('invalid cell value')

    if board[row][col] == LIVE_CELL:
        # Not overpopulation or underpopulation
        if not (neighbor_count <= 1 or neighbor_count >= 4):
            return LIVE_CELL
    elif neighbor_count == 3:
        # Reproduction
        return LIVE_CELL

    return DEAD_CELL


def update_state(board):
    # Maintain the previous row to be updated.
    previous_row = None

    for row in range(len(board)):
        current_row = []

        # Write our updates into the temporary row.
        for col in range(len(board[0])):
            current_row.append(update_cell(board, row, col))

        # If the previous row was updated, swap it into the board.
        if previous_row:
            board[row - 1] = previous_row

        # Record our writes for this row for writing and
        # replacement in the next iteration.
        previous_row = current_row

    # Don't forget to update the last row! This is a very common mistake.
    if len(board) > 1:
        board[-1] = previous_row

    return board


def main():
    """
    Main function
    """


if __name__ == '__main__':
    main()
