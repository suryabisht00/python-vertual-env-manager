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

## Installation

### Windows Installer (Recommended)

1. Download the latest installer (PyVenvManagerSetup.exe) from the releases page
2. Run the installer and follow the instructions
3. Launch the application from the Start Menu or desktop shortcut

### Standalone Executable

1. Download the executable file (PyVenvManager.exe) from the releases page
2. Place it in any folder where you have write permissions
3. Double-click to run the application

## Building from Source

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Quick Build (Using the Build Script)

1. Clone or download this repository
2. Open a command prompt or PowerShell in the project directory
3. Run the build script:

```powershell
.\build.bat
```

4. Choose a build method from the menu:
   - Option 1: Simple build (executable only using PyInstaller)
   - Option 2: GUI builder (user-friendly interface with auto-py-to-exe)
   - Option 3: Full installer (creates a complete Windows installer using NSIS)

### Manual Build Methods

#### Method 1: Simple Build (PyInstaller)

```powershell
python simple_build.py
```

The executable will be created in the `dist` folder and copied to the current directory.

#### Method 2: GUI Builder (auto-py-to-exe)

```powershell
python gui_builder.py
```

This will open a user-friendly interface where you can customize build options.

#### Method 3: Full Installer Build (NSIS)

```powershell
python installer.py
```

This creates a complete Windows installer (PyVenvManagerSetup.exe) that will:
- Install the application to Program Files
- Create Start Menu shortcuts
- Create Desktop shortcut
- Register for uninstallation in Control Panel

**Note**: This method requires NSIS (Nullsoft Scriptable Install System) to be installed.

## Usage

1. Launch the application
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

## License

MIT License - Feel free to modify and distribute as needed.
