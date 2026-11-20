import argparse

from board import Board
from game import DotsAndBoxes


def build_parser():
    parser = argparse.ArgumentParser(description="Dots and Boxes")
    parser.add_argument("--rows", type=int, default=2,
                        help=f"boxes per column, {Board.MIN_SIZE}-{Board.MAX_SIZE} (default 2)")
    parser.add_argument("--cols", type=int, default=2,
                        help=f"boxes per row, {Board.MIN_SIZE}-{Board.MAX_SIZE} (default 2)")
    parser.add_argument("--vs-computer", action="store_true",
                        help="play against the computer (you are Player 1)")
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    try:
        game = DotsAndBoxes(args.rows, args.cols, vs_computer=args.vs_computer)
    except ValueError as error:
        parser.error(str(error))
    game.run()
