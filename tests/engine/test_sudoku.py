import pytest

from engine.sudoku import GRID_SIZE, Sudoku


@pytest.fixture
def valid_grid():
    return [
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


@pytest.fixture
def invalid_grid(valid_grid):
    grid = [row[:] for row in valid_grid]
    grid[0][8] = 9
    return grid


@pytest.fixture
def invalid_grid_bad_row_length():
    sudoku = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    sudoku[0] = [0] * 8
    return sudoku


# initialization


def test_sudoku_init_valid_grid(valid_grid):
    sudoku = Sudoku(valid_grid)
    assert sudoku.grid == valid_grid


def test_sudoku_init_invalid(invalid_grid_bad_row_length):
    with pytest.raises(ValueError, match='9x9'):
        Sudoku(invalid_grid_bad_row_length)


def test_create_empty_grid():
    sudoku = Sudoku.empty()

    assert len(sudoku.grid) == GRID_SIZE
    assert all(len(row) == GRID_SIZE for row in sudoku.grid)
    for row in sudoku.grid:
        assert all(cell == 0 for cell in row)


# set_cell


@pytest.mark.parametrize('val', [-1, 10, 99])
def test_set_cell_rejects_invalid_value(valid_grid, val):
    sudoku = Sudoku(valid_grid)

    with pytest.raises(ValueError, match='cell'):
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

    assert sudoku.grid[0][0] == 5
    assert sudoku.empty_cells == original_empty


def test_set_cell_clearing_cell_decrements_empty_count(valid_grid):
    sudoku = Sudoku(valid_grid)
    original_empty = sudoku.empty_cells

    sudoku.set_cell(row=0, col=0, val=0)

    assert sudoku.grid[0][0] == 0
    assert sudoku.empty_cells == original_empty + 1


def test_set_cell_filling_cell_increments_empty_count(valid_grid):
    sudoku = Sudoku(valid_grid)
    original_empty = sudoku.empty_cells

    sudoku.set_cell(row=0, col=2, val=4)  # was empty

    assert sudoku.grid[0][2] == 4
    assert sudoku.empty_cells == original_empty - 1


def test_set_cell(valid_grid):
    sudoku = Sudoku(valid_grid)
    sudoku.set_cell(val=9, row=4, col=5)
    assert sudoku.grid[4][5] == 9


# helpers / validation


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


@pytest.mark.parametrize(
    'grid,expected',
    [
        pytest.param('valid_grid', True, id='valid'),
        pytest.param('invalid_grid', False, id='invalid'),
    ],
)
def test_is_valid_board(grid, expected, request):
    sudoku = Sudoku(request.getfixturevalue(grid))
    assert sudoku.is_valid_board() is expected
