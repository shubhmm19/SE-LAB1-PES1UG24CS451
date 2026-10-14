"""Board state for Dots and Boxes.

The board knows which lines are drawn and which boxes are claimed (and by
whom).  It does NOT know about turns or scores - that lives in game.py - but
it defends its own state: invalid lines are rejected instead of silently
wrapping around or overwriting something.
"""


class Board:
    MIN_SIZE = 1
    MAX_SIZE = 9

    def __init__(self, rows=2, cols=2):
        for name, value in (("rows", rows), ("cols", cols)):
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or not self.MIN_SIZE <= value <= self.MAX_SIZE
            ):
                raise ValueError(
                    f"{name} must be a whole number between "
                    f"{self.MIN_SIZE} and {self.MAX_SIZE}."
                )
        self.rows = rows
        self.cols = cols
        # horizontal[r][c]: line above box (r, c) / below box (r - 1, c)
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        # vertical[r][c]: line left of box (r, c) / right of box (r, c - 1)
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        self.completed = set()  # {(row, col), ...} of claimed boxes
        self.owners = {}        # {(row, col): player index or None}

    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #
    def is_valid_line(self, orientation, row, col):
        """True if (orientation, row, col) is a line that exists on this board."""
        if orientation not in ("H", "V"):
            return False
        for value in (row, col):
            if isinstance(value, bool) or not isinstance(value, int):
                return False
        if orientation == "H":
            return 0 <= row <= self.rows and 0 <= col < self.cols
        return 0 <= row < self.rows and 0 <= col <= self.cols

    def has_line(self, orientation, row, col):
        """True if the line is already drawn. Line must be valid."""
        grid = self.horizontal if orientation == "H" else self.vertical
        return grid[row][col]

    def box_side_count(self, row, col):
        """How many of the four sides of box (row, col) are drawn."""
        return (
            self.horizontal[row][col]
            + self.horizontal[row + 1][col]
            + self.vertical[row][col]
            + self.vertical[row][col + 1]
        )

    def boxes_touching(self, orientation, row, col):
        """Boxes that have the given line as one of their sides (1 or 2)."""
        if orientation == "H":
            candidates = [(row - 1, col), (row, col)]
        else:
            candidates = [(row, col - 1), (row, col)]
        return [
            (r, c)
            for r, c in candidates
            if 0 <= r < self.rows and 0 <= c < self.cols
        ]

    def total_lines(self):
        return (self.rows + 1) * self.cols + self.rows * (self.cols + 1)

    def lines_used(self):
        return sum(map(sum, self.horizontal)) + sum(map(sum, self.vertical))

    def is_complete(self):
        """The game is over once every line has been drawn."""
        return self.lines_used() == self.total_lines()

    # ------------------------------------------------------------------ #
    # Mutation
    # ------------------------------------------------------------------ #
    def add_line(self, orientation, row, col, player=None):
        """Draw a line and return the list of boxes it completed.

        Raises ValueError (leaving the board untouched) if the line does not
        exist on this board or is already drawn.
        """
        if not self.is_valid_line(orientation, row, col):
            raise ValueError(f"No such line: {orientation} {row} {col}.")
        if self.has_line(orientation, row, col):
            raise ValueError(f"Line {orientation} {row} {col} is already drawn.")

        grid = self.horizontal if orientation == "H" else self.vertical
        grid[row][col] = True
        return self._update_completed(player)

    def _update_completed(self, player):
        newly = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.completed and self.box_side_count(r, c) == 4:
                    self.completed.add((r, c))
                    self.owners[(r, c)] = player
                    newly.append((r, c))
        return newly

    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def _box_label(self, r, c):
        if (r, c) not in self.completed:
            return " "
        owner = self.owners.get((r, c))
        return "X" if owner is None else str(owner + 1)

    def render(self, scores, current):
        lines = ["", f"Scores: P1={scores[0]}  P2={scores[1]} | Turn: P{current + 1}"]
        for r in range(self.rows + 1):
            dots = "."
            for c in range(self.cols):
                dots += ("---" if self.horizontal[r][c] else "   ") + "."
            lines.append(dots)
            if r < self.rows:
                middle = ""
                for c in range(self.cols + 1):
                    middle += "|" if self.vertical[r][c] else " "
                    if c < self.cols:
                        middle += " " + self._box_label(r, c) + " "
                lines.append(middle)
        lines.append("")
        return "\n".join(lines)

    def display(self, scores, current):
        print(self.render(scores, current))
