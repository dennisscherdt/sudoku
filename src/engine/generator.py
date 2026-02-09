from random import shuffle

from domain.constants import GRID_SIZE, Difficulty
from engine.solver import Solver
from engine.sudoku import Sudoku


class Generator:
    def __init__(self, solver: Solver):
        self.solver = solver
        self.grid_size = GRID_SIZE

    def generate(self, difficulty: Difficulty) -> Sudoku:
        """
        Generate a new Sudoku puzzle at the given difficulty.
        Returns a Sudoku instance.
        """
        empty = Sudoku.empty()

        solved = self.solver.solve(empty)
        if solved is None:
            raise RuntimeError('Solver failed to solve an empty Sudoku')

        puzzle = solved.copy()
        cell_mask = self._generate_randomized_matrix(difficulty=difficulty)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if cell_mask[row][col] == 0:
                    puzzle.set_cell(row=row, col=col, val=0)

        return puzzle

    def _generate_randomized_matrix(self, difficulty: Difficulty) -> list[list[int]]:
        empty_cells_count = self.grid_size**2 - difficulty.value

        randomized_cells = [0] * empty_cells_count + [1] * difficulty.value
        shuffle(randomized_cells)

        randomized_matrix = [
            randomized_cells[i : i + self.grid_size]
            for i in range(0, len(randomized_cells), self.grid_size)
        ]

        return randomized_matrix
