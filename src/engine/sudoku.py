from collections import defaultdict
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

type RowIndex = int
type ColIndex = int
type Value = int

type CellCoord = tuple[RowIndex, ColIndex]

type CellSetMap = defaultdict[Value, set[CellCoord]]


class Sudoku:
    def __init__(self, grid: list[list[int]] | SudokuGrid):
        if len(grid) != GRID_SIZE or any(len(row) != GRID_SIZE for row in grid):
            raise ValueError('Sudoku grid must be 9x9')

        # Normalize input so internal state always uses Cell
        self.grid: SudokuGrid = [
            [cell if isinstance(cell, Cell) else Cell(cell) for cell in row] for row in grid
        ]

        # For each row, column, and subgrid, map a number (1–9) to the set of
        # cell coordinates (row, col) that currently contain that number.
        # These maps are used to detect duplicate values and update conflict
        # state incrementally when cells change.
        self.rows: list[CellSetMap] = [defaultdict(set) for _ in range(GRID_SIZE)]
        self.cols: list[CellSetMap] = [defaultdict(set) for _ in range(GRID_SIZE)]
        self.subgrids: list[CellSetMap] = [defaultdict(set) for _ in range(GRID_SIZE)]

        self.total_conflicts = 0

        # Seed board state
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                value = cell.value

                if value == 0:
                    continue

                coordinates = (row, col)
                subgrid = self.determine_subgrid(row, col)

                self._add_to_group(self.rows, row, value, coordinates, cell)
                self._add_to_group(self.cols, col, value, coordinates, cell)
                self._add_to_group(self.subgrids, subgrid, value, coordinates, cell)

    @property
    def empty_cells(self) -> int:
        return sum(cell.value == 0 for row in self.grid for cell in row)

    @classmethod
    def empty(cls) -> Sudoku:
        return cls([[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])

    @staticmethod
    def determine_subgrid(row: int, col: int) -> int:
        return (row // 3) * 3 + (col // 3)

    def _remove_from_group(
        self,
        group: list[CellSetMap],
        index: int,
        value: int,
        coordinates: CellCoord,
    ) -> None:
        """
        Remove a cell from a row/column/subgrid group for a given value and
        update conflict state incrementally.

        This method assumes that the cell at `coordinates` currently contains
        `value` and has already been registered in the given group.
        """
        cells = group[index][value]
        prev_size = len(cells)

        cells.remove(coordinates)

        # If moving from 2 -> 1 we are resolving an existing conflict
        if prev_size == 2:
            other = next(iter(cells))
            other_cell = self.grid[other[0]][other[1]]
            other_cell.conflict_count -= 1
            self.total_conflicts -= 1

        if not cells:
            del group[index][value]

    def _add_to_group(
        self,
        group: list[CellSetMap],
        index: int,
        value: int,
        coordinates: CellCoord,
        cell: Cell,
    ) -> None:
        """
        Add a cell to a row/column/subgrid group for a given value and
        update conflict state incrementally.

        This method registers the cell at `coordinates` as containing `value`
        within the specified group. It assumes the cell was not previously
        present in the group for this value.
        """
        cells = group[index][value]
        prev_size = len(cells)

        cells.add(coordinates)

        # 1 -> 2 a new conflict is introduced
        if prev_size == 1:
            other = next(iter(cells - {coordinates}))
            other_cell = self.grid[other[0]][other[1]]
            other_cell.conflict_count += 1
            cell.conflict_count += 1
            self.total_conflicts += 1

        elif prev_size >= 2:
            cell.conflict_count += 1

    def set_cell(self, row: int, col: int, val: int) -> None:
        if not (0 <= val <= GRID_SIZE):
            raise ValueError('Invalid cell value')

        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            raise ValueError('Invalid cell coordinates')

        cell = self.grid[row][col]
        old_val = cell.value

        if old_val == val:
            return

        subgrid = self.determine_subgrid(row, col)
        coordinates = (row, col)

        if old_val != 0:
            self._remove_from_group(self.rows, row, old_val, coordinates)
            self._remove_from_group(self.cols, col, old_val, coordinates)
            self._remove_from_group(self.subgrids, subgrid, old_val, coordinates)

        cell.value = val
        cell.conflict_count = 0
        if val == 0:
            return

        self._add_to_group(self.rows, row, val, coordinates, cell)
        self._add_to_group(self.cols, col, val, coordinates, cell)
        self._add_to_group(self.subgrids, subgrid, val, coordinates, cell)

    def is_valid_board(self) -> bool:
        return self.total_conflicts == 0

    def copy(self) -> Sudoku:
        return Sudoku(deepcopy(self.grid))

    def __str__(self) -> str:
        return '\n'.join(' '.join(str(cell.value) for cell in row) for row in self.grid)
