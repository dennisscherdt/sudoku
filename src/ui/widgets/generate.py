from PySide6.QtWidgets import QPushButton, QWidget


class GenerateButtonWidget(QPushButton):
    def __init__(self, parent: QWidget | None = None):
        super().__init__('Generate', parent)
