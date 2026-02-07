from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLineEdit, QSizePolicy, QWidget


class CellWidget(QLineEdit):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaxLength(1)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.setValidator(QIntValidator(1, 9, self))

        self.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                border: none;
            }
        """)
