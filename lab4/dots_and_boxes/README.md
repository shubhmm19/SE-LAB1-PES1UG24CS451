# Scenario 23 — Dots and Boxes

A turn-based grid game. Players take turns drawing one line between adjacent
dots. Completing the fourth side of a box claims it, scores a point and gives
the same player another turn. The player with more boxes when every line is
drawn wins.

The project keeps the original modular structure:

| Module | Responsibility |
|---|---|
| `board.py` | Board state: lines, claimed boxes and their owners, rendering. Rejects invalid lines itself. |
| `rules.py` | Side-effect-free rules: parsing typed commands, move validation, legal-move listing. |
| `game.py` | Game flow: turns, scores, winner, interactive loop. |
| `ai.py` | **New.** Computer opponent. |
| `main.py` | Entry point and command-line options only. |
| `tests/test_game.py` | **New.** 34 automated tests (standard library `unittest`). |

## How to run

```
python main.py                      # two humans, 2x2 board (original behaviour)
python main.py --rows 3 --cols 4    # custom board size (1-9 each)
python main.py --vs-computer        # you are Player 1, computer is Player 2
python main.py --rows 3 --cols 3 --vs-computer
```

Enter moves as `H row col` or `V row col` (case-insensitive, rows and columns
start at 0). Other commands: `help`, `quit`.

```
.---.---.
| 2 | 1 |      <- digit = which player owns the box
.---.---.
|       |
.---.---.
```

## How to run the tests

```
python -m unittest discover -v
```

Python 3.10+; no third-party packages.

---

## Task 1 — Investigation and fixes

I ran many games, deliberately completing single boxes, two boxes with one
line, and boxes on the last move, and traced the score/turn flow through
`board.py`, `rules.py` and `game.py`.

**Scoring and turn order after a box is completed behaved correctly** in the
starter (score increases by the number of boxes completed, and the same player
moves again). I kept that behaviour and locked it in with regression tests.

The investigation did expose these genuine defects, all fixed:

| # | Defect in the starter | Effect | Fix |
|---|---|---|---|
| 1 | Claimed boxes were stored as an anonymous set and drawn as `X` | You could not tell which player owned a box, so the board could not be checked against the score | `Board.owners` records the owning player; the box shows `1` or `2` |
| 2 | `isdigit()` accepts characters such as `²` that `int()` rejects | Typing `H ² 1` crashed with a `ValueError` traceback | Only ASCII digits are accepted (`rules.parse_move`) |
| 3 | `Ctrl-D` / `Ctrl-C` at the prompt | Crashed with a traceback | Caught; the game exits cleanly. Added a `quit` command |
| 4 | Board drawing had no corner dots, so `.` characters sat between segments while `\|` walls were offset | Lines and walls did not line up | Rows now render as `.---.---.` so dots and walls align |
| 5 | `Board.add_line` did no checking of its own | `add_line("H", -1, 0)` silently wrote to the **last** row (Python negative indexing); any orientation other than `"H"` silently drew a vertical line | `add_line` validates the line and raises `ValueError` without touching the board |

## Task 2 — New gameplay features

Added across `board.py`, `rules.py`, `game.py`, `ai.py` and `main.py`:

1. **Play against the computer** (`--vs-computer`). New module `ai.py`: take a
   box if one is available (preferring moves that complete the most); otherwise
   avoid drawing a third side on any box; otherwise give away as little as
   possible. It plays through the same `apply_move` path as a human, so it
   obeys the same rules, extra-turn behaviour and scoring.
2. **Configurable board size** (`--rows`, `--cols`, 1–9). `Board` was already
   parameterised, but the game always created a 2×2 board. The end-of-game
   check, validation and rendering were verified for non-square boards.
3. **Box ownership tracking and display** (see defect 1) — used by the display,
   the AI and the tests.

## Task 3 — Validation and robustness

All handled without changing board state, score or turn:

- **Malformed commands** — wrong number of tokens, unknown orientation,
  non-numeric / negative / decimal / Unicode digits, absurdly long numbers
  (also avoids Python's int-conversion limit on huge digit strings).
- **Invalid coordinates** — the message states the legal range for that
  orientation.
- **Repeated lines** — "That line has already been drawn."
- **Moves after the board is complete** — rejected with "The game is already
  over". The main loop also stops once the board is full.
- **Closed input** — `EOF` / `Ctrl-C` end the game cleanly.
- **Bad command-line options** — sizes outside 1–9 produce a normal usage error.

Validation exists at two levels (defence in depth): `rules.validate_move`
gives the user a specific message, and `Board.add_line` independently refuses
bad lines, so no caller can corrupt the board.

## Task 4 — Testing

34 tests in `tests/test_game.py`, including the required five:

| Required case | Test(s) |
|---|---|
| Valid horizontal move | `test_valid_horizontal_move` |
| Valid vertical move | `test_valid_vertical_move` |
| Invalid / repeated move | `test_repeated_line_rejected_and_state_unchanged`, `test_out_of_range_rejected`, `test_invalid_moves_do_not_change_score_turn_or_board` |
| Completion of a box | `test_completing_a_box_claims_it_for_the_player`, `test_completing_a_box_scores_and_keeps_the_turn`, `test_double_box_scores_two_points` |
| End-of-game condition | `test_is_complete_only_when_every_line_drawn`, `test_end_of_game_and_move_after_game_over`, `test_full_game_ends_in_draw` |

Plus regression tests for each defect above, parser tests, game-loop tests
using scripted input, AI tests, and a simulation of ten computer-vs-computer
3×3 games checking that all 9 boxes are always scored.

## Design decisions

- **Game rules separated from I/O.** `DotsAndBoxes.apply_move` contains the
  turn and score logic and does no printing or reading; `run()` only handles
  I/O. This is what makes the rules directly testable. `input`/`print` are
  injectable for the same reason.
- **Errors by exception, not return codes.** `MoveError` carries a
  human-readable reason from `rules.py` to the loop. `valid_move` was kept as a
  boolean wrapper so the original API still works.
- **`Board.add_line` returns the boxes it completed**, replacing the
  before/after set-snapshot diff in `game.py`. `rules.completed_boxes` is kept
  for compatibility.
- **Preserved gameplay.** Defaults are the original: 2×2, two humans, same
  commands, same messages for completing a box. New behaviour is opt-in via
  flags.
- **No new logic in `main.py`.** It only parses options and starts the game.
- **No third-party dependencies.** Standard library only.
- **Simple AI on purpose.** It has no look-ahead (no chain/sacrifice
  analysis), which keeps it small, deterministic when seeded, and testable.
