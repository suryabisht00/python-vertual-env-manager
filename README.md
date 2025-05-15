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

### Quick Build (Recommended)

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
└── Direct_exe_prebuild/
      └── PyVenvManager.exe   # <--- Prebuilt EXE (if provided)
```

- The generated executable will be located at:
  ```
  dist\PyVenvManager.exe
  ```
- A prebuilt executable is also available in the `Direct_exe_prebuild` folder:
  ```
  Direct_exe_prebuild\PyVenvManager.exe
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
