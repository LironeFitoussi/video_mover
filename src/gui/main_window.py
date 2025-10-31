"""
Main GUI window for the Video Mover application.
"""

import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
from typing import List

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from src.file_handler import VideoFileInfo, VideoScanner, VideoMover
from src.config import APP_TITLE, APP_GEOMETRY


class VideoMoverApp:
    """Main application window for Video Mover."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the Video Mover application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_GEOMETRY)
        self.root.resizable(True, True)
        
        # Set window icon
        self._set_window_icon()
        
        # State variables
        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.is_scanning = False
        self.is_moving = False
        self.video_files: List[VideoFileInfo] = []
        
        # Set default paths
        self._set_default_paths()
        
        # Create UI
        self._create_widgets()
        
    def _get_asset_path(self, filename: str) -> Path | None:
        """
        Get the path to an asset file, handling both development and PyInstaller builds.
        
        Args:
            filename: Name of the asset file (e.g., "logo_x1.png")
            
        Returns:
            Path to the asset file, or None if not found
        """
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            # PyInstaller extracts files to sys._MEIPASS
            asset_paths = []
            if hasattr(sys, '_MEIPASS'):
                asset_paths.append(Path(sys._MEIPASS) / "assets" / filename)
            
            # Also check the executable directory
            script_dir = Path(sys.executable).parent
            asset_paths.extend([
                script_dir / "assets" / filename,
                script_dir / filename,
            ])
        else:
            # Running as script
            script_dir = Path(__file__).parent.parent.parent.resolve()
            asset_paths = [script_dir / "assets" / filename]
        
        # Try to find the asset
        for path in asset_paths:
            if path and path.exists():
                return path
        
        return None
    
    def _set_window_icon(self):
        """Set the window icon from assets folder."""
        try:
            icon_path = self._get_asset_path("logo_x1.png")
            
            if icon_path:
                # Load PNG image and set as icon
                icon_image = tk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(True, icon_image)
                # Keep a reference to prevent garbage collection
                self._icon_image = icon_image
        except Exception as e:
            # If icon loading fails, continue without icon
            print(f"Warning: Could not load window icon: {e}")
    
    def _set_default_paths(self):
        """Set default source and destination folder paths."""
        # Get the directory containing the script or executable
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = Path(sys.executable).parent
        else:
            # Running as script
            script_dir = Path(__file__).parent.parent.parent.resolve()
        self.source_folder.set(str(script_dir))
        self.dest_folder.set(str(script_dir / "VIDEOS"))
    
    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Header frame for logo and title
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # Logo
        self._logo_image = None
        try:
            logo_path = self._get_asset_path("logo_x1.png")
            if logo_path:
                if PIL_AVAILABLE:
                    # Use PIL for better image handling and resizing
                    img = Image.open(str(logo_path))
                    max_height = 80
                    if img.height > max_height:
                        # Resize maintaining aspect ratio
                        scale_factor = max_height / img.height
                        new_width = int(img.width * scale_factor)
                        new_height = max_height
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    logo_image = ImageTk.PhotoImage(img)
                else:
                    # Fallback to basic tkinter PhotoImage
                    logo_image = tk.PhotoImage(file=str(logo_path))
                self._logo_image = logo_image  # Keep reference to prevent garbage collection
                logo_label = ttk.Label(header_frame, image=logo_image)
                logo_label.grid(row=0, column=0, padx=(0, 15), sticky=tk.W)
        except Exception as e:
            print(f"Warning: Could not load logo image: {e}")
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="Video File Mover", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=1, sticky=tk.W)
        
        # Source folder selection
        self._create_folder_selection(main_frame)
        
        # Buttons
        self._create_buttons(main_frame)
        
        # Progress bar
        self._create_progress_bar(main_frame)
        
        # Status label
        self._create_status_label(main_frame)
        
        # Statistics
        self._create_statistics_frame(main_frame)
        
        # Video list
        self._create_video_list(main_frame)
    
    def _create_folder_selection(self, parent: ttk.Frame):
        """Create folder selection widgets."""
        # Source folder
        ttk.Label(parent, text="Source Folder:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=10
        )
        source_entry = ttk.Entry(parent, textvariable=self.source_folder, width=50)
        source_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=10)
        ttk.Button(
            parent, 
            text="Browse...", 
            command=self.browse_source
        ).grid(row=1, column=2, pady=10)
        
        # Destination folder
        ttk.Label(parent, text="Destination Folder:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=10
        )
        dest_entry = ttk.Entry(parent, textvariable=self.dest_folder, width=50)
        dest_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=10)
        ttk.Button(
            parent, 
            text="Browse...", 
            command=self.browse_destination
        ).grid(row=2, column=2, pady=10)
    
    def _create_buttons(self, parent: ttk.Frame):
        """Create control buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        self.scan_button = ttk.Button(
            button_frame,
            text="🔍 Scan for Videos",
            command=self.scan_videos,
            width=20
        )
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.start_button = ttk.Button(
            button_frame,
            text="▶️ Start Moving Videos",
            command=self.start_moving,
            state=tk.DISABLED,
            width=20
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
    
    def _create_progress_bar(self, parent: ttk.Frame):
        """Create progress bar widget."""
        self.progress = ttk.Progressbar(
            parent, 
            mode='indeterminate',
            length=400
        )
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
    
    def _create_status_label(self, parent: ttk.Frame):
        """Create status label."""
        self.status_label = ttk.Label(
            parent, 
            text="Ready to scan for videos",
            font=("Arial", 9)
        )
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
    
    def _create_statistics_frame(self, parent: ttk.Frame):
        """Create statistics display frame."""
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        stats_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        stats_frame.columnconfigure(1, weight=1)
        
        self.stats_labels = {}
        stats = ["Total Videos Found", "Videos Moved", "Errors"]
        for i, stat in enumerate(stats):
            ttk.Label(stats_frame, text=f"{stat}:", font=("Arial", 9, "bold")).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=2
            )
            label = ttk.Label(stats_frame, text="0", font=("Arial", 9))
            label.grid(row=i, column=1, sticky=tk.W, padx=10, pady=2)
            self.stats_labels[stat] = label
    
    def _create_video_list(self, parent: ttk.Frame):
        """Create video list treeview."""
        list_frame = ttk.LabelFrame(parent, text="Video Files Found", padding="10")
        list_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(7, weight=1)
        
        # Treeview for video list
        columns = ("Path", "Size")
        self.video_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=10)
        self.video_tree.heading("#0", text="File Name")
        self.video_tree.heading("Path", text="Relative Path")
        self.video_tree.heading("Size", text="Size")
        self.video_tree.column("#0", width=200)
        self.video_tree.column("Path", width=300)
        self.video_tree.column("Size", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.video_tree.yview)
        self.video_tree.configure(yscrollcommand=scrollbar.set)
        
        self.video_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def browse_source(self):
        """Open folder dialog for source selection."""
        folder = filedialog.askdirectory(
            title="Select Source Folder",
            initialdir=self.source_folder.get()
        )
        if folder:
            self.source_folder.set(folder)
            self.video_tree.delete(*self.video_tree.get_children())
            self.start_button.config(state=tk.DISABLED)
            self.update_stats()
    
    def browse_destination(self):
        """Open folder dialog for destination selection."""
        folder = filedialog.askdirectory(
            title="Select Destination Folder",
            initialdir=self.dest_folder.get()
        )
        if folder:
            self.dest_folder.set(folder)
    
    def _validate_paths(self) -> tuple[bool, str]:
        """
        Validate source and destination paths.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        source = Path(self.source_folder.get())
        dest = Path(self.dest_folder.get())
        
        if not source.exists():
            return False, "Source folder does not exist!"
        
        if not source.is_dir():
            return False, "Source path is not a directory!"
        
        if source == dest:
            return False, "Source and destination folders cannot be the same!"
        
        return True, ""
    
    def scan_videos(self):
        """Start scanning for video files."""
        is_valid, error_msg = self._validate_paths()
        if not is_valid:
            messagebox.showerror("Error", error_msg)
            return
        
        source = Path(self.source_folder.get())
        dest = Path(self.dest_folder.get())
        
        self.is_scanning = True
        self.scan_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Scanning for video files...")
        self.video_tree.delete(*self.video_tree.get_children())
        self.video_files = []
        
        # Run scan in separate thread
        thread = threading.Thread(
            target=self._scan_worker, 
            args=(source, dest), 
            daemon=True
        )
        thread.start()
    
    def _scan_worker(self, source_path: Path, dest_path: Path):
        """Worker thread to scan for videos."""
        try:
            def progress_callback(video_info: VideoFileInfo):
                """Callback to update UI when a video is found."""
                self.root.after(
                    0, 
                    self._add_video_to_list, 
                    video_info.name, 
                    video_info.relative_path, 
                    video_info.size
                )
            
            video_files = VideoScanner.scan_directory(
                source_path, 
                dest_path, 
                progress_callback=progress_callback
            )
            
            self.video_files = video_files
            
            # Scan complete
            self.root.after(0, self._scan_complete)
            
        except Exception as e:
            self.root.after(
                0, 
                lambda: messagebox.showerror("Error", f"Scan error: {e}")
            )
            self.root.after(0, self._scan_complete)
    
    def _add_video_to_list(self, name: str, relative_path: str, size: int):
        """Add a video file to the treeview."""
        formatted_size = VideoScanner.format_size(size)
        self.video_tree.insert(
            "", tk.END, 
            text=name,
            values=(relative_path, formatted_size)
        )
    
    def _scan_complete(self):
        """Called when scan is complete."""
        self.is_scanning = False
        self.progress.stop()
        self.scan_button.config(state=tk.NORMAL)
        self.update_stats()
        
        count = len(self.video_files)
        if count > 0:
            self.start_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"Found {count} video file(s). Ready to move.")
        else:
            self.status_label.config(text="No video files found.")
            messagebox.showinfo("Scan Complete", "No video files found in the source folder.")
    
    def start_moving(self):
        """Start moving video files."""
        if not self.video_files:
            messagebox.showwarning("Warning", "No videos to move. Please scan first.")
            return
        
        source = Path(self.source_folder.get())
        dest = Path(self.dest_folder.get())
        
        # Confirm before moving
        response = messagebox.askyesno(
            "Confirm Move",
            f"Move {len(self.video_files)} video file(s) from:\n{source}\n\nto:\n{dest}?",
            icon='question'
        )
        
        if not response:
            return
        
        self.is_moving = True
        self.scan_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Moving video files...")
        
        # Reset stats
        self.stats_labels["Videos Moved"].config(text="0")
        self.stats_labels["Errors"].config(text="0")
        
        # Run move in separate thread
        thread = threading.Thread(
            target=self._move_worker, 
            args=(source, dest), 
            daemon=True
        )
        thread.start()
    
    def _move_worker(self, root_folder: Path, dest_folder: Path):
        """Worker thread to move video files."""
        try:
            def progress_callback(moved_count: int, total_count: int):
                """Callback to update progress."""
                self.root.after(
                    0, 
                    lambda c=moved_count: self.stats_labels["Videos Moved"].config(text=str(c))
                )
                self.root.after(
                    0, 
                    lambda c=moved_count, t=total_count: self.status_label.config(
                        text=f"Moving... {c}/{t}"
                    )
                )
            
            def error_callback(source_path: Path, exception: Exception):
                """Callback for errors."""
                error_count = int(self.stats_labels["Errors"].cget("text")) + 1
                self.root.after(
                    0, 
                    lambda c=error_count: self.stats_labels["Errors"].config(text=str(c))
                )
                print(f"Error moving {source_path}: {exception}")
            
            moved_count, error_count = VideoMover.move_videos(
                self.video_files,
                root_folder,
                dest_folder,
                progress_callback=progress_callback,
                error_callback=error_callback
            )
            
            # Move complete
            self.root.after(0, self._move_complete, moved_count, error_count)
            
        except Exception as e:
            self.root.after(
                0, 
                lambda: messagebox.showerror("Error", f"Move error: {e}")
            )
            self.root.after(0, self._move_complete, 0, len(self.video_files))
    
    def _move_complete(self, moved_count: int, error_count: int):
        """Called when move operation is complete."""
        self.is_moving = False
        self.progress.stop()
        self.scan_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        
        self.status_label.config(
            text=f"Complete! Moved {moved_count} video(s), {error_count} error(s)."
        )
        
        # Remove moved files from list
        self.video_files = []
        self.video_tree.delete(*self.video_tree.get_children())
        self.update_stats()
        
        messagebox.showinfo(
            "Move Complete",
            f"Operation completed!\n\nMoved: {moved_count}\nErrors: {error_count}"
        )
    
    def update_stats(self):
        """Update statistics labels."""
        self.stats_labels["Total Videos Found"].config(text=str(len(self.video_files)))
        self.stats_labels["Videos Moved"].config(text="0")
        self.stats_labels["Errors"].config(text="0")

