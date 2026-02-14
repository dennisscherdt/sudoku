from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLineEdit, QSizePolicy, QWidget

from domain.constants import GRID_SIZE, SUBGRID_SIZE

THIN = '1px'
THICK = '4px'
BORDER_COLOR = '#222'
CORNER_RADIUS = '12px'


class CellWidget(QLineEdit):
    def __init__(self, row: int, col: int, parent: QWidget | None = None):
        super().__init__(parent)

        self.row = row
        self.col = col

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaxLength(1)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.setValidator(QIntValidator(1, 9, self))

        last = GRID_SIZE - 1

        top = THICK if row % SUBGRID_SIZE == 0 else THIN
        left = THICK if col % SUBGRID_SIZE == 0 else THIN
        bottom = THICK if row == last else '0px'
        right = THICK if col == last else '0px'

        radius = ''
        if row == 0 and col == 0:
            radius = f'border-top-left-radius: {CORNER_RADIUS};'
        elif row == 0 and col == last:
            radius = f'border-top-right-radius: {CORNER_RADIUS};'
        elif row == last and col == 0:
            radius = f'border-bottom-left-radius: {CORNER_RADIUS};'
        elif row == last and col == last:
            radius = f'border-bottom-right-radius: {CORNER_RADIUS};'

        self._base_stylesheet = f"""
            QLineEdit {{
                font-size: 16px;
                border-top: {top} solid {BORDER_COLOR};
                border-left: {left} solid {BORDER_COLOR};
                border-bottom: {bottom} solid {BORDER_COLOR};
                border-right: {right} solid {BORDER_COLOR};
                {radius}
            }}
        """
        self.setStyleSheet(self._base_stylesheet)

    def set_conflict(self, has_conflict: bool) -> None:
        if has_conflict:
            self.setStyleSheet(
                self._base_stylesheet
                + """
                QLineEdit { background-color: #ffcccc; }
            """
            )
        else:
            self.setStyleSheet(self._base_stylesheet)
