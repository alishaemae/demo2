# product_dialog.py
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                           QLineEdit, QTextEdit, QComboBox, QSpinBox,
                           QPushButton, QDialogButtonBox, QLabel, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import base64
import os


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
        self.setFixedSize(600, 700)

        layout = QVBoxLayout()

        # Изображение товара
        image_layout = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(150, 150)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #CCCCCC; background-color: #F5F5F5;")
        
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
            self.type_combo.setCurrentIndex(self.product_data.get('id_type', 1) - 1)
        form_layout.addRow("Тип товара:", self.type_combo)

        self.category_combo = QComboBox()
        for category in self.db.get_categories():
            self.category_combo.addItem(category['name'], category['id'])
        if self.product_data:
            self.category_combo.setCurrentIndex(self.product_data.get('id_category', 1) - 1)
        form_layout.addRow("Категория:", self.category_combo)

        self.producer_combo = QComboBox()
        for producer in self.db.get_producers():
            self.producer_combo.addItem(producer['name'], producer['id'])
        if self.product_data:
            self.producer_combo.setCurrentIndex(self.product_data.get('id_producer', 1) - 1)
        form_layout.addRow("Производитель:", self.producer_combo)

        self.supplier_combo = QComboBox()
        for supplier in self.db.get_suppliers():
            self.supplier_combo.addItem(supplier['name'], supplier['id'])
        if self.product_data:
            self.supplier_combo.setCurrentIndex(self.product_data.get('id_supplier', 1) - 1)
        form_layout.addRow("Поставщик:", self.supplier_combo)

        self.price_input = QSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setValue(self.product_data.get('price', 0) if self.product_data else 0)
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

        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        
        # Загружаем текущее изображение если есть
        if self.product_data and self.product_data.get('image_data'):
            self.load_current_image()

    def load_image(self):
        """Загрузка изображения через проводник"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение товара", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

    def load_current_image(self):
        """Загрузка текущего изображения товара"""
        image_data = self.product_data.get('image_data')
        if image_data:
            try:
                image_bytes = base64.b64decode(image_data)
                pixmap = QPixmap()
                pixmap.loadFromData(image_bytes)
                self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            except Exception as e:
                print(f"Ошибка загрузки изображения: {e}")

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
        
        # Добавляем изображение если было выбрано новое
        if self.image_path and os.path.exists(self.image_path):
            try:
                with open(self.image_path, 'rb') as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                data['image_data'] = image_data
            except Exception as e:
                print(f"Ошибка чтения изображения: {e}")
        elif self.product_data and self.product_data.get('image_data'):
            # Сохраняем существующее изображение
            data['image_data'] = self.product_data.get('image_data')
            
        return data