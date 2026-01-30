import pytest

from engine.solver import Solver
from engine.sudoku import GRID_SIZE, Sudoku

PARTIAL_GRID = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

UNSOLVABLE_GRID = [
    [5, 5, 0, 0, 7, 0, 0, 0, 0],  # duplicate 5 in row
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

INVALID_GRID = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]


def assert_clues_preserved(original: Sudoku, solved: Sudoku) -> None:
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = original.grid[r][c]
            if val != 0:
                assert solved.grid[r][c] == val


def test_solve_solves_empty_board():
    original = Sudoku.empty()

    solved = Solver.solve(original)
    print(solved.__str__())
    assert solved is not None
    assert solved.is_valid_board()
    assert solved.empty_cells == 0


def test_solve_does_not_mutate_original():
    original = Sudoku.empty()

    Solver.solve(original)

    assert original.empty_cells == GRID_SIZE * GRID_SIZE


def test_solve_respects_existing_values():
    original = Sudoku(PARTIAL_GRID)

    solved = Solver.solve(original)

    assert solved is not None
    assert solved.is_valid_board()
    assert solved.empty_cells == 0
    assert_clues_preserved(original, solved)


def test_solve_returns_none_on_unsolvable_board():
    sudoku = Sudoku(UNSOLVABLE_GRID)

    assert Solver.solve(sudoku) is None


def test_solve_rejects_invalid_board():
    with pytest.raises(ValueError, match='9x9'):
        Sudoku(INVALID_GRID)
