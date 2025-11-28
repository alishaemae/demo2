# styles.py - ПОЛНЫЙ КОД
from PyQt6.QtGui import QFont


class AppStyles:
    """Класс для хранения стилей приложения"""

    # Основные цвета
    PRIMARY_COLOR = "#7FFF00"  # Дополнительный фон
    ACCENT_COLOR = "#00FA9A"  # Цвет для акцентов
    DISCOUNT_HIGHLIGHT = "#2E8B57"  # Для скидок >15%
    OUT_OF_STOCK_COLOR = "#ADD8E6"  # Голубой для отсутствующих товаров
    STRIKETHROUGH_COLOR = "#FF0000"  # Красный для перечеркнутой цены
    WHITE = "#FFFFFF"  # Основной фон
    TEXT_COLOR = "#000000"  # Основной цвет текста

    # Основной шрифт
    @staticmethod
    def get_font(size=10, bold=False):
        font = QFont("Times New Roman", size)
        font.setBold(bold)
        return font

    # Стили для главного окна
    MAIN_WINDOW = f"""
        QMainWindow {{
            background-color: {WHITE};
            color: {TEXT_COLOR};
        }}
    """

    # Стили для кнопок
    BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: {TEXT_COLOR};
            border: 1px solid #CCCCCC;
            border-radius: 5px;
            padding: 8px 16px;
            font-family: "Times New Roman";
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {ACCENT_COLOR};
            border: 1px solid #999999;
        }}
        QPushButton:pressed {{
            background-color: #00CD85;
        }}
    """

    # Стили для полей ввода
    LINE_EDIT_STYLE = f"""
        QLineEdit {{
            background-color: {WHITE};
            color: {TEXT_COLOR};
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            padding: 5px;
            font-family: "Times New Roman";
            font-size: 12px;
        }}
        QLineEdit:focus {{
            border: 1px solid {ACCENT_COLOR};
        }}
    """

    # Стили для выпадающих списков
    COMBO_BOX_STYLE = f"""
        QComboBox {{
            background-color: {WHITE};
            color: {TEXT_COLOR};
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            padding: 5px;
            font-family: "Times New Roman";
            font-size: 12px;
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {WHITE};
            color: {TEXT_COLOR};
            selection-background-color: {ACCENT_COLOR};
            font-family: "Times New Roman";
            font-size: 12px;
        }}
    """

    # Стили для таблиц
    TABLE_STYLE = f"""
        QTableWidget {{
            background-color: {WHITE};
            color: {TEXT_COLOR};
            border: 1px solid #CCCCCC;
            gridline-color: #DDDDDD;
            font-family: "Times New Roman";
            font-size: 11px;
        }}
        QTableWidget::item {{
            padding: 5px;
            border-bottom: 1px solid #EEEEEE;
        }}
        QTableWidget::item:selected {{
            background-color: {ACCENT_COLOR};
            color: {TEXT_COLOR};
        }}
        QHeaderView::section {{
            background-color: {PRIMARY_COLOR};
            color: {TEXT_COLOR};
            padding: 8px;
            border: 1px solid #CCCCCC;
            font-family: "Times New Roman";
            font-size: 12px;
            font-weight: bold;
        }}
    """

    # Стили для вкладок
    TAB_WIDGET_STYLE = f"""
        QTabWidget::pane {{
            border: 1px solid #CCCCCC;
            background-color: {WHITE};
        }}
        QTabWidget::tab-bar {{
            alignment: center;
        }}
        QTabBar::tab {{
            background-color: #F0F0F0;
            color: {TEXT_COLOR};
            padding: 8px 16px;
            margin: 2px;
            border: 1px solid #CCCCCC;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            font-family: "Times New Roman";
            font-size: 12px;
        }}
        QTabBar::tab:selected {{
            background-color: {PRIMARY_COLOR};
            color: {TEXT_COLOR};
            font-weight: bold;
        }}
        QTabBar::tab:hover:!selected {{
            background-color: {ACCENT_COLOR};
        }}
    """

    # Стили для заголовков
    TITLE_STYLE = f"""
        QLabel {{
            color: {TEXT_COLOR};
            font-family: "Times New Roman";
            font-size: 16px;
            font-weight: bold;
        }}
    """

    # Стили для меток
    LABEL_STYLE = f"""
        QLabel {{
            color: {TEXT_COLOR};
            font-family: "Times New Roman";
            font-size: 12px;
        }}
    """

    # Стили для сообщений
    MESSAGE_BOX_STYLE = f"""
        QMessageBox {{
            background-color: {WHITE};
            color: {TEXT_COLOR};
            font-family: "Times New Roman";
        }}
        QMessageBox QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: {TEXT_COLOR};
            font-family: "Times New Roman";
            min-width: 80px;
        }}
    """


def apply_styles(app):
    """Применяет стили ко всему приложению"""
    app.setStyleSheet(f"""
        * {{
            font-family: "Times New Roman";
        }}
        {AppStyles.MAIN_WINDOW}
        {AppStyles.BUTTON_STYLE}
        {AppStyles.LINE_EDIT_STYLE}
        {AppStyles.COMBO_BOX_STYLE}
        {AppStyles.TABLE_STYLE}
        {AppStyles.TAB_WIDGET_STYLE}
        {AppStyles.TITLE_STYLE}
        {AppStyles.LABEL_STYLE}
        {AppStyles.MESSAGE_BOX_STYLE}
    """)