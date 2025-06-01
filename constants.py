import os

WINDOW_TITLE = "Save Editor"

CONFIG_DIR_NAME = ".roadcraft_editor"
CONFIG_FILE_NAME = "config.json"
IMAGES_DIR_NAME = "images"
UI_IMAGES_DIR_NAME = "ui"

RESOURCE_INDEX = {
    'LOGS': 4,
    'STEEL_BEAMS': 5,
    'CONCRETE_SLABS': 6,
    'STEEL_PIPES': 7
}

ZLIB_HEADER = b'\x78\x9c'

DEFAULT_TRUCKS_MAP_ID = "rb_map_02_storm_aftermath"
LEVELS_KNOWN = [
    ("rb_map_01_storm_preparation", "Storm Preparation"),
    ("rb_map_02_storm_aftermath", "Storm Aftermath"),
    ("rb_map_03_incommunicado", "Incommunicado"),
    ("rb_map_04_salt_mines", "Salt Mines"),
    ("rb_map_05_dam_break", "Dam Break"),
    ("rb_map_06_sinkholes", "Sinkholes"),
    ("rb_map_09_sand_storm", "Sand Storm"),
    ("rb_map_10_geothermal", "Geothermal"),
]

BACKUP_FILE_PATTERN = "CompleteSave_backup_{timestamp}.bak"
BACKUP_MAX_COUNT = 5

STATUS_READY = "Ready. Open a CompleteSave file to begin."
STATUS_SAVE_SUCCESS = "Changes saved successfully"
STATUS_SAVE_FAIL = "Save failed: {error}"
STATUS_LOAD_SUCCESS = "Save file loaded successfully"
STATUS_LOAD_FAIL = "Load failed: {error}"
WARNING_NO_TRUCK_SELECTED = "No truck selected"
CONFIRM_UNLOCK_ALL = "Unlock all trucks?"
CONFIRM_LOCK_ALL = "Lock all trucks?"

LABEL_MONEY = "Money:"
LABEL_XP = "Experience Points:"
LABEL_COMPANY_NAME = "Company Name:"
LABEL_PROGRESS = "Progress:"
LABEL_QUICK_ACTIONS = "Quick Actions"
LABEL_PLAYER_STATS = "Player Statistics"
LABEL_LEVEL_OPERATIONS = "Level Operations"
LABEL_TRUCK_DETAILS = "TRUCK DETAILS"
LABEL_SETTINGS = "Settings"
LABEL_LEVEL_NAME = "Level Name"
LABEL_UNLOCKED = "Unlocked"
LABEL_COMPLETED = "Completed"
LABEL_PROGRESS_PERCENT = "Progress (%)"
LABEL_FUEL = "Fuel"
LABEL_LOGS = "Logs"
LABEL_STEEL_BEAMS = "Steel Beams"
LABEL_CONCRETE_SLABS = "Concrete Slabs"
LABEL_STEEL_PIPES = "Steel Pipes"
LABEL_SAVE_FILE = "Save File:"
LABEL_AUTO_BACKUP = "Auto-create backups when saving"
LABEL_MAX_BACKUPS = "Maximum backups to keep:"
LABEL_SETTINGS_TITLE = "Application Settings"
LABEL_ABOUT_TITLE = "About RoadCraft Save Editor"
LABEL_ABOUT_CONTENT = (
    "<b>RoadCraft Save Editor</b> is a modern, user-friendly save file editor for the game RoadCraft.<br>"
    "<br>"
    "<b>Github</b> <a href='https://github.com/RifaiV/roadcraft-save-editor' style='color:#FFCC00;'>RifaiV/roadcraft-save-editor</a><br>"
    "<br>"
    "Unlock trucks, edit player stats, unlock levels,<br>"
    "<br>"
    "<i>Not affiliated with Saber Interactive. Use at your own risk.</i>"
)

LABEL_LOCKED_TRUCKS = "Locked Trucks"
LABEL_UNLOCKED_TRUCKS = "Unlocked Trucks"

BUTTON_UNLOCK_ALL = "Unlock All"
BUTTON_LOCK_ALL = "Lock All"
BUTTON_COMPLETE_ALL = "Complete All"
BUTTON_SET_ALL_PROGRESS = "Set All Progress"
BUTTON_UNLOCK_SELECTED = "Unlock →"
BUTTON_LOCK_SELECTED = "← Lock"
BUTTON_UNLOCK_ALL_CAPS = "UNLOCK ALL →"
BUTTON_LOCK_ALL_CAPS = "← LOCK ALL"
BUTTON_100K = "$100K"
BUTTON_500K = "$500K"
BUTTON_1M = "$1M"
BUTTON_MAX_XP = "Max XP"
BUTTON_OPEN_SAVE_FILE = "Open Save File..."
BUTTON_SAVE_CHANGES = "Save Changes"

DIALOG_PROCESSING_TITLE = "Processing"
DIALOG_PROCESSING_MESSAGE = "Please wait..."

DIALOG_WARNING_TITLE = "Warning"
DIALOG_CONFIRM_TITLE = "Confirm"
DIALOG_ERROR_TITLE = "Error"
DIALOG_LOADING_TITLE = "Loading Save"
DIALOG_SELECT_SAVE_TITLE = "Select CompleteSave file"
DIALOG_SAVING_CHANGES_TITLE = "Saving Changes"

DIALOG_SELECT_SAVE_FILTER = "CompleteSave files (CompleteSave);;All files (*)"

STATUS_TRUCK_UNLOCKED = "Truck unlocked"
STATUS_TRUCK_LOCKED = "Truck locked"
STATUS_ALL_TRUCKS_UNLOCKED = "All trucks unlocked"
STATUS_ALL_TRUCKS_LOCKED = "All trucks locked"

TAB_TRUCKS = "Trucks"
TAB_PLAYER_STATS = "Player Stats"
TAB_LEVELS = "Levels"
TAB_SETTINGS = "Settings"

DIALOG_LOADING_READING = "Reading file..."
DIALOG_LOADING_PARSING = "Parsing JSON data..."
DIALOG_LOADING_VALIDATING = "Validating data..."
DIALOG_LOADING_COMPLETE = "Loading complete!"
DIALOG_SAVING_CHANGES_MESSAGE = "Saving changes to the save file..."
DIALOG_SAVE_PROGRESS = "Saving file..."
DIALOG_SAVE_COMPLETE = "Save complete!"

ERROR_SELECT_SAVE_FILE = "Please select a CompleteSave file"
ERROR_DECOMPRESS_SAVE = "Failed to decompress save file data"
ERROR_LOAD_SAVE = "Failed to load save file: {error}"
ERROR_MISSING_ORIGINAL_FILE_OR_PATH = "Missing original file content or save path. Please reload the save file."
ERROR_SAVE_CHANGES = "Failed to save changes: {error}"
ERROR_DECOMPRESS_BLOCK = "Failed to decompress block at file offset {offset}"
ERROR_READING_FILE = "Error reading file {file_path}: {error}"
ERROR_ENCODING = "Error during encoding: {error}"

WARNING_NO_TRUCK_SELECTED = "No truck selected"
CONFIRM_UNLOCK_ALL = "Unlock all trucks?"
CONFIRM_LOCK_ALL = "Lock all trucks?"
WARNING_MISSING_SSLVALUE = "Missing SslValue in save data"
WARNING_MISSING_FIELD = "Missing field: {field}"
WARNING_MONEY_NOT_NUMERIC = "Money field is not numeric"
WARNING_XP_NOT_NUMERIC = "XP field is not numeric"
WARNING_LOCKED_TRUCKS_NOT_LIST = "lockedTrucks is not a list"
WARNING_UNLOCKED_TRUCKS_NOT_DICT = "unlockedTrucks is not a dictionary"
WARNING_DECOMPRESSED_SIZE_MISMATCH = "Warning: Decompressed size ({actual}) != expected ({expected})"
WARNING_COMPRESSED_SIZE_MISMATCH = "Warning: Compressed bytes processed ({actual}) != expected ({expected})"

DIALOG_LOADING_MESSAGE = "Loading save file..."

PLACEHOLDER_MONEY = "Enter money amount"
PLACEHOLDER_XP = "Enter XP amount"
PLACEHOLDER_COMPANY = "Enter company name"

ROADCRAFT_SAVE_PATH = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Local", "Saber", "RoadCraftGame", "storage", "steam", "user"
)

