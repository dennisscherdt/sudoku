import pytest

from engine.generator import Difficulty, Generator
from engine.solver import Solver
from engine.sudoku import GRID_SIZE, Sudoku


@pytest.fixture
def solver():
    return Solver()


@pytest.fixture
def generator(solver):
    return Generator(solver)


def test_generate_returns_valid_board(generator):
    sudoku = generator.generate(Difficulty.MEDIUM)

    assert sudoku.is_valid_board()


def test_generate_creates_empty_cells(generator):
    sudoku = generator.generate(Difficulty.MEDIUM)

    assert sudoku.empty_cells > 0


def test_harder_difficulty_has_more_empty_cells(generator):
    easy = generator.generate(Difficulty.EASY)
    hard = generator.generate(Difficulty.HARD)

    assert hard.empty_cells > easy.empty_cells


def test_generate_grid_shape(generator):
    sudoku = generator.generate(Difficulty.MEDIUM)

    assert len(sudoku.grid) == GRID_SIZE
    assert all(len(row) == GRID_SIZE for row in sudoku.grid)


def test_generate_uses_only_valid_cell_values(generator):
    sudoku = generator.generate(Difficulty.MEDIUM)

    for row in sudoku.grid:
        for cell in row:
            assert 0 <= cell <= 9


def test_generator_does_not_mutate_solver_input(generator):
    original = Sudoku.empty()
    original_empty = original.empty_cells

    generator.generate(Difficulty.MEDIUM)

    assert original.empty_cells == original_empty


@pytest.mark.parametrize(
    'difficulty',
    [
        Difficulty.SUPER_EASY,
        Difficulty.EASY,
        Difficulty.MEDIUM,
        Difficulty.HARD,
        Difficulty.SUPER_HARD,
    ],
)
def test_generate_works_for_all_difficulties(generator, difficulty):
    sudoku = generator.generate(difficulty)

    assert sudoku.is_valid_board()
    assert sudoku.empty_cells > 0
