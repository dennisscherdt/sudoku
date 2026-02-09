from PySide6.QtWidgets import QComboBox, QWidget

from domain.constants import Difficulty


class DifficultyWidget(QComboBox):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        for difficulty in Difficulty:
            self.addItem(difficulty.name.replace('_', ' ').title(), difficulty)

    @property
    def selected_difficulty(self) -> Difficulty:
        difficulty: Difficulty = self.currentData()
        return difficulty
