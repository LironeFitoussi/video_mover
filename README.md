# Video Mover - Production Build Guide

This guide will help you build the Video Mover application into a Windows executable (.exe) and create an installation wizard.

## Prerequisites

1. **Python 3.7+** - Make sure Python is installed and accessible from the command line
2. **PyInstaller** - Will be installed automatically via requirements.txt
3. **Inno Setup Compiler** (for installer) - Download from [https://jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)

## Quick Start

### Option 1: Automated Build (Recommended)

Simply run the batch script which will build both the executable and installer:

```batch
build_installer.bat
```

This script will:
1. Check for Python and PyInstaller
2. Install PyInstaller if needed
3. Build the executable
4. Create the installer (if Inno Setup is installed)

### Option 2: Manual Build Steps

#### Step 1: Install Dependencies

```batch
pip install -r requirements.txt
```

#### Step 2: Build the Executable

```batch
python build_exe.py
```

Or manually using PyInstaller:

```batch
pyinstaller --name=VideoMover --windowed --onefile --clean move_videos.py
```

The executable will be created in the `dist` folder as `VideoMover.exe`.

#### Step 3: Create the Installer

1. Install **Inno Setup Compiler** from [https://jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)
2. Open `VideoMover.iss` in Inno Setup Compiler
3. Click **Build > Compile** (or press F9)
4. The installer will be created in the `installer` folder

Or use the command line:

```batch
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" VideoMover.iss
```

## Output Files

After building, you'll find:

- **Executable**: `dist\VideoMover.exe` - Standalone executable that can be run directly
- **Installer**: `installer\VideoMover_Setup_1.0.0.exe` - Installation wizard for distribution

## Distribution

### Standalone Executable
You can distribute the `VideoMover.exe` file directly. Users can run it without installation, but it won't appear in the Start Menu or Add/Remove Programs.

### Installation Package (Recommended)
Distribute the `VideoMover_Setup_1.0.0.exe` file. Users can:
- Install the application with a proper installation wizard
- Uninstall via Windows Settings/Control Panel
- Get desktop and Start Menu shortcuts
- Benefit from proper Windows integration

## Customization

### Change Application Icon

1. Create or obtain an `.ico` file for your application
2. In `build_exe.py`, replace `--icon=NONE` with `--icon=path/to/your/icon.ico`
3. In `VideoMover.iss`, uncomment and set `SetupIconFile=path/to/your/icon.ico`

### Modify Installer Settings

Edit `VideoMover.iss` to customize:
- Application name and version
- Publisher information
- Default installation directory
- Additional installation options

### Update Version Information

1. Update `MyAppVersion` in `VideoMover.iss`
2. Rebuild the installer

## Troubleshooting

### PyInstaller Issues

If you encounter errors with PyInstaller:
- Ensure all dependencies are installed
- Try `--clean` flag: `pyinstaller --clean ...`
- Check PyInstaller documentation: [https://pyinstaller.org/](https://pyinstaller.org/)

### Executable Not Working

- Make sure the executable has proper permissions
- Check if antivirus software is blocking it (PyInstaller executables are sometimes flagged)
- Run from command line to see error messages

### Installer Not Creating

- Verify Inno Setup Compiler is installed
- Check that `dist\VideoMover.exe` exists before building installer
- Ensure you have write permissions in the project directory

## Testing

Before distribution, test:
1. Run `VideoMover.exe` directly from the `dist` folder
2. Install using the installer on a clean system
3. Verify uninstallation works correctly
4. Test the application functionality after installation

## File Structure

```
video_mover/
├── move_videos.py          # Main application source
├── requirements.txt        # Python dependencies
├── build_exe.py           # Build script for executable
├── build_installer.bat    # Automated build script
├── VideoMover.iss         # Inno Setup installer script
├── README.md              # This file
├── dist/                  # Output: Executable files
│   └── VideoMover.exe
└── installer/             # Output: Installer files
    └── VideoMover_Setup_1.0.0.exe
```

## License

[Add your license information here]

