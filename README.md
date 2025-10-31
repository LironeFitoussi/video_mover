# Video Mover

**Video Mover** is a simple Windows application that helps you organize your video files. It scans a folder for videos and moves them to another location based on their creation date, making it easy to sort and organize your video collection.

---

## 🎯 For End Users (No Coding Required)

### Quick Start: Using the Pre-built Application

If you just want to use Video Mover without building it yourself, you can download and run the ready-made version:

#### Step 1: Download the Application
- Download `VideoMover.exe` from the releases section of this repository
- Save it anywhere on your computer (like your Desktop or Downloads folder)

#### Step 2: Run the Application
- Double-click `VideoMover.exe` to start the program
- No installation needed! Just double-click and it runs.

#### Step 3: Use Video Mover
1. Click **"Browse"** next to "Source Folder" to select the folder containing your videos
2. Click **"Browse"** next to "Destination Folder" to select where you want videos moved
3. Click **"Scan for Videos"** to find all video files in the source folder
4. Review the list of videos that will be moved
5. Click **"Move Videos"** to organize them into the destination folder

**That's it!** The application will automatically organize your videos based on when they were created.

---

## 🔧 For Developers: Building from Source

If you want to build the application yourself or make changes to the code, follow these steps.

### What You Need First

Before you start, make sure you have:

1. **Python** installed on your computer
   - Download from: https://www.python.org/downloads/
   - During installation, check the box that says "Add Python to PATH"
   - To check if Python is installed, open Command Prompt and type: `python --version`
   - You should see something like "Python 3.x.x"

2. **(Optional) Inno Setup** - Only needed if you want to create an installer
   - Download from: https://jrsoftware.org/isinfo.php

### Step-by-Step Build Instructions

#### Step 1: Get the Code

**Option A: Using Git (if you have it installed)**
1. Open Command Prompt or PowerShell
2. Navigate to where you want to save the project (for example: `cd C:\Users\YourName\Documents`)
3. Type: `git clone <repository-url>`
4. Type: `cd video_mover`

**Option B: Download as ZIP**
1. Click the green "Code" button on this page
2. Select "Download ZIP"
3. Extract the ZIP file to a folder on your computer
4. Open Command Prompt and navigate to the extracted folder:
   ```
   cd path\to\video_mover
   ```
   (Replace `path\to\video_mover` with the actual folder location)

#### Step 2: Install Required Tools

Open Command Prompt in the project folder and type:
```
pip install -r requirements.txt
```
This will automatically download and install everything needed to build the application.

#### Step 3: (Optional) Create an Icon

If you want a custom icon for the application, run:
```
python create_icon.py
```
This step is optional - you can skip it if you don't need a custom icon.

#### Step 4: Build the Application

Run this command:
```
python build_exe.py
```

This will create a file called `VideoMover.exe` in a new folder called `dist`. The building process may take a few minutes - just wait for it to finish!

#### Step 5: Find Your Application

After building, you'll find `VideoMover.exe` in the `dist` folder. You can:
- Double-click it to run it
- Move it anywhere you want
- Share it with others (they don't need Python installed!)

---

## 🚀 Quick Build (All-in-One)

If you prefer a one-click approach, you can use the automated build script:

**Double-click:** `build_installer.bat`

This script will:
- Check that Python is installed
- Install all required tools
- Build the executable
- (If you have Inno Setup) Create an installer

Just wait for it to finish, then check the `dist` folder for `VideoMover.exe`!

---

## 📦 Creating an Installer (Optional)

If you want to create a proper Windows installer (with Start Menu shortcuts and uninstaller):

### Step 1: Install Inno Setup
1. Download Inno Setup from: https://jrsoftware.org/isinfo.php
2. Run the installer and follow the on-screen instructions

### Step 2: Create the Installer
1. Make sure you've already built `VideoMover.exe` (see Step 4 above)
2. Open Inno Setup Compiler
3. Click "File" → "Open"
4. Navigate to the `video_mover` folder and select `VideoMover.iss`
5. Press **F9** or click the "Build" button
6. The installer will be created in the `installer` folder

**Alternative Method (Command Line):**
Open Command Prompt in the project folder and run:
```
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" VideoMover.iss
```
(Adjust the path if Inno Setup is installed in a different location)

---

## 📁 What Gets Created

After building, you'll find:

- **`dist/VideoMover.exe`** - The standalone application
  - This is all you need! You can run it, move it, or share it
  - No installation required

- **`installer/VideoMover_Setup_*.exe`** - Windows installer (if you created one)
  - This creates Start Menu shortcuts and an uninstaller
  - Better for distribution to other users

---

## ❓ Troubleshooting

### "Python is not recognized"
- Python isn't installed or isn't in your PATH
- Solution: Reinstall Python and make sure to check "Add Python to PATH" during installation

### "pip is not recognized"
- This usually means Python isn't installed correctly
- Solution: Reinstall Python and make sure pip is included

### "Module not found" errors
- Some required files aren't installed
- Solution: Run `pip install -r requirements.txt` again

### Antivirus warnings
- Sometimes antivirus software flags newly created executables
- Solution: This is normal for PyInstaller-built apps. Add an exception or use "Allow" if prompted

### Build errors
- Try these steps in order:
  1. Run `pip install --upgrade pip setuptools wheel`
  2. Run `pip install -r requirements.txt` again
  3. Close and reopen Command Prompt
  4. Try building again with `python build_exe.py`

### Installer won't build
- Make sure `VideoMover.exe` exists in the `dist` folder first
- Check that Inno Setup is installed correctly

---

## 🧪 Testing Your Build

Before sharing your application:

1. ✅ Run `dist/VideoMover.exe` and make sure it works
2. ✅ Test moving some videos to make sure everything functions correctly
3. ✅ If you created an installer, test installing it
4. ✅ Test uninstalling (if using the installer)
5. ✅ Try running on a different computer if possible

---

## 📂 Project Files (For Reference)

```
video_mover/
├── src/                      # The application code
│   ├── main.py              # Where the program starts
│   └── gui/                 # User interface files
├── assets/                   # Icons and logos
├── requirements.txt          # List of tools needed
├── build_exe.py             # Script that builds the .exe
├── build_installer.bat      # One-click build script
├── create_icon.py           # Creates icon files
├── VideoMover.iss           # Installer settings
├── dist/                    # (Created after building)
│   └── VideoMover.exe       # The finished application
└── installer/               # (Created after building installer)
    └── VideoMover_Setup_*.exe
```

---

## 🎨 Customization

### Changing the App Icon
1. Place your `.ico` file in the `assets/` folder
2. Name it `logo.ico` or `logo_x1.ico`
3. The build script will automatically use it

### Changing App Version
1. Open `VideoMover.iss` in a text editor
2. Find the line that says `MyAppVersion=`
3. Change the version number
4. Save the file

### Other Installer Settings
- Open `VideoMover.iss` to customize:
  - App name
  - Publisher name
  - Installation options
  - And more!

---

## 📝 License

[Your license information here]

---

## 💡 Tips

- The standalone `VideoMover.exe` can be run on any Windows computer without installing Python
- Keep the `dist/VideoMover.exe` file - it's your finished application!
- The `build/` folder can be deleted after building (it's just temporary files)
- If you make code changes, you'll need to rebuild the .exe for the changes to appear
