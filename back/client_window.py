# client_window.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QHeaderView
from styles import AppStyles


class ClientWindow(QWidget):
    def __init__(self, stacked_widget, db, user_name):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.user_name = user_name
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        header_layout = QHBoxLayout()
        title = QLabel(f"Просмотр товаров - {self.user_name}")
        title.setFont(AppStyles.get_font(14, True))
        header_layout.addWidget(title)

        back_btn = QPushButton("Выход")
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        layout.addLayout(header_layout)

        # Таблица товаров (только просмотр)
        self.products_table = QTableWidget()
        self.load_products()
        layout.addWidget(self.products_table)

        self.setLayout(layout)

    def load_products(self):
        products = self.db.get_products()
        self.display_products(products)

    def display_products(self, products):
        self.products_table.setRowCount(len(products))
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels([
            "Артикул", "Описание", "Тип", "Категория",
            "Производитель", "Цена"
        ])

        for row, product in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(product['article']))
            self.products_table.setItem(row, 1, QTableWidgetItem(product['description']))
            self.products_table.setItem(row, 2, QTableWidgetItem(product.get('type_name', '')))
            self.products_table.setItem(row, 3, QTableWidgetItem(product.get('category_name', '')))
            self.products_table.setItem(row, 4, QTableWidgetItem(product.get('producer_name', '')))
            
            # Цена с учетом скидки - ИСПРАВЛЕНО: преобразование decimal в float
            price = float(product['price'])  # Преобразуем decimal в float
            discount = float(product['discount'])  # Преобразуем decimal в float
            if discount > 0:
                final_price = price * (1 - discount/100)
                price_item = QTableWidgetItem(f"{price} -> {final_price:.2f}")
                price_item.setForeground(QColor(AppStyles.STRIKETHROUGH_COLOR))
            else:
                price_item = QTableWidgetItem(str(price))
            self.products_table.setItem(row, 5, price_item)

            # Подсветка строк
            background_color = None
            if discount > 15:
                background_color = QColor(AppStyles.DISCOUNT_HIGHLIGHT)
            elif product['amount'] == 0:
                background_color = QColor(AppStyles.OUT_OF_STOCK_COLOR)

            if background_color:
                for col in range(self.products_table.columnCount()):
                    item = self.products_table.item(row, col)
                    if item:
                        item.setBackground(background_color)

        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def go_back(self):
        self.stacked_widget.removeWidget(self)
        self.stacked_widget.setCurrentIndex(0)