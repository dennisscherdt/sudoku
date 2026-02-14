from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from engine.generator import Generator
from engine.solver import Solver
from ui.widgets import BoardWidget, DifficultyWidget, GenerateButtonWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Sudoku')
        self.resize(400, 400)

        self.generator = Generator(Solver())

        central = QWidget(self)
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel('Sudoku')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        self.board = BoardWidget()
        self.difficulty = DifficultyWidget()
        self.generate_button = GenerateButtonWidget()

        self.generate_button.clicked.connect(self._on_generate)

        layout.addWidget(self.title)
        layout.addWidget(self.board)
        layout.addWidget(self.difficulty)
        layout.addWidget(self.generate_button)

    def _on_generate(self) -> None:
        difficulty = self.difficulty.selected_difficulty
        puzzle = self.generator.generate(difficulty)
        self.board.update_board(puzzle)
