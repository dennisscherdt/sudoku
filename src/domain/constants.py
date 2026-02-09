from enum import IntEnum

GRID_SIZE = 9
SUBGRID_SIZE = 3


class Difficulty(IntEnum):
    """Values define the number of given cells in the puzzle."""

    SUPER_EASY = 50
    EASY = 40
    MEDIUM = 30
    HARD = 20
    SUPER_HARD = 10
