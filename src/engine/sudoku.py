from typing import Annotated

SudokuGrid = Annotated[list[list[int]], '9x9 grid']

GRID_SIZE = 9


class Sudoku:
    def __init__(self, grid: SudokuGrid):
        if len(grid) != 9 or any(len(row) != 9 for row in grid):
            raise ValueError('Sudoku grid must be 9x9')
        self.grid = grid
        self.empty_cells = sum(cell == 0 for row in grid for cell in row)

    @classmethod
    def empty(cls) -> Sudoku:
        return cls([[0] * GRID_SIZE for _ in range(9)])

    @staticmethod
    def determine_subgrid(row: int, col: int):
        return (row // 3) * 3 + (col // 3)

    def set_cell(self, row: int, col: int, val: int):
        if not (0 <= val <= GRID_SIZE):
            raise ValueError('Invalid cell input')

        if not (0 <= row <= GRID_SIZE - 1 and 0 <= col <= GRID_SIZE - 1):
            raise ValueError('Invalid cell coordinates')

        cur_val = self.grid[row][col]

        if cur_val == val:
            return

        if cur_val == 0 and val > 0:
            self.empty_cells -= 1
        elif cur_val > 0 and val == 0:
            self.empty_cells += 1

        self.grid[row][col] = val

    def is_valid_board(self):
        rows: list[set[int]] = [set() for _ in range(GRID_SIZE)]
        cols: list[set[int]] = [set() for _ in range(GRID_SIZE)]
        subgrids: list[set[int]] = [set() for _ in range(GRID_SIZE)]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                subgrid_i = self.determine_subgrid(row, col)

                if cell == 0:
                    continue

                if cell in rows[row] or cell in cols[col] or cell in subgrids[subgrid_i]:
                    return False

                rows[row].add(cell)
                cols[col].add(cell)
                subgrids[subgrid_i].add(cell)

        return True
