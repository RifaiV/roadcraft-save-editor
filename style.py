from PyQt6.QtGui import QColor, QPalette, QFont, QIcon
from PyQt6.QtWidgets import QApplication, QStyleFactory, QGraphicsDropShadowEffect, QFrame, QPushButton, QLabel
from PyQt6.QtWidgets import QSpinBox, QCheckBox, QLineEdit, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt, QSize
import os
import sys
from typing import Optional

class StyleManager:
    DARK_THEME = {
        'background': '#1E1E1E',
        'secondary_bg': '#252525',
        'tertiary_bg': '#2D2D2D',
        'text': '#EEEEEE',
        'text_secondary': '#AAAAAA',
        'accent': '#FFCC00',
        'disabled': '#555555',
        'border': '#333333',
        'selection_bg': '#3E3E3E',
        'error': '#FF5555',
        'success': '#55FF7F',
        'card_bg': '#2A2A2A',
        'header_bg': '#323232',
        'panel_bg': '#1A1A1A'
    }
    
    FONTS = {
        'default': QFont("Segoe UI", 10),
        'header': QFont("Segoe UI", 12, QFont.Weight.Bold),
        'title': QFont("Segoe UI", 6, QFont.Weight.Bold),
        'button': QFont("Segoe UI", 10, QFont.Weight.Bold),
        'small': QFont("Segoe UI", 9),
        'monospace': QFont("Courier New", 10),
    }
    
    DEFAULT_WINDOW_SIZE = (1400, 900)
    PANEL_MARGINS = (20, 20, 20, 20)
    PANEL_SPACING = 10
    FORM_LAYOUT_SPACING = 10
    QUICK_BUTTONS_SPACING = 10
    TRUCK_ACTION_PANEL_MARGINS = (5, 50, 5, 50)
    TRUCK_ACTION_PANEL_WIDTH = 150
    LEVELS_TABLE_HEADER_HEIGHT = 75
    LEVELS_TABLE_ROW_HEIGHT = 55
    LEVELS_TABLE_COLUMN_WIDTHS = [250, 100, 100, 120, 100, 100, 120, 140, 120]
    FOOTER_BUTTON_MIN_WIDTH = 150
    PANEL_HEIGHT = 620
    TRUCK_DETAILS_MAX_WIDTH = 300
    TRUCK_IMAGE_CONTAINER_SIZE = (240, 170)
    TRUCK_IMAGE_LABEL_SIZE = (200, 140)
    FILE_ENTRY_MIN_WIDTH = 320
    
    STYLES = {
        'panel': """
            background-color: rgba(35, 35, 35, 200);
            border-radius: 10px;
            border: 1px solid {border};
            padding: 15px;
        """,
        
        'header_label': """
            font-size: 16px;
            font-weight: bold;
            color: {accent};
            padding: 5px 0px;
            border-bottom: 1px solid {border};
            margin-bottom: 10px;
        """,
        
        'title_label': """
            font-size: 12px;
            font-weight: bold;
            color: {accent};
            margin-bottom: 12px;
            border-bottom: 1px solid {border};
            padding-bottom: 15px;
        """,
        
        'main_title_label': """
            font-size: 24px;
            font-weight: bold;
            color: {accent};
        """,
        
        'settings_title_label': """
            font-size: 18px;
            font-weight: bold;
            color: {accent};
            margin-bottom: 15px;
            border-bottom: 1px solid #444;
            padding-bottom: 10px;
        """,
        
        'about_title_label': """
            font-size: 18px;
            font-weight: bold;
            color: {accent};
            margin-bottom: 15px;
            border-bottom: 1px solid #444;
            padding-bottom: 10px;
        """,
        
        'about_content_label': """
            color: #CCC;
            font-size: 14px;
        """,
        
        'dialog_label': """
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        """,
        
        'input_field': """
            QLineEdit {{
                background-color: rgba(45, 45, 45, 200);
                border: 1px solid {border};
                border-radius: 5px;
                padding: 8px;
                color: {text};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid {accent};
            }}
        """,
        
        'button': """
            QPushButton {{
                background-color: rgba(50, 50, 50, 220);
                color: {text};
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(70, 70, 70, 230);
            }}
            QPushButton:pressed {{
                background-color: rgba(90, 90, 90, 240);
            }}
            QPushButton:disabled {{
                background-color: rgba(40, 40, 40, 180);
                color: {disabled};
            }}
        """,
        
        'action_button': """
            QPushButton {{
                background-color: rgba(255, 204, 0, 220);
                color: black;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 215, 40, 230);
            }}
            QPushButton:pressed {{
                background-color: rgba(235, 184, 0, 240);
            }}
            QPushButton:disabled {{
                background-color: rgba(180, 160, 60, 180);
                color: rgba(50, 50, 50, 180);
            }}
        """,
        
        'spinbox': """
            QSpinBox {{
                background-color: rgba(45, 45, 45, 200);
                border: 1px solid {border};
                border-radius: 5px;
                padding: 5px;
                color: {text};
                font-weight: bold;
                font-size: 14px;
                min-width: 50px;
                min-height: 20px;
            }}
            QSpinBox:focus {{
                border: 1px solid {accent};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 16px;
                background-color: rgba(60, 60, 60, 220);
                border-radius: 2px;
                margin: 2px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: rgba(90, 90, 90, 240);
            }}
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {{
                background-color: rgba(120, 120, 120, 250);
            }}
            QSpinBox::up-arrow {{
                width: 10px;
                height: 10px;
                image: none;
                border: none;
                color: white;
                font-size: 14px;
                qproperty-text: "▲";
            }}
            QSpinBox::down-arrow {{
                width: 10px;
                height: 10px;
                image: none;
                border: none;
                color: white;
                font-size: 14px;
                qproperty-text: "▼";
            }}
            QTableWidget::item:selected QSpinBox {{
                background-color: rgba(50, 50, 50, 250);
                color: white;
            }}
        """,
        
        'table_cell_spinbox': """
            QSpinBox {{
                background-color: rgba(45, 45, 45, 220);
                border: 1px solid {border};
                border-radius: 3px;
                padding: 5px;
                color: {text};
                font-weight: bold;
                min-width: 50px;
                min-height: 15px;
                font-size: 13px;
            }}
            QSpinBox:focus {{
                border: 1px solid {accent};
                background-color: rgba(60, 60, 60, 250);
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: rgba(60, 60, 60, 220);
                width: 20px;
                height: 15px;
                border-radius: 2px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: rgba(80, 80, 80, 250);
            }}
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {{
                background-color: rgba(120, 120, 120, 250);
            }}
        """,
        
        'checkbox': """
            QCheckBox {{
                color: {text_secondary};
                font-size: 14px;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 1px solid {disabled};
                border-radius: 4px;
                background-color: rgba(40, 40, 40, 200);
            }}
            QCheckBox::indicator:checked {{
                background-color: {accent};
                border: 1px solid {accent};
                image: url(:/check.png);
            }}
            QCheckBox::indicator:unchecked:hover {{
                border: 1px solid {accent};
            }}
            QCheckBox:disabled {{
                color: {disabled};
            }}
            QCheckBox::indicator:disabled {{
                background-color: rgba(30, 30, 30, 150);
                border: 1px solid rgba(70, 70, 70, 150);
            }}
        """,
        
        'table_cell_checkbox': """
            QCheckBox {{
                background-color: transparent;
                color: {text};
                spacing: 5px;
                padding: 5px;
            }}
            QCheckBox::indicator {{
                width: 22px;
                height: 25px;
                border: 1px solid {disabled};
                border-radius: 3px;
                background-color: rgba(40, 40, 40, 220);
            }}
            QCheckBox::indicator:checked {{
                background-color: {accent};
                border: 1px solid {accent};
            }}
            QCheckBox::indicator:unchecked:hover {{
                border: 1px solid {accent};
            }}
        """,
        
        'list_widget': """
            QListWidget {{
                border: 1px solid {border};
                border-radius: 5px;
                background-color: rgba(30, 30, 30, 210);
                alternate-background-color: rgba(35, 35, 35, 210);
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {border};
                margin: 2px 0px;
            }}
            QListWidget::item:selected {{
                background-color: rgba(255, 204, 0, 120);
                color: {text};
                border-left: 3px solid {accent};
            }}
            QListWidget::item:hover:!selected {{
                background-color: rgba(50, 50, 50, 150);
            }}
            QListWidget QScrollBar:vertical {{
                border: none;
                background: rgba(45, 45, 45, 180);
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }}
            QListWidget QScrollBar::handle:vertical {{
                background: rgba(255, 204, 0, 180);
                border-radius: 5px;
                min-height: 20px;
            }}
            QListWidget QScrollBar::add-line:vertical, QListWidget QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """,
        
        'tab_widget': """
            QTabWidget::pane {{
                border-top: 1px solid {border}; 
                background-color: transparent;
                border-radius: 8px;
            }}
            QTabBar::tab {{ 
                background-color: rgba(35, 35, 35, 180);
                color: {text_secondary};
                padding: 8px 20px; 
                border-top-left-radius: 6px; 
                border-top-right-radius: 6px;
                margin-right: 2px;
                font-size: 14px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{ 
                background-color: rgba(50, 50, 50, 230);
                color: {accent};
                border-bottom: 3px solid {accent};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: rgba(45, 45, 45, 200);
            }}
        """,
        
        'table_widget': """
            QTableWidget {{
                background-color: rgba(30, 30, 30, 180);
                alternate-background-color: rgba(35, 35, 35, 180);
                border-radius: 8px;
                border: 1px solid {border};
                gridline-color: rgba(75, 75, 75, 120);
                selection-background-color: rgba(255, 204, 0, 120);
                selection-color: {text};
            }}
            QTableWidget::item {{
                padding: 5px 5px;
                border-bottom: 1px solid rgba(68, 68, 68, 120);
            }}
            QTableWidget QHeaderView::section {{
                background-color: rgba(45, 45, 45, 240);
                color: {accent};
                padding: 15px 10px;
                border: none;
                border-bottom: 2px solid {accent};
                font-weight: bold;
                font-size: 14px;
                text-transform: uppercase;
            }}
            QTableWidget QHeaderView::section:hover {{
                background-color: rgba(55, 55, 55, 250);
            }}
            QTableWidget::item:selected {{
                background-color: rgba(255, 204, 0, 150);
                color: #000000;
            }}
            QTableWidget::item:hover:!selected {{
                background-color: rgba(45, 45, 45, 200);
            }}
            QScrollBar:vertical {{
                border: none;
                background: rgba(45, 45, 45, 180);
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255, 204, 0, 180);
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: rgba(45, 45, 45, 180);
                height: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal {{
                background: rgba(255, 204, 0, 180);
                border-radius: 5px;
                min-width: 20px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """,
        
        
        'status_bar': """
            QStatusBar {{
                background-color: rgba(30, 30, 30, 230);
                color: white;
                padding: 8px;
                border-top: 1px solid #444;
            }}
            QStatusBar::item {{
                border: none;
                border-left: 1px solid #666;
                margin-left: 3px;
            }}
        """,
        
        'dialog': """
            QDialog {{
                background-color: {background};
                border: 1px solid {border};
                border-radius: 10px;
            }}
            QDialog QLabel {{
                color: {text};
                font-size: 14px;
            }}
        """,
        
        'message_box': """
            QMessageBox {{
                background-color: {background};
            }}
            QMessageBox QLabel {{
                color: {text};
                font-size: 14px;
            }}
            QMessageBox QPushButton {{
                min-width: 80px;
                min-height: 30px;
            }}
        """,
        
        'progress_bar': """
            QProgressBar {{
                border: 1px solid #444;
                border-radius: 5px;
                background-color: #333;
                text-align: center;
                height: 20px;
                color: black;
                font-weight: bold;
                font-size: 12px;
            }}
            QProgressBar::chunk {{
                background-color: #FFCC00;
                border-radius: 5px;
            }}
        """,
        
        'slider': """
            QSlider::groove:horizontal {{
                border: 1px solid {border};
                height: 8px;
                background: rgba(40, 40, 40, 220);
                margin: 2px 0;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {accent};
                border: 1px solid {accent};
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
            QSlider::handle:horizontal:hover {{
                background: #ffd630;
                border: 1px solid #ffd630;
            }}
        """,
        
        'group_box': """
            QGroupBox {{
                border: 1px solid {border};
                border-radius: 5px;
                margin-top: 20px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                color: {accent};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: {accent};
                background-color: {background};
            }}
        """,
        
        'scrollarea': """
            QScrollArea {{
                border: 1px solid {border};
                border-radius: 8px;
                background-color: transparent;
            }}
            QScrollArea #scrollAreaWidgetContents {{
                background-color: transparent;
            }}
        """,
        
        'tooltip': """
            QToolTip {{
                background-color: rgba(35, 35, 35, 230);
                color: {accent};
                border: 1px solid {border};
                padding: 5px;
                border-radius: 3px;
                font-size: 12px;
            }}
        """,
        
        'main_window': """
            QWidget#central_bg {{
                background-color: #1E1E1E;
            }}
        """,
        
        'main_window_with_bg': """
            QWidget#central_bg {{
                background-image: url('{background_image}');
                background-repeat: no-repeat;
                background-position: center center;
                background-attachment: fixed;
                background-color: #1E1E1E;
            }}
        """,
        
        'form_label': """
            QLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {text};
                margin-bottom: 5px;
            }}
        """,
        
        'settings_panel': """
            QFrame {{
                background-color: rgba(35, 35, 35, 200);
                border-radius: 10px;
                border: 1px solid {border};
                padding: 15px;
            }}
        """,
        
        'window_min_button': """
            QPushButton {{
                background-color: transparent;
                color: #AAAAAA;
                border: none;
                font-size: 18px;
                min-width: 32px;
                min-height: 32px;
            }}
            QPushButton:hover {{
                background-color: #333333;
                color: #FFCC00;
            }}
            QPushButton:pressed {{
                background-color: #222222;
                color: #FFD700;
            }}
        """,
        
        'window_close_button': """
            QPushButton {{
                background-color: transparent;
                color: #FF5555;
                border: none;
                font-size: 18px;
                min-width: 32px;
                min-height: 32px;
            }}
            QPushButton:hover {{
                background-color: #333333;
                color: #FFFFFF;
            }}
            QPushButton:pressed {{
                background-color: #550000;
                color: #FFAAAA;
            }}
        """,
        
        'logo_label': """
            QLabel {{
                background: transparent;
                margin-left: 10px;
                margin-right: 10px;
                padding: 0px;
            }}
        """,
        
        'header_frame': """
            QFrame#headerFrame {{
                background-color: rgba(30, 30, 30, 220);
                border-radius: 10px;
                padding: 10px;
            }}
        """,
        
        'about_panel': """
            QFrame#aboutPanel {{
                background-color: rgba(35, 35, 35, 200);
                border-radius: 15px;
                padding: 20px;
            }}
        """,
        
        'truck_frame': """
            background-color: rgba(30, 30, 30, 180);
            border: 1px solid {border};
            border-radius: 8px;
            padding: 5px;
        """,
        
        'truck_details_small_label': """
            font-size: 11px;
            color: {text_secondary};
            margin-top: 8px;
        """,
    }

    @classmethod
    def apply_dark_theme(cls, app):
        """Apply dark theme to the application"""
        try:
            app.setStyle(QStyleFactory.create("Fusion"))
            palette = QPalette()
            colors = cls.DARK_THEME
            
            palette.setColor(QPalette.ColorRole.Window, QColor(colors['background']))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(colors['text']))
            palette.setColor(QPalette.ColorRole.Base, QColor(colors['secondary_bg']))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors['tertiary_bg']))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors['background']))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors['accent']))
            palette.setColor(QPalette.ColorRole.Text, QColor(colors['text']))
            palette.setColor(QPalette.ColorRole.Button, QColor(colors['secondary_bg']))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors['text']))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(colors['accent']))
            palette.setColor(QPalette.ColorRole.Link, QColor(colors['accent']))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(colors['accent']))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors['background']))
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors['text_secondary']))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(colors['disabled']))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(colors['disabled']))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(colors['disabled']))
            
            app.setPalette(palette)
            app.setStyleSheet(cls.get_style('tooltip'))
        except Exception:
            pass

    @classmethod
    def get_style(cls, style_name: str, **kwargs) -> str:
        """Get a style string by name with optional parameter substitution"""
        try:
            if style_name not in cls.STYLES:
                return ""
            
            format_params = {**cls.DARK_THEME, **kwargs}
            return cls.STYLES[style_name].format(**format_params)
        except Exception:
            return ""

    @classmethod
    def create_panel(cls, object_name: str = "panel") -> QFrame:
        """Create a styled panel frame"""
        panel = QFrame()
        panel.setObjectName(object_name)
        panel.setStyleSheet(cls.get_style('panel'))
        return panel

    @classmethod
    def create_header_label(cls, text: str) -> QLabel:
        """Create a styled header label"""
        label = QLabel(text)
        label.setStyleSheet(cls.get_style('header_label'))
        label.setFont(cls.FONTS['header'])
        return label

    @classmethod
    def create_title_label(cls, text: str) -> QLabel:
        """Create a styled title label"""
        label = QLabel(text)
        label.setStyleSheet(cls.get_style('title_label'))
        label.setFont(cls.FONTS['title'])
        return label

    @classmethod
    def create_button(cls, text: str, action_button: bool = False, icon_path: Optional[str] = None) -> QPushButton:
        """Create a styled button"""
        button = QPushButton(text)
        style = 'action_button' if action_button else 'button'
        button.setStyleSheet(cls.get_style(style))
        button.setFont(cls.FONTS['button'])
        if icon_path and os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(16, 16))
        return button

    @classmethod
    def create_input_field(cls, placeholder: str = "", read_only: bool = False) -> QLineEdit:
        """Create a styled input field"""
        field = QLineEdit()
        field.setStyleSheet(cls.get_style('input_field'))
        field.setFont(cls.FONTS['default'])
        if placeholder:
            field.setPlaceholderText(placeholder)
        if read_only:
            field.setReadOnly(True)
        return field

    @classmethod
    def create_spinbox(cls, min_val: int = 0, max_val: int = 100, value: int = 0, table_cell: bool = False) -> QSpinBox:
        """Create a styled spinbox"""
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(value)
        style = 'table_cell_spinbox' if table_cell else 'spinbox'
        spinbox.setStyleSheet(cls.get_style(style))
        spinbox.setFont(cls.FONTS['default'])
        return spinbox

    @classmethod
    def create_checkbox(cls, text: str, checked: bool = False, table_cell: bool = False) -> QCheckBox:
        """Create a styled checkbox"""
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        style = 'table_cell_checkbox' if table_cell else 'checkbox'
        checkbox.setStyleSheet(cls.get_style(style))
        checkbox.setFont(cls.FONTS['default'])
        return checkbox

    @classmethod
    def apply_list_style(cls, list_widget):
        """Apply styling to a list widget"""
        list_widget.setStyleSheet(cls.get_style('list_widget'))
        list_widget.setAlternatingRowColors(True)

    @classmethod
    def apply_table_style(cls, table_widget):
        """Apply styling to a table widget"""
        table_widget.setStyleSheet(cls.get_style('table_widget'))
        table_widget.setAlternatingRowColors(True)
        table_widget.horizontalHeader().setStretchLastSection(True)
        table_widget.verticalHeader().setVisible(False)
        table_widget.horizontalHeader().setDefaultSectionSize(120)
        table_widget.verticalHeader().setDefaultSectionSize(40)

    @classmethod
    def get_truck_frame_stylesheet(cls):
        """Get truck frame stylesheet"""
        return cls.get_style('truck_frame')

    @classmethod
    def create_table_cell_spinbox(cls, min_val: int = 0, max_val: int = 100, value: int = 0) -> QSpinBox:
        """Create a table cell spinbox"""
        return cls.create_spinbox(min_val, max_val, value, table_cell=True)

    @classmethod
    def create_table_cell_checkbox(cls, checked: bool = False) -> QCheckBox:
        """Create a table cell checkbox"""
        return cls.create_checkbox("", checked, table_cell=True)

    @classmethod
    def get_font(cls, font_type: str = 'default'):
        """Get a font by type"""
        return cls.FONTS.get(font_type, cls.FONTS['default'])

    @classmethod
    def get_scaled_size(cls, base_width: int, base_height: int, scaling_factor: float = 1.0):
        """Get a scaled size"""
        return QSize(int(base_width * scaling_factor), int(base_height * scaling_factor))

    @classmethod
    def combine_styles(cls, *style_names):
        """Combine multiple styles"""
        return " ".join(cls.get_style(name) for name in style_names)

    @classmethod
    def create_shadow_effect(cls, color=None, blur_radius=20, offset_x=0, offset_y=0):
        """Create a shadow effect"""
        if color is None:
            color = QColor(0, 0, 0, 160)
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(color)
        shadow.setBlurRadius(blur_radius)
        shadow.setOffset(offset_x, offset_y)
        return shadow

    @classmethod
    def setup_table_widget(cls, table: QTableWidget, column_widths=None, column_labels=None):
        """Setup a table widget with proper styling and configuration"""
        cls.apply_table_style(table)
        if column_labels:
            table.setColumnCount(len(column_labels))
            for i, label in enumerate(column_labels):
                table.setHorizontalHeaderItem(i, QTableWidgetItem(label))
        if column_widths:
            for i, width in enumerate(column_widths):
                if i < table.columnCount():
                    table.setColumnWidth(i, width)
        
        header = table.horizontalHeader()
        if header:
            header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setHighlightSections(False)
            header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            header.setFixedHeight(cls.LEVELS_TABLE_HEADER_HEIGHT)
        
        v_header = table.verticalHeader()
        if v_header:
            v_header.setVisible(False)
            v_header.setDefaultSectionSize(cls.LEVELS_TABLE_ROW_HEIGHT)
        
        for i in range(table.rowCount()):
            table.setRowHeight(i, cls.LEVELS_TABLE_ROW_HEIGHT)
        
        table.setShowGrid(False)
        table.setWordWrap(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setCornerButtonEnabled(False)
        return table

    @classmethod
    def switch_theme(cls, theme_name='dark'):
        """Switch theme (placeholder for future multi-theme support)"""
        themes = {
            'dark': cls.DARK_THEME,
        }
        return themes.get(theme_name, cls.DARK_THEME)

    @staticmethod
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
        
    @staticmethod
    def get_logo_path():
        """Get the logo path"""
        return StyleManager.resource_path(os.path.join("images", "ui", "logo.png"))
