from copy import deepcopy
from dataclasses import dataclass
from typing import Annotated

GRID_SIZE = 9


@dataclass
class Cell:
    value: int = 0  # 0 means empty
    conflict_count: int = 0

    @property
    def is_valid(self) -> bool:
        return self.conflict_count == 0


SudokuGrid = Annotated[list[list[Cell]], '9x9 grid']


class Sudoku:
    def __init__(self, grid: list[list[int]] | SudokuGrid):
        if len(grid) != GRID_SIZE or any(len(row) != GRID_SIZE for row in grid):
            raise ValueError('Sudoku grid must be 9x9')

        # Normalize input so internal state always uses Cell
        self.grid: SudokuGrid = [
            [cell if isinstance(cell, Cell) else Cell(cell) for cell in row] for row in grid
        ]

    @property
    def empty_cells(self) -> int:
        return sum(cell.value == 0 for row in self.grid for cell in row)

    @classmethod
    def empty(cls) -> Sudoku:
        return cls([[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])

    @staticmethod
    def determine_subgrid(row: int, col: int) -> int:
        return (row // 3) * 3 + (col // 3)

    def set_cell(self, row: int, col: int, val: int) -> None:
        if not (0 <= val <= GRID_SIZE):
            raise ValueError('Invalid cell value')

        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            raise ValueError('Invalid cell coordinates')

        self.grid[row][col].value = val

    def is_valid_board(self) -> bool:
        rows: list[set[int]] = [set() for _ in range(GRID_SIZE)]
        cols: list[set[int]] = [set() for _ in range(GRID_SIZE)]
        subgrids: list[set[int]] = [set() for _ in range(GRID_SIZE)]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                value = cell.value
                subgrid_i = self.determine_subgrid(row, col)

                if value == 0:
                    continue

                if value in rows[row] or value in cols[col] or value in subgrids[subgrid_i]:
                    return False

                rows[row].add(value)
                cols[col].add(value)
                subgrids[subgrid_i].add(value)

        return True

    def copy(self) -> Sudoku:
        return Sudoku(deepcopy(self.grid))

    def __str__(self) -> str:
        return '\n'.join(' '.join(str(cell.value) for cell in row) for row in self.grid)
