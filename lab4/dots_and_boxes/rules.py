"""Rule checks and input parsing for Dots and Boxes.

Everything here is side-effect free: it inspects a Board but never changes it.
"""


class MoveError(ValueError):
    """Raised when a typed command or a move is not acceptable."""


MAX_COORD_DIGITS = 6  # guards int() against absurdly long digit strings


def parse_move(raw):
    """Turn text such as 'h 0 1' into ('H', 0, 1).

    Raises MoveError for anything malformed.  Only plain ASCII digits are
    accepted: str.isdigit() also accepts characters like '²' that int()
    cannot convert, which used to crash the game.
    """
    parts = raw.strip().upper().split()
    if len(parts) != 3:
        raise MoveError("Invalid format. Type H row col or V row col, e.g. H 0 1.")

    orientation, row, col = parts
    if orientation not in ("H", "V"):
        raise MoveError("Orientation must be H (horizontal) or V (vertical).")

    for value in (row, col):
        if not (value.isascii() and value.isdigit()):
            raise MoveError("Row and column must be non-negative whole numbers.")
        if len(value) > MAX_COORD_DIGITS:
            raise MoveError("Row or column is out of range for this board.")

    return orientation, int(row), int(col)


def validate_move(board, orientation, row, col):
    """Return None if the move is legal, otherwise raise MoveError."""
    if board.is_complete():
        raise MoveError("The game is already over - no more moves can be made.")
    if not board.is_valid_line(orientation, row, col):
        if orientation == "H":
            limits = f"row 0-{board.rows}, col 0-{board.cols - 1}"
        else:
            limits = f"row 0-{board.rows - 1}, col 0-{board.cols}"
        raise MoveError(f"That line is off the board. For {orientation}: {limits}.")
    if board.has_line(orientation, row, col):
        raise MoveError("That line has already been drawn.")


def valid_move(board, orientation, row, col):
    """Boolean form of validate_move (kept from the original starter code)."""
    try:
        validate_move(board, orientation, row, col)
    except MoveError:
        return False
    return True


def completed_boxes(board, before):
    """Number of boxes completed since the `before` snapshot."""
    return len(board.completed - before)


def legal_moves(board):
    """All lines that can still be drawn, in a stable order."""
    moves = []
    for r in range(board.rows + 1):
        for c in range(board.cols):
            if not board.horizontal[r][c]:
                moves.append(("H", r, c))
    for r in range(board.rows):
        for c in range(board.cols + 1):
            if not board.vertical[r][c]:
                moves.append(("V", r, c))
    return moves
