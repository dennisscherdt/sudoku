from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

from domain.constants import GRID_SIZE

from .cell import CellWidget


class BoardWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setFixedSize(300, 300)

        self.grid = QGridLayout(self)
        self.grid.setSpacing(6)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = CellWidget(parent=self)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.grid.addWidget(cell, row, col)
