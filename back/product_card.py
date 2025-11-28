# product_card.py
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import base64


class ProductCard(QFrame):
    def __init__(self, product_data, is_admin=False, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.is_admin = is_admin
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(280, 450)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 15px;
                margin: 8px;
            }
            QFrame:hover {
                border-color: #00FA9A;
                background-color: #F8FFF8;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)

        # Изображение товара
        self.image_label = QLabel()
        self.image_label.setFixedSize(120, 120)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #CCCCCC; 
                background-color: #F5F5F5;
                border-radius: 4px;
            }
        """)
        self.load_image()
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Категория товара
        category_label = QLabel(f"Категория товара | {self.product_data.get('category_name', '')}")
        category_label.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 12px; 
                color: #333333;
                margin: 2px;
            }
        """)
        layout.addWidget(category_label)

        # Наименование товара
        name_label = QLabel(f"Наименование товара: {self.product_data.get('article', '')}")
        name_label.setStyleSheet("""
            QLabel {
                font-size: 11px; 
                color: #666666;
                margin: 1px;
            }
        """)
        layout.addWidget(name_label)

        # Описание товара
        description = self.product_data.get('description', '')
        if len(description) > 80:
            description = description[:80] + "..."
        desc_label = QLabel(f"Описание товара: {description}")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 10px; 
                color: #777777;
                margin: 1px;
            }
        """)
        layout.addWidget(desc_label)

        # Производитель
        producer_label = QLabel(f"Производитель: {self.product_data.get('producer_name', '')}")
        producer_label.setStyleSheet("""
            QLabel {
                font-size: 10px; 
                color: #777777;
                margin: 1px;
            }
        """)
        layout.addWidget(producer_label)

        # Поставщик
        supplier_label = QLabel(f"Поставщик: {self.product_data.get('supplier_name', '')}")
        supplier_label.setStyleSheet("""
            QLabel {
                font-size: 10px; 
                color: #777777;
                margin: 1px;
            }
        """)
        layout.addWidget(supplier_label)

        # Цена и единица измерения
        price_layout = QHBoxLayout()
        price_label = QLabel(f"Цена: {self.product_data.get('price', 0)} руб.")
        price_label.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 14px; 
                color: #FF0000;
                margin: 2px;
            }
        """)
        price_layout.addWidget(price_label)
        
        unit_label = QLabel("шт.")
        unit_label.setStyleSheet("""
            QLabel {
                font-size: 11px; 
                color: #666666;
                margin: 2px;
            }
        """)
        price_layout.addWidget(unit_label)
        price_layout.addStretch()
        
        layout.addLayout(price_layout)

        # Количество на складе
        amount_label = QLabel(f"Количество на складе: {self.product_data.get('amount', 0)}")
        amount_label.setStyleSheet("""
            QLabel {
                font-size: 10px; 
                color: #777777;
                margin: 1px;
            }
        """)
        layout.addWidget(amount_label)

        # Скидка
        discount = self.product_data.get('discount', 0)
        discount_label = QLabel(f"Действующая скидка: {discount}%")
        if discount > 15:
            discount_label.setStyleSheet("""
                QLabel {
                    font-weight: bold; 
                    font-size: 12px; 
                    color: #FF4500;
                    margin: 2px;
                }
            """)
        else:
            discount_label.setStyleSheet("""
                QLabel {
                    font-size: 11px; 
                    color: #666666;
                    margin: 2px;
                }
            """)
        layout.addWidget(discount_label)

        # Кнопки управления для администратора
        if self.is_admin:
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(5)
            
            edit_btn = QPushButton("Редактировать")
            edit_btn.setFixedHeight(25)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7FFF00;
                    color: black;
                    border: 1px solid #CCCCCC;
                    border-radius: 3px;
                    font-size: 10px;
                    padding: 2px 5px;
                }
                QPushButton:hover {
                    background-color: #00FA9A;
                }
            """)
            edit_btn.clicked.connect(self.edit_product)
            btn_layout.addWidget(edit_btn)

            delete_btn = QPushButton("Удалить")
            delete_btn.setFixedHeight(25)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF6B6B;
                    color: white;
                    border: 1px solid #CCCCCC;
                    border-radius: 3px;
                    font-size: 10px;
                    padding: 2px 5px;
                }
                QPushButton:hover {
                    background-color: #FF5252;
                }
            """)
            delete_btn.clicked.connect(self.delete_product)
            btn_layout.addWidget(delete_btn)

            image_btn = QPushButton("Изм. фото")
            image_btn.setFixedHeight(25)
            image_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4FC3F7;
                    color: white;
                    border: 1px solid #CCCCCC;
                    border-radius: 3px;
                    font-size: 10px;
                    padding: 2px 5px;
                }
                QPushButton:hover {
                    background-color: #29B6F6;
                }
            """)
            image_btn.clicked.connect(self.change_image)
            btn_layout.addWidget(image_btn)

            layout.addLayout(btn_layout)

        layout.addStretch()
        self.setLayout(layout)

    def load_image(self):
        """Загрузка изображения товара"""
        image_data = self.product_data.get('image_data')
        if image_data:
            try:
                # Декодируем base64 изображение
                image_bytes = base64.b64decode(image_data)
                pixmap = QPixmap()
                pixmap.loadFromData(image_bytes)
                self.image_label.setPixmap(pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio))
            except:
                self.set_default_image()
        else:
            self.set_default_image()

    def set_default_image(self):
        """Установка изображения по умолчанию"""
        self.image_label.setText("Нет\nизображения")
        self.image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #CCCCCC; 
                background-color: #F5F5F5;
                color: #666666; 
                font-size: 9px;
                border-radius: 4px;
            }
        """)

    def edit_product(self):
        """Редактирование товара"""
        if self.parent and hasattr(self.parent, 'edit_product'):
            self.parent.edit_product(self.product_data['id'])

    def delete_product(self):
        """Удаление товара"""
        if self.parent and hasattr(self.parent, 'delete_product'):
            self.parent.delete_product(self.product_data['id'])

    def change_image(self):
        """Изменение изображения товара"""
        if self.parent and hasattr(self.parent, 'change_product_image'):
            self.parent.change_product_image(self.product_data['id'])