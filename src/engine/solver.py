from random import shuffle

from engine.sudoku import Sudoku


class Solver:
    @staticmethod
    def solve(unsolved: Sudoku) -> Sudoku | None:
        """
        Returns a new, solved instance of Sudoku.
        Does not mutate the input Sudoku.
        """
        sudoku = unsolved.copy()

        grid = sudoku.grid
        size = len(grid)

        def find_empty_cell() -> list[int] | None:
            for row in range(size):
                for col in range(size):
                    cell = grid[row][col]
                    if cell == 0:
                        return [row, col]

            return None

        def backtrack() -> bool:
            pos = find_empty_cell()
            if pos is None:
                return True

            row, col = pos

            def generate_random_list() -> list[int]:
                """Prevents identical solutions on each call with the same starting grid values"""
                nums = list(range(1, 10))
                shuffle(nums)
                return nums

            for n in generate_random_list():
                sudoku.set_cell(row=row, col=col, val=n)
                if sudoku.is_valid_board():
                    if backtrack():
                        return True
                sudoku.set_cell(row=row, col=col, val=0)

            return False

        if not sudoku.is_valid_board():
            return None

        if backtrack():
            return sudoku

        return None
