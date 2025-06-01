import os
import PyInstaller.__main__

# Application name
APP_NAME = "RoadCraft SaveEditor"

MAIN_SCRIPT = "main.py"
current_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(current_dir, "images", "ui", "icon.ico")

if not os.path.exists(icon_path):
    print(f"WARNING: Icon not found at: {icon_path}")
    print("Continuing without icon...")
    icon_path = None

args = [
    MAIN_SCRIPT,
    '--name=' + APP_NAME,
    '--onefile',
    '--windowed',
    '--clean',
    '--noconfirm',
    '--add-data=images;images',
]

if icon_path:
    args.append(f'--icon={icon_path}')

print("Starting PyInstaller build...")
PyInstaller.__main__.run(args)
print("Build complete!")