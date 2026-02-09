from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from ui.widgets import BoardWidget, DifficultyWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Sudoku')
        self.resize(400, 400)

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

        layout.addWidget(self.title)
        layout.addWidget(self.board)
        layout.addWidget(self.difficulty)
