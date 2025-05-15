# Python Virtual Environment Manager

A GUI application to create, manage, and activate Python virtual environments with an easy-to-use interface.

## Features

- Create new Python virtual environments with various options
- Import existing virtual environments
- Activate environments in a new command prompt
- Automatically run main Python files when activating environments
- Manage environments (delete, refresh)
- Automatic detection of main Python files
- Customizable UI themes (Light/Dark)
- Customizable colors for user interface elements
- Threaded operations for responsive UI
- Settings persistence across sessions

## Requirements

- Python 3.6 or higher (with Tkinter, included by default in standard Python distributions)
- No external Python packages required to run
- See `requirement.txt` for build requirements

## How to Build the Executable (EXE)

### Quick Build on Windows (Recommended)

1. Make sure you have Python 3.6+ installed.
2. Install PyInstaller (only needed for building the EXE):
   ```powershell
   pip install pyinstaller
   ```
3. Run the following command in the project directory:
   ```powershell
   pyinstaller --onefile --windowed --icon=icon.ico PyVenvManager.py
   ```
   This will generate the standalone executable in the `dist` folder.

### Quick Build on Linux (All Distributions)

1. Make sure you have Python 3.6+ and Tkinter installed. For most distributions, install with:
   - **Debian/Ubuntu:**
     ```bash
     sudo apt update && sudo apt install python3 python3-tk
     ```
   - **Fedora:**
     ```bash
     sudo dnf install python3 python3-tkinter
     ```
   - **Arch Linux/Manjaro:**
     ```bash
     sudo pacman -S python python-tk
     ```
2. Install PyInstaller:
   ```bash
   pip3 install pyinstaller
   ```
3. (Optional) If you want an app icon, use a PNG icon (e.g., icon.png). Not all Linux desktops support .ico files.
4. Run the following command in the project directory:
   ```bash
   pyinstaller --onefile --windowed --icon=icon.ico PyVenvManager.py
   ```
   - If you get an error with the icon, try removing the `--icon=icon.ico` part or use a PNG icon: `--icon=icon.png`.
5. The standalone executable will be created in the `dist/` directory (e.g., `dist/PyVenvManager`).
6. Make the file executable if needed:
   ```bash
   chmod +x dist/PyVenvManager
   ```
7. Run the app:
   ```bash
   ./dist/PyVenvManager
   ```

**Note:** The Linux build must be done on a Linux system (or WSL). The Windows EXE will not run on Linux, and vice versa.

### Quick Build on macOS

1. Make sure you have Python 3.6+ and Tkinter installed. On most macOS systems, Tkinter is included by default. If not, you can install it with Homebrew:
   ```bash
   brew install python-tk
   ```
2. Install PyInstaller:
   ```bash
   pip3 install pyinstaller
   ```
3. (Optional) If you want an app icon, use a PNG or ICNS icon (e.g., icon.png or icon.icns). macOS does not support .ico files for app icons.
4. Run the following command in the project directory:
   ```bash
   pyinstaller --onefile --windowed --icon=icon.icns PyVenvManager.py
   ```
   - If you get an error with the icon, try removing the `--icon=icon.icns` part or use a PNG icon: `--icon=icon.png`.
5. The standalone executable will be created in the `dist/` directory (e.g., `dist/PyVenvManager`).
6. Make the file executable if needed:
   ```bash
   chmod +x dist/PyVenvManager
   ```
7. Run the app:
   ```bash
   ./dist/PyVenvManager
   ```

**Note:** The macOS build must be done on a Mac. The Windows EXE and Linux binary will not run on macOS, and vice versa.

### Output EXE File

After building, your project directory structure will look like this:

```
project-root/
│   PyVenvManager.py
│   README.md
│   requirement.txt
│   icon.ico
├── dist/
│     └── PyVenvManager.exe   # <--- Generated EXE after build
└── Os_name_Prebuild/
      └── PyVenvManager.exe   # <--- Prebuilt EXE (if provided) 
```
### Os_name_Prebuild such as windows_prebuild(folder), same linux_prebuild(folder) and mac_prebuild(folder)

- The generated executable will be located at:
  ```
  dist\PyVenvManager.exe
  ```
- A prebuilt executable is also available in the `Os_name_Prebuild` folder:
  ```
  Os_name_Prebuild\PyVenvManager.exe
  ```
- You can move this file anywhere and double-click to run the application. No installation is required.

### Notes
- The `icon.ico` file is used for the application icon. If you want to change it, replace `icon.ico` in the project directory.
- No external dependencies are required for running the EXE; all modules are from the Python standard library.

## Quick Start

### Run the Executable Directly

1. Download or clone this repository.
2. In the `dist` folder, locate `PyVenvManager.exe` (or use the provided `PyVenvManager.exe` in the root if available).
3. Double-click `PyVenvManager.exe` to launch the application.  
   *No installation or setup required.*

### Select UI Theme

- After launching the application, go to the Settings tab.
- Choose your preferred UI theme (Light/Dark) and customize colors as desired.

## Usage

1. Launch the application (see "Quick Start" above to run the EXE directly).
2. Use the "Create New" button to create a new virtual environment:
   - Enter a name for the environment
   - Select a Python executable (optional)
   - Specify additional packages to install (optional)
   - Set options like system site packages
3. Select an environment from the list and click "Activate" to use it in a new terminal
4. Use the "Import" button to import existing virtual environments from other locations
5. Use the Settings tab to:
   - Change the directory where environments are stored
   - Select a default Python executable
   - Customize themes and colors

## Customization

The application allows customizing:
- Theme (Light/Dark mode)
- UI colors (primary, secondary, background, text, accent)
- Default Python executable
- Environment storage location

## Requirements File

A `requirement.txt` file is included for reference.  
No external dependencies are required to run; all modules are from the Python standard library.  
To build the EXE, install `pyinstaller` as listed in `requirement.txt`.

## License

MIT License - Feel free to modify and distribute as needed.
