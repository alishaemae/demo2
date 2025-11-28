import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from database import Database
from login_window import LoginWindow
from ui_components import StackedWidget
from styles import apply_styles  # Импортируем функцию применения стилей

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ООО 'Обувь' - Информационная система")
        self.setGeometry(100, 100, 1200, 700)

        self.stacked_widget = StackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Добавляем окно входа
        login_window = LoginWindow(self.stacked_widget, self.db)
        self.stacked_widget.addWidget(login_window)

def main():
    app = QApplication(sys.argv)
    # Применяем стили ко всему приложению
    apply_styles(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()