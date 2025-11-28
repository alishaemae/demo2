# manager_window.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QLineEdit, QTabWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QHeaderView
from styles import AppStyles


class ManagerWindow(QWidget):
    def __init__(self, stacked_widget, db, user_name):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.user_name = user_name
        self.all_orders = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        header_layout = QHBoxLayout()
        title = QLabel(f"Панель менеджера - {self.user_name}")
        title.setFont(AppStyles.get_font(14, True))
        title.setStyleSheet(f"color: {AppStyles.TEXT_COLOR};")
        header_layout.addWidget(title)

        back_btn = QPushButton("Выход")
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        layout.addLayout(header_layout)

        # Вкладки
        self.tabs = QTabWidget()

        # Вкладка товаров
        products_tab = QWidget()
        products_layout = QVBoxLayout()

        # Поиск, сортировка и фильтрация для товаров
        search_filter_layout = QHBoxLayout()
        
        # Поиск
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по всем данным...")
        self.search_input.textChanged.connect(self.apply_filters)
        search_filter_layout.addWidget(QLabel("Поиск:"))
        search_filter_layout.addWidget(self.search_input)
        
        # Сортировка по количеству
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Без сортировки", "none")
        self.sort_combo.addItem("Количество (по возрастанию)", "amount_asc")
        self.sort_combo.addItem("Количество (по убыванию)", "amount_desc")
        self.sort_combo.currentIndexChanged.connect(self.apply_filters)
        search_filter_layout.addWidget(QLabel("Сортировка:"))
        search_filter_layout.addWidget(self.sort_combo)
        
        # Фильтр по поставщику
        self.supplier_filter = QComboBox()
        self.supplier_filter.addItem("Все поставщики", 0)
        for supplier in self.db.get_suppliers():
            self.supplier_filter.addItem(supplier['name'], supplier['id'])
        self.supplier_filter.currentIndexChanged.connect(self.apply_filters)
        search_filter_layout.addWidget(QLabel("Поставщик:"))
        search_filter_layout.addWidget(self.supplier_filter)
        
        products_layout.addLayout(search_filter_layout)

        # Дополнительные фильтры для товаров
        filters_layout = QHBoxLayout()

        self.type_filter = QComboBox()
        self.type_filter.addItem("Все типы", 0)
        for product_type in self.db.get_product_types():
            self.type_filter.addItem(product_type['name'], product_type['id'])
        self.type_filter.currentIndexChanged.connect(self.apply_filters)
        filters_layout.addWidget(QLabel("Тип:"))
        filters_layout.addWidget(self.type_filter)

        self.category_filter = QComboBox()
        self.category_filter.addItem("Все категории", 0)
        for category in self.db.get_categories():
            self.category_filter.addItem(category['name'], category['id'])
        self.category_filter.currentIndexChanged.connect(self.apply_filters)
        filters_layout.addWidget(QLabel("Категория:"))
        filters_layout.addWidget(self.category_filter)

        self.producer_filter = QComboBox()
        self.producer_filter.addItem("Все производители", 0)
        for producer in self.db.get_producers():
            self.producer_filter.addItem(producer['name'], producer['id'])
        self.producer_filter.currentIndexChanged.connect(self.apply_filters)
        filters_layout.addWidget(QLabel("Производитель:"))
        filters_layout.addWidget(self.producer_filter)

        products_layout.addLayout(filters_layout)

        self.products_table = QTableWidget()
        products_layout.addWidget(self.products_table)

        products_tab.setLayout(products_layout)
        self.tabs.addTab(products_tab, "Товары")

        # Вкладка заказов
        orders_tab = QWidget()
        orders_layout = QVBoxLayout()

        # Панель управления заказами
        orders_management_layout = QHBoxLayout()

        refresh_orders_btn = QPushButton("Обновить")
        refresh_orders_btn.clicked.connect(self.load_orders)
        orders_management_layout.addWidget(refresh_orders_btn)

        orders_management_layout.addStretch()

        orders_layout.addLayout(orders_management_layout)

        # Фильтры для заказов
        orders_filters_layout = QHBoxLayout()

        # Фильтр по статусу
        self.order_status_filter = QComboBox()
        self.order_status_filter.addItem("Все статусы", 0)
        for status in self.db.get_statuses():
            self.order_status_filter.addItem(status['name'], status['id'])
        self.order_status_filter.currentIndexChanged.connect(self.apply_order_filters)
        orders_filters_layout.addWidget(QLabel("Статус:"))
        orders_filters_layout.addWidget(self.order_status_filter)

        # Фильтр по городу ПВЗ
        self.order_city_filter = QComboBox()
        self.order_city_filter.addItem("Все города", 0)
        orders_filters_layout.addWidget(QLabel("Город:"))
        orders_filters_layout.addWidget(self.order_city_filter)

        orders_layout.addLayout(orders_filters_layout)

        # Поиск и сортировка для заказов
        orders_search_sort_layout = QHBoxLayout()

        # Поиск по коду заказа
        self.order_search_input = QLineEdit()
        self.order_search_input.setPlaceholderText("Поиск по коду заказа...")
        self.order_search_input.textChanged.connect(self.apply_order_filters)
        orders_search_sort_layout.addWidget(QLabel("Поиск:"))
        orders_search_sort_layout.addWidget(self.order_search_input)

        # Сортировка
        self.order_sort_combo = QComboBox()
        self.order_sort_combo.addItem("Сортировка: Дата заказа (новые)", "date_order_desc")
        self.order_sort_combo.addItem("Сортировка: Дата заказа (старые)", "date_order_asc")
        self.order_sort_combo.addItem("Сортировка: Дата доставки (ближ.)", "date_delivery_asc")
        self.order_sort_combo.addItem("Сортировка: Дата доставки (дальш.)", "date_delivery_desc")
        self.order_sort_combo.addItem("Сортировка: Код заказа", "code")
        self.order_sort_combo.currentIndexChanged.connect(self.apply_order_filters)
        orders_search_sort_layout.addWidget(self.order_sort_combo)

        orders_layout.addLayout(orders_search_sort_layout)

        self.orders_table = QTableWidget()
        # Включаем сортировку по клику на заголовок
        self.orders_table.setSortingEnabled(True)
        orders_layout.addWidget(self.orders_table)

        orders_tab.setLayout(orders_layout)
        self.tabs.addTab(orders_tab, "Заказы")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.load_products()
        self.load_orders()

    def load_products(self):
        products = self.db.get_products()
        self.display_products(products)

    def load_orders(self):
        orders = self.db.get_orders()
        self.all_orders = orders
        self.update_city_filter()
        self.apply_order_filters()

    def update_city_filter(self):
        """Обновляет список городов в фильтре"""
        cities = set()
        for order in self.all_orders:
            city = order.get('pvz_city', '')
            if city:
                cities.add(city)

        self.order_city_filter.clear()
        self.order_city_filter.addItem("Все города", 0)
        for city in sorted(cities):
            self.order_city_filter.addItem(city, city)

    def display_products(self, products):
        self.products_table.setRowCount(len(products))
        self.products_table.setColumnCount(9)
        self.products_table.setHorizontalHeaderLabels([
            "Артикул", "Описание", "Тип", "Категория",
            "Производитель", "Цена", "Скидка %", "Количество", "Поставщик"
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

            # Скидка
            discount_item = QTableWidgetItem(str(product['discount']))
            self.products_table.setItem(row, 6, discount_item)

            # Количество
            amount_item = QTableWidgetItem(str(product['amount']))
            self.products_table.setItem(row, 7, amount_item)
            
            self.products_table.setItem(row, 8, QTableWidgetItem(product.get('supplier_name', '')))

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

    def display_orders(self, orders):
        self.orders_table.setRowCount(len(orders))
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
            "Код заказа", "Дата заказа", "Дата доставки",
            "Статус", "Клиент", "ПВЗ", "Город"
        ])

        for row, order in enumerate(orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order['identificator_code'])))
            self.orders_table.setItem(row, 1, QTableWidgetItem(str(order['date_order'])))
            self.orders_table.setItem(row, 2, QTableWidgetItem(str(order['date_delivery'])))

            status_item = QTableWidgetItem(order.get('status_name', ''))
            if order.get('status_name') == 'Новый':
                status_item.setBackground(QColor(AppStyles.ACCENT_COLOR))
            self.orders_table.setItem(row, 3, status_item)

            self.orders_table.setItem(row, 4,
                                      QTableWidgetItem(f"{order.get('user_surname', '')} {order.get('user_name', '')}"))
            self.orders_table.setItem(row, 5,
                                      QTableWidgetItem(f"{order.get('pvz_street', '')}, {order.get('number', '')}"))
            self.orders_table.setItem(row, 6, QTableWidgetItem(order.get('pvz_city', '')))

        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def apply_filters(self):
        filters = {}

        # Поиск по всем текстовым полям
        if self.search_input.text():
            filters['search'] = self.search_input.text()
        
        # Сортировка
        sort_option = self.sort_combo.currentData()
        if sort_option != "none":
            filters['sort'] = sort_option
        
        # Фильтр по поставщику
        if self.supplier_filter.currentData() and self.supplier_filter.currentData() != 0:
            filters['supplier'] = self.supplier_filter.currentData()

        # Существующие фильтры
        if self.type_filter.currentData() and self.type_filter.currentData() != 0:
            filters['type'] = self.type_filter.currentData()

        if self.category_filter.currentData() and self.category_filter.currentData() != 0:
            filters['category'] = self.category_filter.currentData()

        if self.producer_filter.currentData() and self.producer_filter.currentData() != 0:
            filters['producer'] = self.producer_filter.currentData()

        products = self.db.get_products(filters)
        self.display_products(products)

    def apply_order_filters(self):
        """Применяет фильтры и сортировку к заказам"""
        if not self.all_orders:
            return

        filtered_orders = self.all_orders.copy()

        # Фильтрация по статусу
        status_filter = self.order_status_filter.currentData()
        if status_filter and status_filter != 0:
            filtered_orders = [order for order in filtered_orders if order.get('id_status') == status_filter]

        # Фильтрация по городу
        city_filter = self.order_city_filter.currentData()
        if city_filter and city_filter != 0:
            filtered_orders = [order for order in filtered_orders if order.get('pvz_city') == city_filter]

        # Поиск по коду заказа
        search_text = self.order_search_input.text().strip()
        if search_text:
            filtered_orders = [order for order in filtered_orders
                               if search_text in str(order.get('identificator_code', ''))]

        # Сортировка
        sort_option = self.order_sort_combo.currentData()
        if sort_option == "date_order_desc":
            filtered_orders.sort(key=lambda x: x.get('date_order', ''), reverse=True)
        elif sort_option == "date_order_asc":
            filtered_orders.sort(key=lambda x: x.get('date_order', ''))
        elif sort_option == "date_delivery_asc":
            filtered_orders.sort(key=lambda x: x.get('date_delivery', ''))
        elif sort_option == "date_delivery_desc":
            filtered_orders.sort(key=lambda x: x.get('date_delivery', ''), reverse=True)
        elif sort_option == "code":
            filtered_orders.sort(key=lambda x: x.get('identificator_code', 0))

        self.display_orders(filtered_orders)

    def go_back(self):
        self.stacked_widget.removeWidget(self)
        self.stacked_widget.setCurrentIndex(0)