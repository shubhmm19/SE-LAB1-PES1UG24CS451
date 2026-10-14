"""A simple computer opponent for Dots and Boxes.

Strategy (greedy, no look-ahead):
  1. If any move completes a box, take the one that completes the most boxes.
  2. Otherwise play a "safe" move that does not give the opponent a box
     (i.e. does not create a third side on any box).
  3. If every move is unsafe, give away as little as possible.
"""

import random

from rules import legal_moves


def _boxes_completed_by(board, move):
    orientation, row, col = move
    return sum(
        1 for box in board.boxes_touching(orientation, row, col)
        if board.box_side_count(*box) == 3
    )


def _boxes_given_away_by(board, move):
    orientation, row, col = move
    return sum(
        1 for box in board.boxes_touching(orientation, row, col)
        if board.box_side_count(*box) == 2
    )


def choose_move(board, rng=None):
    """Pick a move for the computer, or None if no line is left."""
    rng = rng or random
    moves = legal_moves(board)
    if not moves:
        return None

    best_gain = max(_boxes_completed_by(board, m) for m in moves)
    if best_gain > 0:
        return rng.choice([m for m in moves if _boxes_completed_by(board, m) == best_gain])

    least_loss = min(_boxes_given_away_by(board, m) for m in moves)
    return rng.choice([m for m in moves if _boxes_given_away_by(board, m) == least_loss])
