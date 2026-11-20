import random
import unittest

from ai import choose_move
from board import Board
from game import DotsAndBoxes
from rules import MoveError, legal_moves, parse_move, valid_move, validate_move


def scripted(moves):
    """Build an input function that feeds the given lines, then hits EOF."""
    feed = iter(moves)

    def _input(_prompt=""):
        try:
            return next(feed)
        except StopIteration:
            raise EOFError

    return _input


def draw_box_zero(game_or_board_play):
    """Helper: three sides of box (0,0); the caller supplies the 4th."""
    for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0)):
        game_or_board_play(*move)


class BoardTests(unittest.TestCase):
    # --- required: valid horizontal / vertical move ------------------- #
    def test_valid_horizontal_move(self):
        board = Board()
        completed = board.add_line("H", 0, 1)
        self.assertTrue(board.horizontal[0][1])
        self.assertEqual(completed, [])

    def test_valid_vertical_move(self):
        board = Board()
        completed = board.add_line("V", 1, 2)
        self.assertTrue(board.vertical[1][2])
        self.assertEqual(completed, [])

    # --- required: invalid / repeated move ---------------------------- #
    def test_repeated_line_rejected_and_state_unchanged(self):
        board = Board()
        board.add_line("H", 0, 0)
        used_before = board.lines_used()
        with self.assertRaises(ValueError):
            board.add_line("H", 0, 0)
        self.assertEqual(board.lines_used(), used_before)

    def test_negative_index_does_not_wrap_around(self):
        # Regression: the starter silently wrote to the last row/column.
        board = Board()
        with self.assertRaises(ValueError):
            board.add_line("H", -1, 0)
        with self.assertRaises(ValueError):
            board.add_line("V", 0, -1)
        self.assertEqual(board.lines_used(), 0)

    def test_unknown_orientation_rejected(self):
        # Regression: the starter treated any non-"H" as vertical.
        board = Board()
        with self.assertRaises(ValueError):
            board.add_line("X", 0, 0)
        self.assertEqual(board.lines_used(), 0)

    def test_out_of_range_rejected(self):
        board = Board()
        for move in (("H", 3, 0), ("H", 0, 2), ("V", 2, 0), ("V", 0, 3)):
            with self.assertRaises(ValueError):
                board.add_line(*move)
        self.assertEqual(board.lines_used(), 0)

    # --- required: completion of a box -------------------------------- #
    def test_completing_a_box_claims_it_for_the_player(self):
        board = Board()
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0)):
            board.add_line(*move, player=0)
        completed = board.add_line("V", 0, 1, player=1)
        self.assertEqual(completed, [(0, 0)])
        self.assertIn((0, 0), board.completed)
        self.assertEqual(board.owners[(0, 0)], 1)

    def test_one_line_can_complete_two_boxes(self):
        board = Board()
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0),
                     ("H", 0, 1), ("H", 1, 1), ("V", 0, 2)):
            board.add_line(*move)
        completed = board.add_line("V", 0, 1)
        self.assertEqual(sorted(completed), [(0, 0), (0, 1)])

    def test_box_is_only_reported_once(self):
        board = Board()
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0), ("V", 0, 1)):
            board.add_line(*move)
        self.assertEqual(board.add_line("H", 2, 0), [])

    # --- required: end of game ---------------------------------------- #
    def test_is_complete_only_when_every_line_drawn(self):
        board = Board()
        moves = legal_moves(board)
        self.assertEqual(len(moves), board.total_lines())
        for move in moves[:-1]:
            board.add_line(*move)
            self.assertFalse(board.is_complete())
        board.add_line(*moves[-1])
        self.assertTrue(board.is_complete())

    def test_non_square_boards(self):
        for rows, cols in ((1, 1), (2, 3), (3, 2), (4, 4)):
            board = Board(rows, cols)
            for move in legal_moves(board):
                board.add_line(*move)
            self.assertTrue(board.is_complete())
            self.assertEqual(len(board.completed), rows * cols)

    def test_bad_board_sizes_rejected(self):
        for rows, cols in ((0, 2), (2, 0), (-1, 2), (10, 2), (2.5, 2), (True, 2)):
            with self.assertRaises(ValueError):
                Board(rows, cols)

    def test_render_shows_owner_and_aligned_dots(self):
        board = Board(1, 1)
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0)):
            board.add_line(*move, player=0)
        board.add_line("V", 0, 1, player=1)
        lines = board.render([0, 1], 0).splitlines()
        self.assertIn("| 2 |", lines)       # box owned by player 2
        self.assertIn(".---.", lines)       # corner dots line up with walls


class ParseAndValidateTests(unittest.TestCase):
    def test_parse_accepts_lowercase_and_extra_spaces(self):
        self.assertEqual(parse_move("  h   0  1 "), ("H", 0, 1))
        self.assertEqual(parse_move("V 2 0"), ("V", 2, 0))

    def test_parse_rejects_malformed_commands(self):
        bad = ["", "H", "H 0", "H 0 1 2", "Z 0 0", "H a 1", "H 1 b",
               "H -1 0", "H 1.5 0", "H 0x1 0"]
        for text in bad:
            with self.assertRaises(MoveError, msg=text):
                parse_move(text)

    def test_parse_rejects_unicode_digits(self):
        # Regression: '²'.isdigit() is True but int('²') raises ValueError.
        for text in ("H ² 1", "V 0 ٣", "H １ 0"):
            with self.assertRaises(MoveError, msg=text):
                parse_move(text)

    def test_parse_rejects_absurdly_long_numbers(self):
        with self.assertRaises(MoveError):
            parse_move("H " + "9" * 5000 + " 0")

    def test_validate_move_messages(self):
        board = Board()
        board.add_line("H", 0, 0)
        with self.assertRaisesRegex(MoveError, "already been drawn"):
            validate_move(board, "H", 0, 0)
        with self.assertRaisesRegex(MoveError, "off the board"):
            validate_move(board, "H", 9, 9)
        self.assertIsNone(validate_move(board, "V", 0, 0))

    def test_valid_move_boolean_wrapper(self):
        board = Board()
        self.assertTrue(valid_move(board, "H", 0, 0))
        board.add_line("H", 0, 0)
        self.assertFalse(valid_move(board, "H", 0, 0))
        self.assertFalse(valid_move(board, "Q", 0, 0))

    def test_no_move_is_valid_after_game_over(self):
        board = Board(1, 1)
        for move in legal_moves(board):
            board.add_line(*move)
        with self.assertRaisesRegex(MoveError, "already over"):
            validate_move(board, "H", 0, 0)
        self.assertFalse(valid_move(board, "H", 0, 0))


class GameTests(unittest.TestCase):
    def setUp(self):
        self.game = DotsAndBoxes(output_fn=lambda *_: None)

    def test_turn_passes_when_no_box_completed(self):
        self.assertEqual(self.game.current, 0)
        self.game.apply_move("H", 0, 0)
        self.assertEqual(self.game.current, 1)
        self.game.apply_move("V", 0, 2)
        self.assertEqual(self.game.current, 0)
        self.assertEqual(self.game.scores, [0, 0])

    def test_completing_a_box_scores_and_keeps_the_turn(self):
        draw_box_zero(self.game.apply_move)          # P1, P2, P1 -> now P2
        self.assertEqual(self.game.current, 1)
        completed = self.game.apply_move("V", 0, 1)  # P2 closes the box
        self.assertEqual(completed, 1)
        self.assertEqual(self.game.scores, [0, 1])
        self.assertEqual(self.game.current, 1)       # extra turn
        self.assertEqual(self.game.board.owners[(0, 0)], 1)

    def test_double_box_scores_two_points(self):
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0),
                     ("H", 0, 1), ("H", 1, 1), ("V", 0, 2)):
            self.game.apply_move(*move)
        player = self.game.current
        self.assertEqual(self.game.apply_move("V", 0, 1), 2)
        self.assertEqual(self.game.scores[player], 2)
        self.assertEqual(self.game.current, player)

    def test_invalid_moves_do_not_change_score_turn_or_board(self):
        self.game.apply_move("H", 0, 0)
        snapshot = (self.game.current, list(self.game.scores),
                    self.game.board.lines_used())
        for move in (("H", 0, 0), ("H", -1, 0), ("V", 9, 9), ("Z", 0, 0)):
            with self.assertRaises(MoveError):
                self.game.apply_move(*move)
        self.assertEqual(
            (self.game.current, self.game.scores, self.game.board.lines_used()),
            snapshot,
        )

    def test_end_of_game_and_move_after_game_over(self):
        for move in legal_moves(self.game.board):
            self.game.apply_move(*move)
        self.assertTrue(self.game.is_over())
        self.assertEqual(sum(self.game.scores), 4)
        before = (self.game.current, list(self.game.scores))
        with self.assertRaises(MoveError):
            self.game.apply_move("H", 0, 0)
        self.assertEqual((self.game.current, self.game.scores), before)

    def test_winner_and_draw(self):
        self.game.scores = [3, 1]
        self.assertEqual(self.game.winner(), 0)
        self.game.scores = [1, 3]
        self.assertEqual(self.game.winner(), 1)
        self.game.scores = [2, 2]
        self.assertIsNone(self.game.winner())


class GameLoopTests(unittest.TestCase):
    def run_game(self, lines, **kwargs):
        out = []
        game = DotsAndBoxes(input_fn=scripted(lines), output_fn=out.append, **kwargs)
        game.run()
        return game, "\n".join(out)

    def test_full_game_ends_in_draw(self):
        lines = ["H 0 0", "H 1 0", "V 0 0", "V 0 1", "H 0 1", "H 1 1", "V 0 2",
                 "H 2 0", "H 2 1", "V 1 0", "V 1 1", "V 1 2"]
        game, text = self.run_game(lines)
        self.assertEqual(game.scores, [1 + 1, 1 + 1])
        self.assertIn("Game over!", text)
        self.assertIn("The game is a draw.", text)

    def test_garbage_input_never_crashes_or_corrupts(self):
        lines = ["", "hello", "H", "H 0", "H x 1", "H -1 0", "H ² 1", "Z 0 0",
                 "H 99 99", "H " + "9" * 5000 + " 0", "help", "H 0 0", "H 0 0"]
        game, text = self.run_game(lines)          # ends via EOF, no exception
        self.assertEqual(game.board.lines_used(), 1)
        self.assertEqual(game.scores, [0, 0])
        self.assertEqual(game.current, 1)
        self.assertIn("already been drawn", text)
        self.assertIn("Commands:", text)

    def test_quit_command_and_eof_exit_cleanly(self):
        game, text = self.run_game(["H 0 0", "quit"])
        self.assertIn("Game abandoned.", text)
        game, text = self.run_game(["H 0 0"])
        self.assertIn("Input closed", text)

    def test_vs_computer_human_then_computer(self):
        game, text = self.run_game(["H 0 0"], vs_computer=True, rng=random.Random(1))
        self.assertIn("Computer (Player 2) plays", text)


class AITests(unittest.TestCase):
    def test_takes_a_box_when_available(self):
        board = Board()
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0)):
            board.add_line(*move)
        self.assertEqual(choose_move(board, random.Random(0)), ("V", 0, 1))

    def test_avoids_giving_away_a_box_when_a_safe_move_exists(self):
        board = Board()
        board.add_line("H", 0, 0)
        board.add_line("H", 1, 0)          # box (0,0) now has 2 sides
        for seed in range(20):
            move = choose_move(board, random.Random(seed))
            for box in board.boxes_touching(*move):
                self.assertLess(board.box_side_count(*box), 2)

    def test_returns_none_when_board_is_full(self):
        board = Board(1, 1)
        for move in legal_moves(board):
            board.add_line(*move)
        self.assertIsNone(choose_move(board))

    def test_computer_vs_computer_finishes_with_all_boxes_scored(self):
        for seed in range(10):
            game = DotsAndBoxes(rows=3, cols=3, output_fn=lambda *_: None)
            rng = random.Random(seed)
            while not game.is_over():
                game.apply_move(*choose_move(game.board, rng))
            self.assertEqual(sum(game.scores), 9)


if __name__ == "__main__":
    unittest.main()
