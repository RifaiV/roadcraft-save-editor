import sys
import os
import json
import glob
import hashlib
import shutil
import zlib
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QFileDialog, QLabel, QPushButton, 
    QLineEdit, QComboBox, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QProgressBar, QDialog, 
    QFormLayout, QSpinBox, QCheckBox, QStatusBar, QMessageBox, QFrame, QSizePolicy, QScrollArea, 
    QSplitter, QGridLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QPixmap, QFont, QColor, QIcon, QPalette
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer, QRect
from trucks import TrucksData
from style import StyleManager
from constants import *
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
IMAGES_DIR = resource_path(IMAGES_DIR_NAME)
UI_IMAGES_DIR = resource_path(os.path.join(IMAGES_DIR_NAME, UI_IMAGES_DIR_NAME))
BACKGROUND_IMAGE = os.path.join(UI_IMAGES_DIR, "background.jpg")
ICON_PATH = os.path.join(UI_IMAGES_DIR, "icon.ico")
SAVE_FILE_HEADER_LENGTH = 53
SAVE_FILE_WBITS_VALUE = -15
class Config:    
    CONFIG_DIR_NAME = CONFIG_DIR_NAME
    CONFIG_FILE_NAME = CONFIG_FILE_NAME
    DEFAULTS = {
        'window_geometry': f"{StyleManager.DEFAULT_WINDOW_SIZE[0]}x{StyleManager.DEFAULT_WINDOW_SIZE[1]}",
        'auto_backup': True,
        'backup_count': BACKUP_MAX_COUNT,
        'theme': 'dark'
    }
    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), self.CONFIG_DIR_NAME)
        self.config_file = os.path.join(self.config_dir, self.CONFIG_FILE_NAME)
        self.default_config = self.DEFAULTS.copy()
        self.config = self.load_config()
    def load_config(self) -> Dict[str, Any]:
        os.makedirs(self.config_dir, exist_ok=True)
        config = self.default_config.copy()
        if os.path.isfile(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        config.update(loaded)
            except Exception as e:
                pass
        return config
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            pass
    def get(self, key: str, default=None) -> Any:
        return self.config.get(key, self.default_config.get(key, default))
    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save_config()
    def reset_to_defaults(self) -> None:
        self.config = self.default_config.copy()
        self.save_config()
class SaveManager:
    def compute_md5_hex(self, data: bytes) -> str:
        return hashlib.md5(data).hexdigest()
    def try_decompress_zlib_block(self, data: bytes, start_offset: int = 0) -> Optional[Dict]:
        zlib_block_with_headers = data[start_offset:]
        if len(zlib_block_with_headers) < 8:
            return None
        uncompressed_size = int.from_bytes(zlib_block_with_headers[0:4], byteorder='little')
        compressed_size = int.from_bytes(zlib_block_with_headers[4:8], byteorder='little')
        if len(zlib_block_with_headers) < compressed_size + 8:
            return None
        if compressed_size < 6:
            return None
        try:
            decompressed = zlib.decompress(
                zlib_block_with_headers[8 : 8 + compressed_size], 
                wbits=15
            )
        except zlib.error:
            return None
        return {
            'uncompressed_size': uncompressed_size,
            'compressed_size': compressed_size,
            'decompressed_bytes': decompressed
        }
    def decode_file(self, file_path: str) -> Tuple[Optional[bytes], Optional[bytes]]:
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        offset = SAVE_FILE_HEADER_LENGTH
        decompressed_data = bytearray()
        total_compressed_size_expected = int.from_bytes(file_content[4:8], byteorder='little')
        total_uncompressed_size_expected = int.from_bytes(file_content[12:16], byteorder='little')
        bytes_processed_in_stream = 0
        while bytes_processed_in_stream < total_compressed_size_expected and (offset + 8) <= len(file_content):
            current_block_data = file_content[offset:]
            result = self.try_decompress_zlib_block(current_block_data, start_offset=0)
            if result is None:
                raise Exception(ERROR_DECOMPRESS_BLOCK.format(offset=offset))
            decompressed_data.extend(result['decompressed_bytes'])
            bytes_processed_in_stream += result['compressed_size'] + 8
            offset += result['compressed_size'] + 8
        if len(decompressed_data) != total_uncompressed_size_expected:
            pass
        if bytes_processed_in_stream != total_compressed_size_expected:
            pass
        return file_content, decompressed_data
    def encode_file(self, original_header_content: bytes, decompressed_data_bytes: bytes, output_path: str) -> bool:
        try:
            if not decompressed_data_bytes:
                raise Exception(ERROR_DECOMPRESS_SAVE)
            new_compressed_data = zlib.compress(
                decompressed_data_bytes, 
                level=zlib.Z_DEFAULT_COMPRESSION, 
                wbits=15
            )
            new_block_uncompressed_size_bytes = len(decompressed_data_bytes).to_bytes(4, 'little')
            new_block_compressed_size_bytes = len(new_compressed_data).to_bytes(4, 'little')
            new_zlib_data_blocks = new_block_uncompressed_size_bytes + new_block_compressed_size_bytes + new_compressed_data
            magic_bytes = original_header_content[0:4]
            unknown_bytes_8_12 = original_header_content[8:12]
            unknown_bytes_16_20 = original_header_content[16:20]
            unknown_byte_52 = original_header_content[52:53]
            new_total_compressed_size_bytes = len(new_zlib_data_blocks).to_bytes(4, 'little')
            new_total_uncompressed_size_bytes = len(decompressed_data_bytes).to_bytes(4, 'little')
            new_md5_header_bytes = self.compute_md5_hex(new_zlib_data_blocks).encode('ascii')
            final_header = (
                magic_bytes +
                new_total_compressed_size_bytes +
                unknown_bytes_8_12 +
                new_total_uncompressed_size_bytes +                unknown_bytes_16_20 +
                new_md5_header_bytes +
                unknown_byte_52
            )
            final_data_to_write = final_header + new_zlib_data_blocks
            with open(output_path, 'wb') as f:
                f.write(final_data_to_write)
            return True
        except Exception as e:
            raise Exception(ERROR_ENCODING.format(error=e))
    def get_steam_users(self) -> Dict[str, List[str]]:
        users = {}
        try:
            base_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Saber", "RoadCraftGame", "storage", "steam", "user")
            if os.path.exists(base_path):
                for user_folder in os.listdir(base_path):
                    user_save_dir = os.path.join(base_path, user_folder, "Main", "save")
                    if os.path.exists(user_save_dir):
                        save_slots = []
                        for file in os.listdir(user_save_dir):
                            if file.startswith("SLOT_"):
                                save_slots.append(file)
                        if save_slots:
                            users[user_folder] = save_slots
            return users
        except Exception as e:
            return {}
    def get_save_path(self, user_id: str, slot_name: str) -> str:
        try:
            save_path = os.path.join(
                os.path.expanduser("~"),
                "AppData", "Local", "Saber", "RoadCraftGame", "storage", "steam", "user",
                user_id, "Main", "save", slot_name
            )
            if os.path.exists(save_path):
                return save_path
            return ""
        except Exception as e:
            return ""
    def create_backup(self, save_path: str, backup_dir: Optional[str] = None) -> str:
        if backup_dir is None:
            backup_dir = os.path.dirname(save_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = BACKUP_FILE_PATTERN.format(timestamp=timestamp)
        backup_path = os.path.join(backup_dir, backup_name)
        shutil.copy2(save_path, backup_path)
        return backup_path
    def cleanup_old_backups(self, backup_dir: str, max_backups: int = BACKUP_MAX_COUNT):
        backup_pattern = os.path.join(backup_dir, BACKUP_FILE_PATTERN.replace('{timestamp}', '*'))
        backups = glob.glob(backup_pattern)
        if len(backups) > max_backups:
            backups.sort(key=os.path.getmtime)
            for backup_file in backups[:-max_backups]:
                try:
                    os.remove(backup_file)
                except OSError:
                    pass
    def validate_save_data(self, data: Dict[str, Any]) -> List[str]:
        warnings = []
        if "SslValue" not in data:
            warnings.append(WARNING_MISSING_SSLVALUE)
            return warnings
        ssl_value = data["SslValue"]
        required_fields = ["money", "xp", "lockedTrucks", "unlockedTrucks"]
        for field in required_fields:
            if field not in ssl_value:
                warnings.append(WARNING_MISSING_FIELD.format(field=field))
        if "money" in ssl_value and not isinstance(ssl_value["money"], (int, float)):
            warnings.append(WARNING_MONEY_NOT_NUMERIC)
        if "xp" in ssl_value and not isinstance(ssl_value["xp"], (int, float)):
            warnings.append(WARNING_XP_NOT_NUMERIC)
        if "lockedTrucks" in ssl_value and not isinstance(ssl_value["lockedTrucks"], list):
            warnings.append(WARNING_LOCKED_TRUCKS_NOT_LIST)
        if "unlockedTrucks" in ssl_value and not isinstance(ssl_value["unlockedTrucks"], dict):
            warnings.append(WARNING_UNLOCKED_TRUCKS_NOT_DICT)
        return warnings
BACKGROUND_IMAGE = os.path.join(UI_IMAGES_DIR, "background.jpg")
os.makedirs(UI_IMAGES_DIR, exist_ok=True)
class ProgressDialog(QDialog):
    def __init__(self, parent=None, title=DIALOG_PROCESSING_TITLE, message=DIALOG_PROCESSING_MESSAGE):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 150)
        layout = QVBoxLayout(self)
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(StyleManager.get_style('dialog_label'))
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(StyleManager.get_style('progress_bar'))
        self.detail_label = QLabel("")
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.detail_label)
        layout.setContentsMargins(*StyleManager.PANEL_MARGINS)
    def update_progress(self, value: int, detail: str = ""):
        self.progress_bar.setValue(value)
        self.detail_label.setText(detail)
        QApplication.processEvents()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._drag_pos = None
        self.config = Config()
        self.current_save_path = None
        self.original_file_content = None
        self.json_data = None
        self.current_truck_image = None
        self.save_manager = SaveManager()
        self.trucks_data = TrucksData()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*StyleManager.DEFAULT_WINDOW_SIZE)
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        app = QApplication.instance()
        if app:
            StyleManager.apply_dark_theme(app)
        self._init_ui()
        if not os.path.exists(BACKGROUND_IMAGE):
            self.status.showMessage(f"Background image not found at: {BACKGROUND_IMAGE}")
    def _init_ui(self):
        central = QWidget()
        central.setObjectName("central_bg")
        self.setCentralWidget(central)
        if os.path.exists(BACKGROUND_IMAGE):
            self.setStyleSheet(StyleManager.get_style('main_window_with_bg', background_image=BACKGROUND_IMAGE.replace(os.sep, "/")))
        else:
            self.setStyleSheet(StyleManager.get_style('main_window'))
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(*StyleManager.PANEL_MARGINS)
        main_layout.setSpacing(StyleManager.PANEL_SPACING)
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet(StyleManager.get_style('header_frame'))
        header_container = QVBoxLayout()
        header_container.setContentsMargins(0, 0, 0, 0)
        header_container.setSpacing(0)
        window_controls_bar = QHBoxLayout()
        window_controls_bar.setContentsMargins(0, 0, 0, 0)
        window_controls_bar.setSpacing(0)
        window_controls_bar.addStretch(1)
        btn_min = QPushButton("–")
        btn_min.setMinimumSize(28, 28)
        btn_min.setMaximumSize(28, 28)
        btn_min.setStyleSheet(StyleManager.get_style('window_min_button'))
        btn_min.clicked.connect(self.showMinimized)
        btn_close = QPushButton("×")
        btn_close.setMinimumSize(28, 28)
        btn_close.setMaximumSize(28, 28)
        btn_close.setStyleSheet(StyleManager.get_style('window_close_button'))
        btn_close.clicked.connect(self.close)
        window_controls_bar.addWidget(btn_min)
        window_controls_bar.addWidget(btn_close)
        header_container.addLayout(window_controls_bar)
        header_content_layout = QHBoxLayout()
        header_content_layout.setContentsMargins(0, 0, 0, 0)
        header_content_layout.setSpacing(0)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = StyleManager.get_logo_path()
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(
                320, 60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setStyleSheet(StyleManager.get_style('logo_label'))
            header_content_layout.addWidget(logo_label)
        else:
            title_label = QLabel(WINDOW_TITLE.upper())
            title_label.setStyleSheet(StyleManager.get_style('main_title_label'))
            header_content_layout.addWidget(title_label)
        header_content_layout.addStretch(1)
        file_layout = QHBoxLayout()
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.setSpacing(0)
        self.file_entry = QLineEdit()
        self.file_entry.setReadOnly(True)
        self.file_entry.setMinimumWidth(StyleManager.FILE_ENTRY_MIN_WIDTH)
        self.file_entry.setStyleSheet(StyleManager.get_style('input_field'))
        self.browse_button = QPushButton(BUTTON_OPEN_SAVE_FILE)
        self.browse_button.setObjectName("actionButton")
        self.browse_button.setStyleSheet(StyleManager.get_style('action_button'))
        self.browse_button.clicked.connect(self._browse_save_file)
        file_layout.addWidget(self.file_entry)
        file_layout.addWidget(self.browse_button)
        header_content_layout.addLayout(file_layout)
        header_container.addLayout(header_content_layout)
        header_frame.setLayout(header_container)
        main_layout.addWidget(header_frame)
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(StyleManager.get_style('tab_widget'))
        self.trucks_tab = QWidget()
        self.stats_tab = QWidget()
        self.levels_tab = QWidget()
        self.settings_tab = QWidget()
        self.tabs.addTab(self.trucks_tab, TAB_TRUCKS)
        self.tabs.addTab(self.stats_tab, TAB_PLAYER_STATS)
        self.tabs.addTab(self.levels_tab, TAB_LEVELS)
        self.tabs.addTab(self.settings_tab, TAB_SETTINGS)
        main_layout.addWidget(self.tabs, 1)
        self.status = QStatusBar()
        self.status.setStyleSheet(StyleManager.get_style('status_bar'))
        self.setStatusBar(self.status)
        self.status.showMessage(STATUS_READY)
        footer_layout = QHBoxLayout()
        footer_layout.addStretch(1)
        self.save_button = QPushButton(BUTTON_SAVE_CHANGES)
        self.save_button.setObjectName("actionButton")
        self.save_button.setStyleSheet(StyleManager.get_style('action_button'))
        self.save_button.setMinimumWidth(StyleManager.FOOTER_BUTTON_MIN_WIDTH)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self._save_changes)
        footer_layout.addWidget(self.save_button)
        main_layout.addLayout(footer_layout)
        self._init_trucks_tab()
        self._init_stats_tab()
        self._init_levels_tab()
        self._init_settings_tab()
    def _init_trucks_tab(self):
        layout = QHBoxLayout(self.trucks_tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(StyleManager.PANEL_SPACING)
        panel_height = StyleManager.PANEL_HEIGHT
        self.locked_trucks_panel = TruckListPanel(LABEL_LOCKED_TRUCKS)
        self.locked_trucks_panel.setFixedHeight(panel_height)
        self.locked_trucks_panel.selectionChanged.connect(self._on_locked_truck_selected)
        self.truck_action_panel = TruckActionPanel()
        self.truck_action_panel.setFixedHeight(panel_height)
        self.truck_action_panel.unlockSelected.connect(self._unlock_selected)
        self.truck_action_panel.lockSelected.connect(self._lock_selected)
        self.truck_action_panel.unlockAll.connect(self._unlock_all)
        self.truck_action_panel.lockAll.connect(self._lock_all)
        self.unlocked_trucks_panel = TruckListPanel(LABEL_UNLOCKED_TRUCKS)
        self.unlocked_trucks_panel.setFixedHeight(panel_height)
        self.unlocked_trucks_panel.selectionChanged.connect(self._on_unlocked_truck_selected)
        self.truck_details_panel = TruckDetailsPanel()
        self.truck_details_panel.setFixedHeight(panel_height)
        layout.addWidget(self.locked_trucks_panel, 3)
        layout.addWidget(self.truck_action_panel)
        layout.addWidget(self.unlocked_trucks_panel, 3)
        layout.addWidget(self.truck_details_panel)
    def _on_locked_truck_selected(self, truck_id):
        self.unlocked_trucks_panel.clear_selection()
        self._update_truck_details(truck_id)
    def _on_unlocked_truck_selected(self, truck_id):
        self.locked_trucks_panel.clear_selection()
        self._update_truck_details(truck_id)
    def _update_truck_details(self, truck_id):
        stats = self.trucks_data.get_truck_stats(truck_id)
        image_path = self.trucks_data.get_truck_image_path(truck_id)
        if image_path is None:
            image_path = ""
        self.truck_details_panel.update_truck_details(stats, image_path)
    def _unlock_selected(self):
        truck_id = self.locked_trucks_panel.get_selected_truck_id()
        if not truck_id:
            QMessageBox.warning(self, DIALOG_WARNING_TITLE, WARNING_NO_TRUCK_SELECTED)
            return
        self._move_truck(truck_id, "unlock")
    def _lock_selected(self):
        truck_id = self.unlocked_trucks_panel.get_selected_truck_id()
        if not truck_id:
            QMessageBox.warning(self, DIALOG_WARNING_TITLE, WARNING_NO_TRUCK_SELECTED)
            return
        self._move_truck(truck_id, "lock")
    def _unlock_all(self):
        if QMessageBox.question(self, DIALOG_CONFIRM_TITLE, CONFIRM_UNLOCK_ALL) == QMessageBox.StandardButton.Yes:
            self._move_all_trucks("unlock")
    def _lock_all(self):
        if QMessageBox.question(self, DIALOG_CONFIRM_TITLE, CONFIRM_LOCK_ALL) == QMessageBox.StandardButton.Yes:
            self._move_all_trucks("lock")
    def _move_truck(self, truck_id, action):
        if not self.json_data:
            return
        ssl_value = self.json_data["SslValue"]
        locked_trucks = ssl_value.get("lockedTrucks", [])
        unlocked_trucks_dict = ssl_value.get("unlockedTrucks", {})
        map_ids = [map_id for map_id, _ in LEVELS_KNOWN]
        if action == "unlock":
            if truck_id in locked_trucks:
                locked_trucks.remove(truck_id)
            for map_id in map_ids:
                unlocked_trucks = unlocked_trucks_dict.get(map_id, [])
                if truck_id not in unlocked_trucks:
                    unlocked_trucks.append(truck_id)
                unlocked_trucks_dict[map_id] = sorted(unlocked_trucks)
        else:
            for map_id in map_ids:
                unlocked_trucks = unlocked_trucks_dict.get(map_id, [])
                if truck_id in unlocked_trucks:
                    unlocked_trucks.remove(truck_id)
                unlocked_trucks_dict[map_id] = sorted(unlocked_trucks)
            if truck_id not in locked_trucks:
                locked_trucks.append(truck_id)
        ssl_value["lockedTrucks"] = sorted(locked_trucks)
        ssl_value["unlockedTrucks"] = unlocked_trucks_dict
        self._populate_save_data()
        action_text = STATUS_TRUCK_UNLOCKED if action == "unlock" else STATUS_TRUCK_LOCKED
        self.status.showMessage(f"{action_text}: {self.trucks_data.get_display_name(truck_id)}")
    def _move_all_trucks(self, action):
        if not self.json_data:
            return
        ssl_value = self.json_data["SslValue"]
        map_ids = [map_id for map_id, _ in LEVELS_KNOWN]
        all_trucks = list(self.trucks_data.get_all_trucks().keys())
        if action == "unlock":
            ssl_value["lockedTrucks"] = []
            if "unlockedTrucks" not in ssl_value:
                ssl_value["unlockedTrucks"] = {}
            for map_id in map_ids:
                ssl_value["unlockedTrucks"][map_id] = sorted(all_trucks)
        else:
            ssl_value["lockedTrucks"] = sorted(all_trucks)
            if "unlockedTrucks" not in ssl_value:
                ssl_value["unlockedTrucks"] = {}
            for map_id in map_ids:
                ssl_value["unlockedTrucks"][map_id] = []
        self._populate_save_data()
        action_text = STATUS_ALL_TRUCKS_UNLOCKED if action == "unlock" else STATUS_ALL_TRUCKS_LOCKED
        self.status.showMessage(action_text)
    def _init_stats_tab(self):
        layout = QVBoxLayout(self.stats_tab)
        layout.setContentsMargins(*StyleManager.PANEL_MARGINS)
        self.stats_panel = StatsPanel()
        layout.addWidget(self.stats_panel)
        layout.addStretch(1)
    def _init_levels_tab(self):
        layout = QVBoxLayout(self.levels_tab)
        layout.setContentsMargins(*StyleManager.PANEL_MARGINS)
        self.levels_panel = LevelsPanel()
        self.levels_panel.unlock_all_btn.clicked.connect(self._levels_unlock_all)
        self.levels_panel.lock_all_btn.clicked.connect(self._levels_lock_all)
        self.levels_panel.complete_all_btn.clicked.connect(self._levels_complete_all)
        self.levels_panel.set_progress_btn.clicked.connect(self._levels_set_all_progress)
        layout.addWidget(self.levels_panel)
        self._levels_known = LEVELS_KNOWN
        self.levels_widgets = []
    def _init_settings_tab(self):
        layout = QVBoxLayout(self.settings_tab)
        layout.setContentsMargins(*StyleManager.PANEL_MARGINS)
        layout.setSpacing(StyleManager.PANEL_SPACING)
        settings_panel = QFrame()
        settings_panel.setObjectName("settingsPanel")
        settings_panel.setStyleSheet(StyleManager.get_style('panel'))
        settings_layout = QFormLayout(settings_panel)
        settings_layout.setSpacing(StyleManager.FORM_LAYOUT_SPACING)
        settings_layout.setContentsMargins(*StyleManager.PANEL_MARGINS)
        settings_title = QLabel(LABEL_SETTINGS_TITLE)
        settings_title.setStyleSheet(StyleManager.get_style('settings_title_label'))
        settings_layout.addRow(settings_title)
        self.auto_backup_cb = QCheckBox(LABEL_AUTO_BACKUP)
        self.auto_backup_cb.setStyleSheet(StyleManager.get_style('checkbox'))
        self.auto_backup_cb.setChecked(self.config.get("auto_backup", True))
        self.auto_backup_cb.stateChanged.connect(self._save_settings)
        self.backup_count_spin = QSpinBox()
        self.backup_count_spin.setMinimum(1)
        self.backup_count_spin.setMaximum(20)
        self.backup_count_spin.setValue(self.config.get("backup_count", 5))
        self.backup_count_spin.setStyleSheet(StyleManager.get_style('spinbox'))
        self.backup_count_spin.valueChanged.connect(self._save_settings)
        backups_label = QLabel(LABEL_MAX_BACKUPS)
        backups_label.setStyleSheet(StyleManager.get_style('form_label'))
        settings_layout.addRow(self.auto_backup_cb)
        settings_layout.addRow(backups_label, self.backup_count_spin)
        about_panel = QFrame()
        about_panel.setObjectName("aboutPanel")
        about_panel.setStyleSheet(StyleManager.get_style('panel'))
        about_layout = QVBoxLayout(about_panel)
        about_title = QLabel(LABEL_ABOUT_TITLE)
        about_title.setStyleSheet(StyleManager.get_style('about_title_label'))
        about_content = QLabel()
        about_content.setTextFormat(Qt.TextFormat.RichText)
        about_content.setOpenExternalLinks(True)
        about_content.setText(LABEL_ABOUT_CONTENT)
        about_content.setStyleSheet(StyleManager.get_style('about_content_label'))
        about_content.setWordWrap(True)
        about_content.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        about_layout.addWidget(about_title)
        about_layout.addWidget(about_content)
        about_layout.addStretch(1)
        layout.addWidget(settings_panel)
        layout.addWidget(about_panel)
        layout.addStretch(1)
    def _browse_save_file(self):
        if os.path.exists(ROADCRAFT_SAVE_PATH):
            start_dir = ROADCRAFT_SAVE_PATH
        else:
            start_dir = ""
        file_path, _ = QFileDialog.getOpenFileName(self, DIALOG_SELECT_SAVE_TITLE, start_dir, DIALOG_SELECT_SAVE_FILTER)
        if file_path:
            self.current_save_path = file_path
            self.file_entry.setText(file_path)
            self._load_save()
    def _load_save(self):
        if not self.current_save_path:
            QMessageBox.critical(self, DIALOG_ERROR_TITLE, ERROR_SELECT_SAVE_FILE)
            return
        progress = ProgressDialog(self, DIALOG_LOADING_TITLE, DIALOG_LOADING_MESSAGE)
        progress.show()
        QApplication.processEvents()
        try:
            progress.update_progress(10, DIALOG_LOADING_READING)
            self.original_file_content, decompressed_data = self.save_manager.decode_file(self.current_save_path)
            if decompressed_data is None:
                raise Exception(ERROR_DECOMPRESS_SAVE)
            progress.update_progress(60, DIALOG_LOADING_PARSING)
            self.json_data = json.loads(decompressed_data.decode('utf-8'))
            progress.update_progress(80, DIALOG_LOADING_VALIDATING)
            warnings = self.save_manager.validate_save_data(self.json_data)
            if warnings:
                pass
            progress.update_progress(100, DIALOG_LOADING_COMPLETE)
            self._populate_save_data()
            self.status.showMessage(STATUS_LOAD_SUCCESS)
            self.save_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, DIALOG_ERROR_TITLE, ERROR_LOAD_SAVE.format(error=e))
            self.status.showMessage(STATUS_LOAD_FAIL.format(error=e))
        progress.close()
    def _populate_save_data(self):
        if not self.json_data:
            return
        ssl_value = self.json_data.get("SslValue", {})
        locked_trucks = ssl_value.get("lockedTrucks", [])
        unlocked_trucks_dict = ssl_value.get("unlockedTrucks", {})
        unlocked_trucks = sorted(set(truck for trucks in unlocked_trucks_dict.values() for truck in trucks))
        self.locked_trucks_panel.populate_trucks(locked_trucks, self.trucks_data.get_display_name)
        self.unlocked_trucks_panel.populate_trucks(unlocked_trucks, self.trucks_data.get_display_name)
        stats_data = {
            'money': ssl_value.get("money", 0),
            'xp': ssl_value.get("xp", 0),
            'companyName': ssl_value.get("companyName", "")
        }
        self.stats_panel.set_stats_data(stats_data)
        completed = set(ssl_value.get("completedLevels", []))
        unlocked = set(ssl_value.get("unlockedLevels", []))
        progress = ssl_value.get("levelsProgress", {})
        recovery_coins = ssl_value.get("recoveryCoins", {})
        fobs_resources = ssl_value.get("fobsResources", {})
        self.levels_panel.levels_table.setRowCount(len(self._levels_known))
        self.levels_widgets.clear()
        for row, (level_id, level_name) in enumerate(self._levels_known):
            name_item = QTableWidgetItem(level_name)
            name_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            unlocked_cb = QCheckBox()
            unlocked_cb.setChecked(level_id in unlocked)
            completed_cb = QCheckBox()
            completed_cb.setChecked(level_id in completed)
            prog_spin = StyleManager.create_table_cell_spinbox(0, 100, progress.get(level_id, 0))
            fuel_spin = StyleManager.create_table_cell_spinbox(0, 9999, recovery_coins.get(level_id, 0))
            fob_vals = []
            if level_id in fobs_resources and "resources" in fobs_resources[level_id]:
                fob_vals = fobs_resources[level_id]["resources"]
                if len(fob_vals) < 8:
                    fob_vals += [0] * (8 - len(fob_vals))
            else:
                fob_vals = [0] * 8
                pass
            logs_spin = StyleManager.create_table_cell_spinbox(0, 999999, fob_vals[RESOURCE_INDEX['LOGS']])
            steel_beams_spin = StyleManager.create_table_cell_spinbox(0, 999999, fob_vals[RESOURCE_INDEX['STEEL_BEAMS']])
            concrete_slabs_spin = StyleManager.create_table_cell_spinbox(0, 9999, fob_vals[RESOURCE_INDEX['CONCRETE_SLABS']])
            steel_pipes_spin = StyleManager.create_table_cell_spinbox(0, 999999, fob_vals[RESOURCE_INDEX['STEEL_PIPES']])
            self.levels_panel.levels_table.setItem(row, 0, name_item)
            self.levels_panel.levels_table.setCellWidget(row, 1, unlocked_cb)
            self.levels_panel.levels_table.setCellWidget(row, 2, completed_cb)
            self.levels_panel.levels_table.setCellWidget(row, 3, prog_spin)
            self.levels_panel.levels_table.setCellWidget(row, 4, fuel_spin)
            self.levels_panel.levels_table.setCellWidget(row, 5, logs_spin)
            self.levels_panel.levels_table.setCellWidget(row, 6, steel_beams_spin)
            self.levels_panel.levels_table.setCellWidget(row, 7, concrete_slabs_spin)
            self.levels_panel.levels_table.setCellWidget(row, 8, steel_pipes_spin)
            self.levels_widgets.append((level_id, unlocked_cb, completed_cb, prog_spin, fuel_spin, logs_spin, steel_beams_spin, concrete_slabs_spin, steel_pipes_spin))
    def _save_changes(self):
        if not self.json_data:
            return
        if self.original_file_content is None or self.current_save_path is None:
            QMessageBox.critical(self, DIALOG_ERROR_TITLE, ERROR_MISSING_ORIGINAL_FILE_OR_PATH)
            self.status.showMessage(STATUS_SAVE_FAIL.format(error="missing file content or path"))
            return
        progress = ProgressDialog(self, DIALOG_SAVING_CHANGES_TITLE, DIALOG_SAVING_CHANGES_MESSAGE)
        progress.show()
        QApplication.processEvents()
        try:
            ssl_value = self.json_data["SslValue"]
            new_locked_trucks = self.locked_trucks_panel.get_all_truck_ids()
            ssl_value["lockedTrucks"] = sorted(new_locked_trucks)
            new_unlocked_trucks = self.unlocked_trucks_panel.get_all_truck_ids()
            if "unlockedTrucks" not in ssl_value:
                ssl_value["unlockedTrucks"] = {}
            for map_id, _ in LEVELS_KNOWN:
                ssl_value["unlockedTrucks"][map_id] = sorted(new_unlocked_trucks)
            if "newUnlockedTrucks" in ssl_value:
                if not new_unlocked_trucks:
                    for truck in ssl_value.get("newUnlockedTrucks", []):
                        if truck not in ssl_value["lockedTrucks"]:
                            ssl_value["lockedTrucks"].append(truck)
                    ssl_value["lockedTrucks"] = sorted(set(ssl_value["lockedTrucks"]))
                    ssl_value["newUnlockedTrucks"] = []
                else:
                    ssl_value["newUnlockedTrucks"] = sorted(new_unlocked_trucks)
            stats_data = self.stats_panel.get_stats_data()
            ssl_value["money"] = stats_data['money']
            ssl_value["xp"] = stats_data['xp']
            ssl_value["companyName"] = stats_data['company_name']
            if hasattr(self, 'levels_widgets'):
                unlocked = []
                completed = []
                level_progress = {}
                recovery_coins = {}
                fobs_resources = {}
                for (level_id, unlocked_cb, completed_cb, prog_spin, fuel_spin, logs_spin, steel_beams_spin, concrete_slabs_spin, steel_pipes_spin) in self.levels_widgets:
                    if unlocked_cb.isChecked():
                        unlocked.append(level_id)
                    if completed_cb.isChecked():
                        completed.append(level_id)
                    level_progress[level_id] = prog_spin.value()
                    recovery_coins[level_id] = fuel_spin.value()
                    res_list = [0]*8
                    if level_id in self.json_data["SslValue"].get("fobsResources", {}) and "resources" in self.json_data["SslValue"]["fobsResources"][level_id]:
                        res_list = self.json_data["SslValue"]["fobsResources"][level_id]["resources"]
                        if len(res_list) < 8:
                            res_list += [0]*(8-len(res_list))
                    res_list[RESOURCE_INDEX['LOGS']] = logs_spin.value()
                    res_list[RESOURCE_INDEX['STEEL_BEAMS']] = steel_beams_spin.value()
                    res_list[RESOURCE_INDEX['CONCRETE_SLABS']] = concrete_slabs_spin.value()
                    res_list[RESOURCE_INDEX['STEEL_PIPES']] = steel_pipes_spin.value()
                    fobs_resources[level_id] = {"resources": res_list}
                self.json_data["SslValue"]["unlockedLevels"] = unlocked
                self.json_data["SslValue"]["completedLevels"] = completed
                self.json_data["SslValue"]["levelsProgress"] = level_progress
                self.json_data["SslValue"]["recoveryCoins"] = recovery_coins
                self.json_data["SslValue"]["fobsResources"] = fobs_resources
            progress.update_progress(90, DIALOG_SAVE_PROGRESS)
            decompressed_data_bytes = json.dumps(self.json_data, separators=(",", ":")).encode('utf-8')
            self.save_manager.encode_file(self.original_file_content[:53], decompressed_data_bytes, self.current_save_path)
            progress.update_progress(100, DIALOG_SAVE_COMPLETE)
            self.status.showMessage(STATUS_SAVE_SUCCESS)
        except Exception as e:
            QMessageBox.critical(self, DIALOG_ERROR_TITLE, ERROR_SAVE_CHANGES.format(error=e))
            self.status.showMessage(STATUS_SAVE_FAIL.format(error=e))
        progress.close()
    def _save_settings(self):
        self.config.set("auto_backup", self.auto_backup_cb.isChecked())
        self.config.set("backup_count", self.backup_count_spin.value())
    def _levels_unlock_all(self):
        for _, unlocked_cb, _, _, _, _, _, _, _ in self.levels_widgets:
            unlocked_cb.setChecked(True)
    def _levels_lock_all(self):
        for _, unlocked_cb, _, _, _, _, _, _, _ in self.levels_widgets:
            unlocked_cb.setChecked(False)
    def _levels_complete_all(self):
        for _, _, completed_cb, _, _, _, _, _, _ in self.levels_widgets:
            completed_cb.setChecked(True)
    def _levels_set_all_progress(self):
        value = self.levels_panel.progress_spin.value()
        for _, _, _, prog_spin, _, _, _, _, _ in self.levels_widgets:
            prog_spin.setValue(value)
    def mousePressEvent(self, a0):
        if a0 is not None and a0.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = a0.globalPosition().toPoint() - self.frameGeometry().topLeft()
            a0.accept()
    def mouseMoveEvent(self, a0):
        if a0 is not None and self._drag_pos is not None and a0.buttons() & Qt.MouseButton.LeftButton:
            self.move(a0.globalPosition().toPoint() - self._drag_pos)
            a0.accept()
    def mouseReleaseEvent(self, a0):
        self._drag_pos = None
        if a0 is not None:
            a0.accept()
class BasePanel(QFrame):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("basePanel")
        self.setStyleSheet(StyleManager.get_style('panel'))
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(*StyleManager.PANEL_MARGINS)
        self.main_layout.setSpacing(StyleManager.PANEL_SPACING)
        if title:
            self.title_label = StyleManager.create_title_label(title)
            self.main_layout.addWidget(self.title_label)
    def add_widget(self, widget):
        self.main_layout.addWidget(widget)
    def add_layout(self, layout):
        self.main_layout.addLayout(layout)
    def add_stretch(self, stretch: int = 1):
        self.main_layout.addStretch(stretch)
class QuickButtonPanel(BasePanel):
    def __init__(self, title: str = LABEL_QUICK_ACTIONS, parent=None):
        super().__init__(title, parent)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(StyleManager.QUICK_BUTTONS_SPACING)
        self.add_layout(self.buttons_layout)
    def add_button(self, text: str, callback, action_button: bool = False):
        button = StyleManager.create_button(text, action_button)
        button.clicked.connect(callback)
        self.buttons_layout.addWidget(button)
        return button
class TruckDetailsPanel(BasePanel):
    def __init__(self, parent=None):
        super().__init__(LABEL_TRUCK_DETAILS, parent)
        self.setMaximumWidth(StyleManager.TRUCK_DETAILS_MAX_WIDTH)
        outer_container = QVBoxLayout()
        outer_container.setContentsMargins(0, 0, 0, 0)
        outer_container.setSpacing(0)
        outer_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_container = QFrame()
        image_container.setFixedSize(*StyleManager.TRUCK_IMAGE_CONTAINER_SIZE)
        image_container.setObjectName("imageContainer")
        image_container.setStyleSheet(StyleManager.get_truck_frame_stylesheet())
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(0)
        image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.truck_image_label = QLabel()
        self.truck_image_label.setFixedSize(*StyleManager.TRUCK_IMAGE_LABEL_SIZE)
        self.truck_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.truck_image_label.setStyleSheet(
            StyleManager.get_style('panel') +
            "background: transparent; background-position: center; background-repeat: no-repeat;"
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(StyleManager.DARK_THEME['background']))
        shadow.setOffset(0, 0)
        self.truck_image_label.setGraphicsEffect(shadow)
        image_layout.addWidget(self.truck_image_label, 0, Qt.AlignmentFlag.AlignCenter)
        outer_container.addWidget(image_container, 0, Qt.AlignmentFlag.AlignCenter)


        label_width = 220
        self.truck_name_label = QLabel()
        self.truck_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.truck_name_label.setStyleSheet(StyleManager.get_style('truck_details_small_label') + "margin-top: 12px; text-align: center;")
        self.truck_name_label.setFixedWidth(label_width)
        outer_container.addWidget(self.truck_name_label, 0, Qt.AlignmentFlag.AlignCenter)

        outer_container.addSpacing(12)

        details_frame = QFrame()
        details_frame.setObjectName("detailsFrame")
        details_frame.setStyleSheet(StyleManager.get_truck_frame_stylesheet())
        details_frame_layout = QVBoxLayout(details_frame)
        details_frame_layout.setContentsMargins(8, 4, 8, 4)
        details_frame_layout.setSpacing(2)
        self.truck_details_label = QLabel()

        self.truck_details_label.setStyleSheet("color: #fff; background: transparent; border: none; font-size: 13px; font-family: 'Segoe UI', Arial, sans-serif;")
        self.truck_details_label.setFixedWidth(label_width)
        self.truck_details_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.truck_details_label.setWordWrap(True)
        details_frame_layout.addWidget(self.truck_details_label)
        outer_container.addWidget(details_frame, 0, Qt.AlignmentFlag.AlignCenter)
        outer_container.addStretch(1)
        self.main_layout.addLayout(outer_container)

    def update_truck_details(self, truck_data: dict, image_path: str = ""):
        self.truck_name_label.setText(truck_data.get('display_name', 'Unknown'))
        details = f"Type: {truck_data.get('type', 'Unknown')}\n"
        details += f"Rarity: {truck_data.get('rarity', 'Unknown')}\n"
        details += f"ID: {truck_data.get('id', 'Unknown')}"
        self.truck_details_label.setText(details)
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                180, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.truck_image_label.setPixmap(pixmap)
            self.truck_image_label.setText("")
        else:
            self.truck_image_label.setText("No image\navailable")
            self.truck_image_label.setPixmap(QPixmap())
            self.truck_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
class TruckListPanel(BasePanel):
    selectionChanged = pyqtSignal(str)
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
        self.list_widget = QListWidget()
        StyleManager.apply_list_style(self.list_widget)
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        self.add_widget(self.list_widget)
    def _on_selection_changed(self):
        items = self.list_widget.selectedItems()
        if items:
            truck_id = items[0].data(Qt.ItemDataRole.UserRole)
            self.selectionChanged.emit(truck_id)
    def clear_selection(self):
        self.list_widget.clearSelection()
    def populate_trucks(self, trucks: list, display_name_func):
        self.list_widget.clear()
        for truck_id in trucks:
            item = QListWidgetItem(display_name_func(truck_id))
            item.setData(Qt.ItemDataRole.UserRole, truck_id)
            self.list_widget.addItem(item)
    def get_selected_truck_id(self) -> str | None:
        items = self.list_widget.selectedItems()
        return items[0].data(Qt.ItemDataRole.UserRole) if items else None
    def get_all_truck_ids(self) -> list:
        truck_ids = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None:
                truck_id = item.data(Qt.ItemDataRole.UserRole)
                if truck_id is not None:
                    truck_ids.append(truck_id)
        return truck_ids
class TruckActionPanel(QFrame):
    unlockSelected = pyqtSignal()
    lockSelected = pyqtSignal()
    unlockAll = pyqtSignal()
    lockAll = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(StyleManager.TRUCK_ACTION_PANEL_WIDTH)
        self.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*StyleManager.TRUCK_ACTION_PANEL_MARGINS)
        self.unlock_selected_btn = StyleManager.create_button(BUTTON_UNLOCK_SELECTED)
        self.unlock_selected_btn.clicked.connect(self.unlockSelected.emit)
        self.lock_selected_btn = StyleManager.create_button(BUTTON_LOCK_SELECTED)
        self.lock_selected_btn.clicked.connect(self.lockSelected.emit)
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(StyleManager.get_style('panel'))
        self.unlock_all_btn = StyleManager.create_button(BUTTON_UNLOCK_ALL_CAPS)
        self.unlock_all_btn.clicked.connect(self.unlockAll.emit)
        self.lock_all_btn = StyleManager.create_button(BUTTON_LOCK_ALL_CAPS)
        self.lock_all_btn.clicked.connect(self.lockAll.emit)
        layout.addStretch(1)
        layout.addWidget(self.unlock_selected_btn)
        layout.addWidget(self.lock_selected_btn)
        layout.addSpacing(40)
        layout.addWidget(separator)
        layout.addSpacing(40)
        layout.addWidget(self.unlock_all_btn)
        layout.addWidget(self.lock_all_btn)
        layout.addStretch(1)
class StatsPanel(BasePanel):
    def __init__(self, parent=None):
        super().__init__(LABEL_PLAYER_STATS, parent)
        form_layout = QFormLayout()
        form_layout.setSpacing(StyleManager.FORM_LAYOUT_SPACING)
        self.money_entry = StyleManager.create_input_field(PLACEHOLDER_MONEY)
        self.xp_entry = StyleManager.create_input_field(PLACEHOLDER_XP) 
        self.company_name_entry = StyleManager.create_input_field(PLACEHOLDER_COMPANY)
        money_label = QLabel(LABEL_MONEY)
        money_label.setStyleSheet(StyleManager.get_style('form_label'))
        xp_label = QLabel(LABEL_XP)
        xp_label.setStyleSheet(StyleManager.get_style('form_label'))
        company_label = QLabel(LABEL_COMPANY_NAME)
        company_label.setStyleSheet(StyleManager.get_style('form_label'))
        form_layout.addRow(money_label, self.money_entry)
        form_layout.addRow(xp_label, self.xp_entry)
        form_layout.addRow(company_label, self.company_name_entry)
        self.add_layout(form_layout)
        quick_panel = QuickButtonPanel(LABEL_QUICK_ACTIONS)
        quick_panel.add_button(BUTTON_100K, lambda: self.money_entry.setText("100000"))
        quick_panel.add_button(BUTTON_500K, lambda: self.money_entry.setText("500000"))
        quick_panel.add_button(BUTTON_1M, lambda: self.money_entry.setText("1000000"))
        quick_panel.add_button(BUTTON_MAX_XP, lambda: self.xp_entry.setText("999999"))
        self.add_widget(quick_panel)
        self.add_stretch()
    def get_stats_data(self) -> dict:
        return {
            'money': int(self.money_entry.text() or 0),
            'xp': int(self.xp_entry.text() or 0),
            'company_name': self.company_name_entry.text() or ""
        }
    def set_stats_data(self, data: dict):
        self.money_entry.setText(str(data.get('money', 0)))
        self.xp_entry.setText(str(data.get('xp', 0)))
        self.company_name_entry.setText(data.get('companyName', ''))
class LevelsPanel(BasePanel):
    TABLE_COLUMNS = [
        LABEL_LEVEL_NAME, LABEL_UNLOCKED, LABEL_COMPLETED, LABEL_PROGRESS_PERCENT,
        LABEL_FUEL, LABEL_LOGS, LABEL_STEEL_BEAMS, LABEL_CONCRETE_SLABS, LABEL_STEEL_PIPES
    ]
    COLUMN_COUNT = len(TABLE_COLUMNS)
    COLUMN_WIDTHS = StyleManager.LEVELS_TABLE_COLUMN_WIDTHS
    def __init__(self, parent=None):
        super().__init__(LABEL_LEVEL_OPERATIONS, parent)
        controls_grid = QGridLayout()
        controls_grid.setSpacing(StyleManager.QUICK_BUTTONS_SPACING)
        self.unlock_all_btn = StyleManager.create_button(BUTTON_UNLOCK_ALL)
        self.lock_all_btn = StyleManager.create_button(BUTTON_LOCK_ALL)
        self.complete_all_btn = StyleManager.create_button(BUTTON_COMPLETE_ALL)
        progress_label = QLabel(LABEL_PROGRESS)
        progress_label.setStyleSheet(StyleManager.get_style('form_label'))
        self.progress_spin = StyleManager.create_spinbox(0, 100, 100)
        self.set_progress_btn = StyleManager.create_button(BUTTON_SET_ALL_PROGRESS)
        controls_grid.addWidget(self.unlock_all_btn, 0, 0)
        controls_grid.addWidget(self.lock_all_btn, 0, 1)
        controls_grid.addWidget(self.complete_all_btn, 0, 2)
        controls_grid.addWidget(progress_label, 1, 0)
        controls_grid.addWidget(self.progress_spin, 1, 1)
        controls_grid.addWidget(self.set_progress_btn, 1, 2)
        self.add_layout(controls_grid)
        self.levels_table = QTableWidget()
        self._setup_levels_table()
        self.add_widget(self.levels_table)
    def _setup_levels_table(self):
        from PyQt6.QtWidgets import QHeaderView, QTableWidget, QCheckBox
        from PyQt6.QtGui import QColor, QFont
        from PyQt6.QtCore import Qt
        if self.levels_table is None:
            self.levels_table = QTableWidget(self)
        self.levels_table.clear()
        self.levels_table.setColumnCount(self.COLUMN_COUNT)
        self.levels_table.setRowCount(0)
        header = self.levels_table.horizontalHeader()
        if header is not None:
            header.setVisible(True)
            header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            header.setDefaultSectionSize(StyleManager.LEVELS_TABLE_COLUMN_WIDTHS[0])
            header.setMinimumSectionSize(100)
            header.setHighlightSections(True)
            header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setFixedHeight(StyleManager.LEVELS_TABLE_HEADER_HEIGHT)
        vertical_header = self.levels_table.verticalHeader()
        if vertical_header:
            vertical_header.setVisible(False)
            vertical_header.setDefaultSectionSize(StyleManager.LEVELS_TABLE_ROW_HEIGHT)
        header_font = QFont()
        header_font.setPointSize(11)
        header_font.setBold(True)
        header_font.setFamily("Segoe UI")
        for col, header_text in enumerate(self.TABLE_COLUMNS):
            item = QTableWidgetItem(header_text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            item.setForeground(QColor(StyleManager.DARK_THEME['accent']))
            item.setBackground(QColor(StyleManager.DARK_THEME['panel_bg']))
            self.levels_table.setHorizontalHeaderItem(col, item)
            self.levels_table.setColumnWidth(col, self.COLUMN_WIDTHS[col])
        self.levels_table.setAlternatingRowColors(True)
        self.levels_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.levels_table.setShowGrid(False)
        self.levels_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.levels_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.levels_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        StyleManager.apply_table_style(self.levels_table)
        self.levels_table.setCornerButtonEnabled(False)
        self.levels_table.setWordWrap(False)
        self.levels_table.update()
        self.levels_table.show()
class SettingsPanel(BasePanel):
    def __init__(self, config, parent=None):
        super().__init__(LABEL_SETTINGS_TITLE, parent)
        form_layout = QFormLayout()
        form_layout.setSpacing(StyleManager.FORM_LAYOUT_SPACING)
        self.auto_backup_cb = QCheckBox()
        self.auto_backup_cb.setChecked(config.get('auto_backup', True))
        self.backup_count_spinbox = QSpinBox()
        self.backup_count_spinbox.setMinimum(1)
        self.backup_count_spinbox.setMaximum(20)
        self.backup_count_spinbox.setValue(config.get('backup_count', BACKUP_MAX_COUNT))
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Dark")
        self.theme_combo.setCurrentText(config.get('theme', 'dark').capitalize())
        auto_backup_label = QLabel(LABEL_AUTO_BACKUP)
        auto_backup_label.setStyleSheet(StyleManager.get_style('form_label'))
        max_backups_label = QLabel(LABEL_MAX_BACKUPS)
        max_backups_label.setStyleSheet(StyleManager.get_style('form_label'))
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet(StyleManager.get_style('form_label'))
        form_layout.addRow(auto_backup_label, self.auto_backup_cb)
        form_layout.addRow(max_backups_label, self.backup_count_spinbox)
        form_layout.addRow(theme_label, self.theme_combo)
        self.add_layout(form_layout)
def main():
    app = QApplication(sys.argv)
    StyleManager.apply_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
