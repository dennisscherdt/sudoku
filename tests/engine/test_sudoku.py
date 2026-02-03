import pytest

from engine.sudoku import GRID_SIZE, Cell, Sudoku

# Fixtures


@pytest.fixture
def valid_grid():
    raw = [
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
    return [[Cell(value=v) for v in row] for row in raw]


@pytest.fixture
def invalid_grid(valid_grid):
    grid = [row[:] for row in valid_grid]
    grid[0][8].value = 9  # duplicate in row + subgrid
    return grid


@pytest.fixture
def invalid_grid_bad_row_length():
    sudoku = [[Cell(value=0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    sudoku[0] = [Cell(value=0) for _ in range(GRID_SIZE - 1)]
    return sudoku


# Initialization


def test_sudoku_init_valid_grid(valid_grid):
    sudoku = Sudoku(valid_grid)
    assert sudoku.grid == valid_grid
    assert sudoku.is_valid_board()


def test_sudoku_init_invalid_shape(invalid_grid_bad_row_length):
    with pytest.raises(ValueError, match='9x9'):
        Sudoku(invalid_grid_bad_row_length)


def test_create_empty_grid():
    sudoku = Sudoku.empty()

    assert len(sudoku.grid) == GRID_SIZE
    assert all(len(row) == GRID_SIZE for row in sudoku.grid)
    for row in sudoku.grid:
        for cell in row:
            assert cell.value == 0
            assert cell.conflict_count == 0

    assert sudoku.is_valid_board()


# set_cell validation


@pytest.mark.parametrize('val', [-1, 10, 99])
def test_set_cell_rejects_invalid_value(valid_grid, val):
    sudoku = Sudoku(valid_grid)

    with pytest.raises(ValueError, match='value'):
        sudoku.set_cell(row=0, col=0, val=val)


@pytest.mark.parametrize(
    'row,col',
    [
        (-1, 0),
        (0, -1),
        (9, 0),
        (0, 9),
    ],
)
def test_set_cell_rejects_invalid_coordinates(valid_grid, row, col):
    sudoku = Sudoku(valid_grid)

    with pytest.raises(ValueError, match='coordinates'):
        sudoku.set_cell(row=row, col=col, val=1)


def test_set_cell_same_value_is_noop(valid_grid):
    sudoku = Sudoku(valid_grid)
    original_empty = sudoku.empty_cells

    sudoku.set_cell(row=0, col=0, val=5)

    assert sudoku.grid[0][0].value == 5
    assert sudoku.empty_cells == original_empty
    assert sudoku.is_valid_board()


def test_set_cell_clearing_cell_increments_empty_count(valid_grid):
    sudoku = Sudoku(valid_grid)
    original_empty = sudoku.empty_cells

    sudoku.set_cell(row=0, col=0, val=0)

    assert sudoku.grid[0][0].value == 0
    assert sudoku.empty_cells == original_empty + 1


def test_set_cell_filling_cell_decrements_empty_count(valid_grid):
    sudoku = Sudoku(valid_grid)
    original_empty = sudoku.empty_cells

    sudoku.set_cell(row=0, col=2, val=4)  # was empty

    assert sudoku.grid[0][2].value == 4
    assert sudoku.empty_cells == original_empty - 1


def test_set_cell_updates_value(valid_grid):
    sudoku = Sudoku(valid_grid)
    sudoku.set_cell(val=9, row=4, col=5)

    assert sudoku.grid[4][5].value == 9


# Conflict tracking (incremental engine)


def test_row_conflict_marks_both_cells_invalid(valid_grid):
    sudoku = Sudoku(valid_grid)

    sudoku.set_cell(row=0, col=2, val=5)  # duplicate 5 in row 0

    c1 = sudoku.grid[0][0]
    c2 = sudoku.grid[0][2]

    assert not c1.is_valid
    assert not c2.is_valid
    assert not sudoku.is_valid_board()
    assert sudoku.total_conflicts == 2


def test_conflict_resolves_when_value_removed(valid_grid):
    sudoku = Sudoku(valid_grid)

    sudoku.set_cell(row=0, col=2, val=5)
    sudoku.set_cell(row=0, col=2, val=0)

    assert sudoku.grid[0][0].is_valid
    assert sudoku.is_valid_board()
    assert sudoku.total_conflicts == 0


def test_multiple_conflicts_can_exist_simultaneously(valid_grid):
    sudoku = Sudoku(valid_grid)

    sudoku.set_cell(row=0, col=2, val=5)
    sudoku.set_cell(row=2, col=0, val=6)

    assert sudoku.total_conflicts == 5
    assert not sudoku.is_valid_board()


def test_initial_invalid_grid_seeds_conflicts():
    raw = [
        [5, 5, 0, 0, 0, 0, 0, 0, 0],
        *([[0] * GRID_SIZE] * (GRID_SIZE - 1)),
    ]

    sudoku = Sudoku(raw)

    assert not sudoku.is_valid_board()
    assert sudoku.total_conflicts == 2

    assert sudoku.grid[0][0].conflict_count == 2
    assert sudoku.grid[0][1].conflict_count == 2


# Helpers


@pytest.mark.parametrize(
    'row,col,expected',
    [
        (0, 0, 0),
        (0, 8, 2),
        (4, 4, 4),
        (8, 8, 8),
    ],
)
def test_determine_subgrid(row, col, expected):
    assert Sudoku.determine_subgrid(row, col) == expected
