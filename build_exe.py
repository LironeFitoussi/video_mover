#!/usr/bin/env python3
"""
Build script to create a Windows executable from the Video Mover application.
Run this script to build the .exe file.
"""

import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """Build the executable using PyInstaller."""
    script_dir = Path(__file__).parent.resolve()
    app_script = script_dir / "src" / "main.py"
    assets_dir = script_dir / "assets"
    
    if not app_script.exists():
        print(f"Error: {app_script} not found!")
        return False
    
    # Try to find icon file (ICO preferred, PNG also works)
    icon_file = None
    icon_paths = [
        script_dir / "assets" / "logo.ico",
        script_dir / "assets" / "logo_x1.ico",
        script_dir / "assets" / "logo_x1.png",
    ]
    
    for path in icon_paths:
        if path.exists():
            icon_file = path
            break
    
    print("Building executable...")
    print(f"Script: {app_script}")
    if icon_file:
        print(f"Icon: {icon_file}")
    
    # PyInstaller command (using module method for better compatibility)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=VideoMover",
        "--windowed",  # No console window (GUI app)
        "--onefile",  # Single executable file
        "--clean",
        "--noconfirm",
        "--paths", str(script_dir),  # Add project root to path
    ]
    
    # Add icon if available
    if icon_file:
        cmd.extend(["--icon", str(icon_file)])
    
    # Add assets directory to include logo in the build
    if assets_dir.exists():
        cmd.extend(["--add-data", f"{assets_dir}{os.pathsep}assets"])
    
    cmd.append(str(app_script))
    
    try:
        result = subprocess.run(cmd, check=True, cwd=str(script_dir))
        print("\n✓ Build successful!")
        print(f"Executable location: {script_dir / 'dist' / 'VideoMover.exe'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n✗ Build error: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)

