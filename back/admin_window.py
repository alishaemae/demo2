# admin_window.py - ПОЛНЫЙ ИСПРАВЛЕННЫЙ КОД
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QLineEdit, QTabWidget, QMessageBox,
                             QDialog, QFormLayout, QSpinBox, QTextEdit,
                             QDialogButtonBox, QDateEdit, QFileDialog, QDoubleSpinBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor, QPixmap
from PyQt6.QtWidgets import QHeaderView
from styles import AppStyles
import datetime
import base64
import os
from PIL import Image
import io


class ProductDialog(QDialog):
    def __init__(self, db, product_data=None):
        super().__init__()
        self.db = db
        self.product_data = product_data
        self.image_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавление товара" if not self.product_data else "Редактирование товара")
        self.setModal(True)
        self.setFixedSize(500, 700)

        layout = QVBoxLayout()

        # Загрузка изображения
        image_layout = QHBoxLayout()
        self.image_label = QLabel("Изображение не выбрано")
        self.image_label.setFixedSize(150, 150)
        self.image_label.setStyleSheet("border: 1px solid #CCCCCC; background-color: #F5F5F5;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        load_image_btn = QPushButton("Загрузить изображение")
        load_image_btn.clicked.connect(self.load_image)
        
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(load_image_btn)
        layout.addLayout(image_layout)

        form_layout = QFormLayout()

        self.article_input = QLineEdit()
        self.article_input.setText(self.product_data.get('article', '') if self.product_data else '')
        form_layout.addRow("Артикул:", self.article_input)

        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        self.description_input.setText(self.product_data.get('description', '') if self.product_data else '')
        form_layout.addRow("Описание:", self.description_input)

        self.type_combo = QComboBox()
        for product_type in self.db.get_product_types():
            self.type_combo.addItem(product_type['name'], product_type['id'])
        if self.product_data:
            for i in range(self.type_combo.count()):
                if self.type_combo.itemData(i) == self.product_data.get('id_type'):
                    self.type_combo.setCurrentIndex(i)
                    break
        form_layout.addRow("Тип товара:", self.type_combo)

        self.category_combo = QComboBox()
        for category in self.db.get_categories():
            self.category_combo.addItem(category['name'], category['id'])
        if self.product_data:
            for i in range(self.category_combo.count()):
                if self.category_combo.itemData(i) == self.product_data.get('id_category'):
                    self.category_combo.setCurrentIndex(i)
                    break
        form_layout.addRow("Категория:", self.category_combo)

        self.producer_combo = QComboBox()
        for producer in self.db.get_producers():
            self.producer_combo.addItem(producer['name'], producer['id'])
        if self.product_data:
            for i in range(self.producer_combo.count()):
                if self.producer_combo.itemData(i) == self.product_data.get('id_producer'):
                    self.producer_combo.setCurrentIndex(i)
                    break
        form_layout.addRow("Производитель:", self.producer_combo)

        self.supplier_combo = QComboBox()
        for supplier in self.db.get_suppliers():
            self.supplier_combo.addItem(supplier['name'], supplier['id'])
        if self.product_data:
            for i in range(self.supplier_combo.count()):
                if self.supplier_combo.itemData(i) == self.product_data.get('id_supplier'):
                    self.supplier_combo.setCurrentIndex(i)
                    break
        form_layout.addRow("Поставщик:", self.supplier_combo)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setDecimals(2)
        price_value = float(self.product_data.get('price', 0)) if self.product_data else 0
        self.price_input.setValue(price_value)
        form_layout.addRow("Цена:", self.price_input)

        self.discount_input = QSpinBox()
        self.discount_input.setRange(0, 100)
        self.discount_input.setValue(self.product_data.get('discount', 0) if self.product_data else 0)
        form_layout.addRow("Скидка %:", self.discount_input)

        self.amount_input = QSpinBox()
        self.amount_input.setRange(0, 1000)
        self.amount_input.setValue(self.product_data.get('amount', 0) if self.product_data else 0)
        form_layout.addRow("Количество:", self.amount_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение товара", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            try:
                with Image.open(file_name) as img:
                    img = img.resize((300, 200), Image.Resampling.LANCZOS)
                    
                    temp_path = "temp_resized_image.png"
                    img.save(temp_path, "PNG")
                    
                    self.image_path = temp_path
                    pixmap = QPixmap(temp_path)
                    self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
                    
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить изображение: {e}")

    def get_product_data(self):
        data = {
            'article': self.article_input.text(),
            'description': self.description_input.toPlainText(),
            'id_type': self.type_combo.currentData(),
            'id_category': self.category_combo.currentData(),
            'id_producer': self.producer_combo.currentData(),
            'id_supplier': self.supplier_combo.currentData(),
            'price': self.price_input.value(),
            'discount': self.discount_input.value(),
            'amount': self.amount_input.value()
        }
        
        if self.image_path and os.path.exists(self.image_path):
            try:
                with open(self.image_path, 'rb') as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                data['image_data'] = image_data
                
                os.remove(self.image_path)
            except Exception as e:
                print(f"Ошибка чтения изображения: {e}")
                
        return data


class OrderDialog(QDialog):
    def __init__(self, db, order_data=None):
        super().__init__()
        self.db = db
        self.order_data = order_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавление заказа" if not self.order_data else "Редактирование заказа")
        self.setModal(True)
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.code_input = QSpinBox()
        self.code_input.setRange(100, 9999)
        self.code_input.setValue(self.order_data.get('identificator_code', 100) if self.order_data else 100)
        form_layout.addRow("Код заказа:", self.code_input)

        self.date_order_input = QDateEdit()
        self.date_order_input.setDate(QDate.currentDate())
        if self.order_data and self.order_data.get('date_order'):
            self.date_order_input.setDate(QDate.fromString(self.order_data['date_order'], 'yyyy-MM-dd'))
        form_layout.addRow("Дата заказа:", self.date_order_input)

        self.date_delivery_input = QDateEdit()
        self.date_delivery_input.setDate(QDate.currentDate().addDays(7))
        if self.order_data and self.order_data.get('date_delivery'):
            self.date_delivery_input.setDate(QDate.fromString(self.order_data['date_delivery'], 'yyyy-MM-dd'))
        form_layout.addRow("Дата доставки:", self.date_delivery_input)

        self.pvz_combo = QComboBox()
        for pvz in self.db.get_pvz_list():
            self.pvz_combo.addItem(f"{pvz['city']}, {pvz['street']} {pvz['number']}", pvz['id'])
        if self.order_data:
            for i in range(self.pvz_combo.count()):
                if self.pvz_combo.itemData(i) == self.order_data.get('id_pvz'):
                    self.pvz_combo.setCurrentIndex(i)
                    break
        form_layout.addRow("ПВЗ:", self.pvz_combo)

        self.status_combo = QComboBox()
        for status in self.db.get_statuses():
            self.status_combo.addItem(status['name'], status['id'])
        if self.order_data:
            for i in range(self.status_combo.count()):
                if self.status_combo.itemData(i) == self.order_data.get('id_status'):
                    self.status_combo.setCurrentIndex(i)
                    break
        form_layout.addRow("Статус:", self.status_combo)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_order_data(self):
        return {
            'identificator_code': self.code_input.value(),
            'date_order': self.date_order_input.date().toString('yyyy-MM-dd'),
            'date_delivery': self.date_delivery_input.date().toString('yyyy-MM-dd'),
            'id_pvz': self.pvz_combo.currentData(),
            'id_status': self.status_combo.currentData(),
            'id_user': 3
        }


class AdminWindow(QWidget):
    def __init__(self, stacked_widget, db, user_name):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.user_name = user_name
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        title = QLabel(f"Панель администратора - {self.user_name}")
        title.setFont(AppStyles.get_font(14, True))
        title.setStyleSheet(f"color: {AppStyles.TEXT_COLOR};")
        header_layout.addWidget(title)

        back_btn = QPushButton("Выход")
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        layout.addLayout(header_layout)

        self.tabs = QTabWidget()

        products_tab = QWidget()
        products_layout = QVBoxLayout()

        management_layout = QHBoxLayout()

        add_btn = QPushButton("Добавить товар")
        add_btn.clicked.connect(self.add_product)
        management_layout.addWidget(add_btn)

        edit_btn = QPushButton("Редактировать товар")
        edit_btn.clicked.connect(self.edit_product)
        management_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Удалить товар")
        delete_btn.clicked.connect(self.delete_product)
        management_layout.addWidget(delete_btn)

        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.load_products)
        management_layout.addWidget(refresh_btn)

        products_layout.addLayout(management_layout)

        search_filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по всем данным...")
        self.search_input.textChanged.connect(self.apply_filters)
        search_filter_layout.addWidget(QLabel("Поиск:"))
        search_filter_layout.addWidget(self.search_input)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Без сортировки", "none")
        self.sort_combo.addItem("Количество (по возрастанию)", "amount_asc")
        self.sort_combo.addItem("Количество (по убыванию)", "amount_desc")
        self.sort_combo.currentIndexChanged.connect(self.apply_filters)
        search_filter_layout.addWidget(QLabel("Сортировка:"))
        search_filter_layout.addWidget(self.sort_combo)
        
        self.supplier_filter = QComboBox()
        self.supplier_filter.addItem("Все поставщики", 0)
        for supplier in self.db.get_suppliers():
            self.supplier_filter.addItem(supplier['name'], supplier['id'])
        self.supplier_filter.currentIndexChanged.connect(self.apply_filters)
        search_filter_layout.addWidget(QLabel("Поставщик:"))
        search_filter_layout.addWidget(self.supplier_filter)
        
        products_layout.addLayout(search_filter_layout)

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
        self.tabs.addTab(products_tab, "Управление товарами")

        orders_tab = QWidget()
        orders_layout = QVBoxLayout()

        orders_management_layout = QHBoxLayout()

        add_order_btn = QPushButton("Добавить заказ")
        add_order_btn.clicked.connect(self.add_order)
        orders_management_layout.addWidget(add_order_btn)

        edit_order_btn = QPushButton("Редактировать заказ")
        edit_order_btn.clicked.connect(self.edit_order)
        orders_management_layout.addWidget(edit_order_btn)

        delete_order_btn = QPushButton("Удалить заказ")
        delete_order_btn.clicked.connect(self.delete_order)
        orders_management_layout.addWidget(delete_order_btn)

        refresh_orders_btn = QPushButton("Обновить")
        refresh_orders_btn.clicked.connect(self.load_orders)
        orders_management_layout.addWidget(refresh_orders_btn)

        orders_layout.addLayout(orders_management_layout)

        self.orders_table = QTableWidget()
        orders_layout.addWidget(self.orders_table)

        orders_tab.setLayout(orders_layout)
        self.tabs.addTab(orders_tab, "Управление заказами")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.load_products()
        self.load_orders()

    def load_products(self):
        products = self.db.get_products()
        self.display_products(products)

    def load_orders(self):
        orders = self.db.get_orders()
        self.display_orders(orders)

    def display_products(self, products):
        self.products_table.setRowCount(len(products))
        self.products_table.setColumnCount(10)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Артикул", "Описание", "Тип", "Категория",
            "Производитель", "Цена", "Скидка %", "Количество", "Поставщик"
        ])

        for row, product in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.products_table.setItem(row, 1, QTableWidgetItem(product['article']))
            self.products_table.setItem(row, 2, QTableWidgetItem(product['description']))
            self.products_table.setItem(row, 3, QTableWidgetItem(product.get('type_name', '')))
            self.products_table.setItem(row, 4, QTableWidgetItem(product.get('category_name', '')))
            self.products_table.setItem(row, 5, QTableWidgetItem(product.get('producer_name', '')))
            
            price = float(product['price'])
            discount = float(product['discount'])
            if discount > 0:
                final_price = price * (1 - discount/100)
                price_item = QTableWidgetItem(f"{price} -> {final_price:.2f}")
                price_item.setForeground(QColor(AppStyles.STRIKETHROUGH_COLOR))
            else:
                price_item = QTableWidgetItem(str(price))
            self.products_table.setItem(row, 6, price_item)

            discount_item = QTableWidgetItem(str(product['discount']))
            self.products_table.setItem(row, 7, discount_item)

            amount_item = QTableWidgetItem(str(product['amount']))
            self.products_table.setItem(row, 8, amount_item)
            
            self.products_table.setItem(row, 9, QTableWidgetItem(product.get('supplier_name', '')))

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
        self.orders_table.setColumnCount(8)
        self.orders_table.setHorizontalHeaderLabels([
            "ID", "Код заказа", "Дата заказа", "Дата доставки",
            "Статус", "Клиент", "ПВЗ", "Город"
        ])

        for row, order in enumerate(orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            self.orders_table.setItem(row, 1, QTableWidgetItem(str(order['identificator_code'])))
            self.orders_table.setItem(row, 2, QTableWidgetItem(str(order['date_order'])))
            self.orders_table.setItem(row, 3, QTableWidgetItem(str(order['date_delivery'])))

            status_item = QTableWidgetItem(order.get('status_name', ''))
            if order.get('status_name') == 'Новый':
                status_item.setBackground(QColor(AppStyles.ACCENT_COLOR))
            self.orders_table.setItem(row, 4, status_item)

            self.orders_table.setItem(row, 5,
                                      QTableWidgetItem(f"{order.get('user_surname', '')} {order.get('user_name', '')}"))
            self.orders_table.setItem(row, 6,
                                      QTableWidgetItem(f"{order.get('pvz_street', '')}, {order.get('number', '')}"))
            self.orders_table.setItem(row, 7, QTableWidgetItem(order.get('pvz_city', '')))

        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def apply_filters(self):
        filters = {}

        if self.search_input.text():
            filters['search'] = self.search_input.text()
        
        sort_option = self.sort_combo.currentData()
        if sort_option != "none":
            filters['sort'] = sort_option
        
        if self.supplier_filter.currentData() and self.supplier_filter.currentData() != 0:
            filters['supplier'] = self.supplier_filter.currentData()

        if self.type_filter.currentData() and self.type_filter.currentData() != 0:
            filters['type'] = self.type_filter.currentData()

        if self.category_filter.currentData() and self.category_filter.currentData() != 0:
            filters['category'] = self.category_filter.currentData()

        if self.producer_filter.currentData() and self.producer_filter.currentData() != 0:
            filters['producer'] = self.producer_filter.currentData()

        products = self.db.get_products(filters)
        self.display_products(products)

    def add_product(self):
        dialog = ProductDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            product_data = dialog.get_product_data()
            if self.db.add_product(product_data):
                QMessageBox.information(self, "Успех", f"Товар {product_data['article']} добавлен")
                self.load_products()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить товар")

    def edit_product(self):
        current_row = self.products_table.currentRow()
        if current_row >= 0:
            product_id = int(self.products_table.item(current_row, 0).text())
            
            all_products = self.db.get_products()
            product_data = None
            for product in all_products:
                if product['id'] == product_id:
                    product_data = product
                    break
            
            if product_data:
                dialog = ProductDialog(self.db, product_data)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    updated_data = dialog.get_product_data()
                    if self.db.update_product(product_id, updated_data):
                        QMessageBox.information(self, "Успех", f"Товар {updated_data['article']} обновлен")
                        self.load_products()
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить товар")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти данные товара")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для редактирования")

    def delete_product(self):
        current_row = self.products_table.currentRow()
        if current_row >= 0:
            product_id = self.products_table.item(current_row, 0).text()
            product_name = self.products_table.item(current_row, 1).text()

            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить товар {product_name} (ID: {product_id})?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.db.delete_product(product_id):
                    QMessageBox.information(self, "Успех", f"Товар {product_name} удален")
                    self.load_products()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить товар")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления")

    def add_order(self):
        dialog = OrderDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            order_data = dialog.get_order_data()
            if self.db.add_order(order_data):
                QMessageBox.information(self, "Успех", f"Заказ #{order_data['identificator_code']} добавлен")
                self.load_orders()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить заказ")

    def edit_order(self):
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order_id = int(self.orders_table.item(current_row, 0).text())
            
            all_orders = self.db.get_orders()
            order_data = None
            for order in all_orders:
                if order['id'] == order_id:
                    order_data = order
                    break
            
            if order_data:
                dialog = OrderDialog(self.db, order_data)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    updated_data = dialog.get_order_data()
                    if self.db.update_order(order_id, updated_data):
                        QMessageBox.information(self, "Успех", f"Заказ #{updated_data['identificator_code']} обновлен")
                        self.load_orders()
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить заказ")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти данные заказа")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для редактирования")

    def delete_order(self):
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order_id = self.orders_table.item(current_row, 0).text()
            order_code = self.orders_table.item(current_row, 1).text()

            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить заказ #{order_code} (ID: {order_id})?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.db.delete_order(order_id):
                    QMessageBox.information(self, "Успех", f"Заказ #{order_code} удален")
                    self.load_orders()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить заказ")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для удаления")

    def go_back(self):
        self.stacked_widget.removeWidget(self)
        self.stacked_widget.setCurrentIndex(0)