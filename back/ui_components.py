from PyQt6.QtWidgets import QStackedWidget

class StackedWidget(QStackedWidget):
    """Кастомный StackedWidget с дополнительными методами если понадобятся"""
    def __init__(self):
        super().__init__()