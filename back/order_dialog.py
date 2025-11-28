# order_dialog.py
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QSpinBox,
                             QDateEdit, QComboBox, QDialogButtonBox)
from PyQt6.QtCore import QDate


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
            self.pvz_combo.setCurrentIndex(self.order_data.get('id_pvz', 1) - 1)
        form_layout.addRow("ПВЗ:", self.pvz_combo)

        self.status_combo = QComboBox()
        for status in self.db.get_statuses():
            self.status_combo.addItem(status['name'], status['id'])
        if self.order_data:
            self.status_combo.setCurrentIndex(self.order_data.get('id_status', 1) - 1)
        form_layout.addRow("Статус:", self.status_combo)

        layout.addLayout(form_layout)

        # Кнопки
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
            'id_user': 3  # По умолчанию клиент
        }