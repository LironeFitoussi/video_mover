@echo off
REM Build script for creating Video Mover installer
REM This script builds the .exe first, then creates the installer

echo ========================================
echo Video Mover - Build and Installer Script
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
echo Checking PyInstaller installation...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Build the executable
echo.
echo Step 1: Building executable...
python build_exe.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

REM Check if executable was created
if not exist "dist\VideoMover.exe" (
    echo ERROR: Executable not found in dist folder
    pause
    exit /b 1
)

echo.
echo Step 2: Creating installer...
echo Checking for Inno Setup Compiler...

REM Try to find Inno Setup Compiler
set INNO_SETUP_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set INNO_SETUP_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set INNO_SETUP_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
) else (
    echo.
    echo WARNING: Inno Setup Compiler not found in standard locations
    echo Please install Inno Setup from: https://jrsoftware.org/isinfo.php
    echo.
    echo You can also manually compile the installer by:
    echo   1. Opening VideoMover.iss in Inno Setup Compiler
    echo   2. Clicking Build ^> Compile
    echo.
    echo The executable is ready at: dist\VideoMover.exe
    pause
    exit /b 0
)

REM Compile the installer
"%INNO_SETUP_PATH%" "VideoMover.iss"
if errorlevel 1 (
    echo ERROR: Failed to create installer
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo Executable: dist\VideoMover.exe
echo Installer: installer\VideoMover_Setup_1.0.0.exe
echo.
pause


