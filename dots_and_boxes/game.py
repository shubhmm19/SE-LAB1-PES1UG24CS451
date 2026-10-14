"""Game flow: turns, scores and the interactive loop."""

from ai import choose_move
from board import Board
from rules import MoveError, parse_move, validate_move

HELP_TEXT = (
    "Commands:\n"
    "  H row col   draw a horizontal line (row 0..rows, col 0..cols-1)\n"
    "  V row col   draw a vertical line   (row 0..rows-1, col 0..cols)\n"
    "  help        show this message\n"
    "  quit        leave the game\n"
    "Rows and columns start at 0. Completing a box scores a point and "
    "gives you another turn."
)


class DotsAndBoxes:
    def __init__(self, rows=2, cols=2, vs_computer=False,
                 input_fn=input, output_fn=print, rng=None):
        self.board = Board(rows, cols)
        self.current = 0
        self.scores = [0, 0]
        self.vs_computer = vs_computer
        self.computer_player = 1 if vs_computer else None
        self.input = input_fn
        self.output = output_fn
        self.rng = rng

    # ------------------------------------------------------------------ #
    # Core rules (no input/output - easy to test)
    # ------------------------------------------------------------------ #
    def is_over(self):
        return self.board.is_complete()

    def apply_move(self, orientation, row, col):
        """Play a move for the current player; return boxes completed.

        Raises MoveError (changing nothing) if the move is not legal.
        A player who completes at least one box scores and moves again;
        otherwise the turn passes to the other player.
        """
        validate_move(self.board, orientation, row, col)
        newly = self.board.add_line(orientation, row, col, self.current)
        if newly:
            self.scores[self.current] += len(newly)
        else:
            self.current = 1 - self.current
        return len(newly)

    def winner(self):
        """0 or 1 for the winning player index, None for a draw."""
        if self.scores[0] == self.scores[1]:
            return None
        return 0 if self.scores[0] > self.scores[1] else 1

    # ------------------------------------------------------------------ #
    # Interactive loop
    # ------------------------------------------------------------------ #
    def _announce(self, player, count):
        if count:
            self.output(f"Player {player + 1} completed {count} box(es) and plays again.")

    def _computer_turn(self):
        move = choose_move(self.board, self.rng)
        if move is None:
            return
        player = self.current
        self.output(f"Computer (Player {player + 1}) plays {move[0]} {move[1]} {move[2]}")
        self._announce(player, self.apply_move(*move))

    def _human_turn(self):
        """Handle one line of input. Returns False if the player quit."""
        try:
            raw = self.input(f"Player {self.current + 1}, move: ")
        except (EOFError, KeyboardInterrupt):
            self.output("\nInput closed - leaving the game.")
            return False

        command = raw.strip().lower()
        if command in ("quit", "q", "exit"):
            self.output("Game abandoned.")
            return False
        if command in ("help", "?"):
            self.output(HELP_TEXT)
            return True

        try:
            orientation, row, col = parse_move(raw)
            player = self.current
            self._announce(player, self.apply_move(orientation, row, col))
        except MoveError as error:
            self.output(str(error))
        return True

    def run(self):
        self.output("Dots and Boxes")
        self.output("Enter moves as H row col or V row col.")
        self.output("Rows and columns start at 0.")
        self.output("Example: H 0 1   (type 'help' for more, 'quit' to leave)")
        if self.vs_computer:
            self.output("You are Player 1. The computer is Player 2.")

        while not self.is_over():
            self.output(self.board.render(self.scores, self.current))
            if self.current == self.computer_player:
                self._computer_turn()
            elif not self._human_turn():
                return

        self.output(self.board.render(self.scores, self.current))
        self.output("Game over!")
        winner = self.winner()
        if winner is None:
            self.output("The game is a draw.")
        else:
            self.output(f"Player {winner + 1} wins!")
