from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from client_window import ClientWindow
from manager_window import ManagerWindow
from admin_window import AdminWindow


class LoginWindow(QWidget):
    def __init__(self, stacked_widget, db):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("ООО 'Обувь' - Вход в систему")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Форма входа
        form_layout = QFormLayout()

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        form_layout.addRow("Логин:", self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Пароль:", self.password_input)

        layout.addLayout(form_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()

        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self.login)
        buttons_layout.addWidget(login_btn)

        guest_btn = QPushButton("Войти как гость")
        guest_btn.clicked.connect(self.guest_login)
        buttons_layout.addWidget(guest_btn)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        # Временный фикс для тестирования ролей
        if login == "admin" and password == "admin":
            self.stacked_widget.addWidget(AdminWindow(self.stacked_widget, self.db, "Администратор"))
            self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)
            return
        elif login == "manager" and password == "manager":
            self.stacked_widget.addWidget(ManagerWindow(self.stacked_widget, self.db, "Менеджер"))
            self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)
            return

        user = self.db.check_user(login, password)
        if user:
            role_id = user['role']
            user_name = f"{user['surname']} {user['name']}"

            print(f"Успешный вход: {user_name}, роль: {role_id}")  # Отладочный вывод

            if role_id == 1:  # Администратор
                print("Создание окна администратора")
                self.stacked_widget.addWidget(AdminWindow(self.stacked_widget, self.db, user_name))
            elif role_id == 2:  # Менеджер
                print("Создание окна менеджера")
                self.stacked_widget.addWidget(ManagerWindow(self.stacked_widget, self.db, user_name))
            elif role_id == 3:  # Клиент
                print("Создание окна клиента")
                self.stacked_widget.addWidget(ClientWindow(self.stacked_widget, self.db, user_name))
            else:
                QMessageBox.warning(self, "Ошибка", f"Неизвестная роль: {role_id}")
                return

            self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def guest_login(self):
        self.stacked_widget.addWidget(ClientWindow(self.stacked_widget, self.db, "Гость"))
        self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)