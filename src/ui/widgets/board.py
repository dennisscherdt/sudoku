from PySide6.QtWidgets import QGridLayout, QWidget

from domain.constants import GRID_SIZE

from .cell import CellWidget


class BoardWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setFixedSize(300, 300)

        grid = QGridLayout(self)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = CellWidget(row, col, parent=self)
                grid.addWidget(cell, row, col)
