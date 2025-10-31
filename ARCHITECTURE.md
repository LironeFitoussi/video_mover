# Video Mover - Architecture

This document describes the professional modular architecture of the Video Mover application.

## Project Structure

```
video_mover/
├── src/                      # Main source code package
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration constants
│   ├── file_handler.py      # File operations (scanning, moving)
│   └── gui/                 # GUI components package
│       ├── __init__.py      # GUI package exports
│       └── main_window.py   # Main application window
├── move_videos.py           # Backward-compatible entry point
├── build_exe.py             # Build script for executable
├── build_installer.bat      # Automated build script
├── VideoMover.iss           # Inno Setup installer script
├── VideoMover.spec          # PyInstaller spec file
└── requirements.txt         # Python dependencies
```

## Module Overview

### `src/config.py`
Contains all configuration constants:
- Video file extensions
- Image file extensions
- Application settings (title, geometry)

### `src/file_handler.py`
Core file operations module containing:

- **`VideoFileInfo`**: Data class for video file information
- **`VideoScanner`**: Static class for scanning directories
  - `is_video_file()`: Check if file is a video
  - `format_size()`: Format file size in human-readable format
  - `scan_directory()`: Scan directory tree for videos
- **`VideoMover`**: Static class for moving video files
  - `move_videos()`: Move videos preserving folder structure

### `src/gui/main_window.py`
Main GUI application window:
- **`VideoMoverApp`**: Main application class
  - Handles all GUI components
  - Manages state (scanning, moving)
  - Coordinates file operations with UI updates

### `src/main.py`
Application entry point:
- Creates Tkinter root window
- Initializes and runs the application

## Design Principles

1. **Separation of Concerns**: Business logic (file operations) is separated from UI code
2. **Single Responsibility**: Each module has a clear, single purpose
3. **Testability**: Modules can be imported and tested independently
4. **Maintainability**: Code is organized logically and easy to navigate
5. **Extensibility**: Easy to add new features or modify existing ones

## Running the Application

### As a Module
```bash
python -m src.main
```

### Using Entry Point
```bash
python move_videos.py
```

### As Executable
```bash
dist/VideoMover.exe
```

## Building

The build scripts have been updated to work with the new structure:
- `build_exe.py` - Builds executable from `src/main.py`
- `build_installer.bat` - Automated build process
- `VideoMover.spec` - PyInstaller specification file


