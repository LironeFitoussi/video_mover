"""
File handling utilities for scanning and moving video files.
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Callable, Optional

from src.config import VIDEO_EXTENSIONS


class VideoFileInfo:
    """Data class for video file information."""
    
    def __init__(self, path: Path, relative_path: str, name: str, size: int):
        self.path = path
        self.relative_path = relative_path
        self.name = name
        self.size = size


class VideoScanner:¬
    """Handles scanning for video files in a directory tree."""
    
    @staticmethod
    def is_video_file(file_path: Path) -> bool:
        """Check if a file is a video based on its extension."""
        return file_path.suffix.lower() in VIDEO_EXTENSIONS
    ¬¬
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def scan_directory(
        source_path: Path,
        destination_path: Path,
        progress_callback: Optional[Callable[[VideoFileInfo], None]] = None
    ) -> List[VideoFileInfo]:
        """
        Scan a directory tree for video files.
        
        Args:
            source_path: Root directory to scan
            destination_path: Destination directory to exclude from scan
            progress_callback: Optional callback function called for each video found
            
        Returns:
            List of VideoFileInfo objects
        """
        video_files = []
        source_resolved = source_path.resolve()
        dest_resolved = destination_path.resolve()
        
        for current_dir, dirs, files in os.walk(source_resolved):
            current_path = Path(current_dir)
            
            # Skip destination folder
            if dest_resolved in current_path.parents or current_path == dest_resolved:
                continue
            
            for file_name in files:
                file_path = current_path / file_name
                
                if VideoScanner.is_video_file(file_path):
                    try:
                        size = file_path.stat().st_size
                        relative_path = file_path.relative_to(source_resolved)
                        
                        video_info = VideoFileInfo(
                            path=file_path,
                            relative_path=str(relative_path),
                            name=file_name,
                            size=size
                        )
                        
                        video_files.append(video_info)
                        
                        if progress_callback:
                            progress_callback(video_info)
                            
                    except Exception as e:
                        print(f"Error accessing {file_path}: {e}")
        
        return video_files


class VideoMover:
    """Handles moving video files to destination directory."""
    
    @staticmethod
    def move_videos(
        video_files: List[VideoFileInfo],
        root_folder: Path,
        dest_folder: Path,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        error_callback: Optional[Callable[[Path, Exception], None]] = None
    ) -> tuple[int, int]:
        """
        Move video files to destination directory preserving folder structure.
        
        Args:
            video_files: List of VideoFileInfo objects to move
            root_folder: Root source folder
            dest_folder: Destination folder
            progress_callback: Optional callback(moved_count, total_count)
            error_callback: Optional callback(source_path, exception)
            
        Returns:
            Tuple of (moved_count, error_count)
        """
        root_path = root_folder.resolve()
        dest_path = dest_folder.resolve()
        dest_path.mkdir(parents=True, exist_ok=True)
        
        moved_count = 0
        error_count = 0
        total_count = len(video_files)
        
        for video_info in video_files:
            source_path = video_info.path
            
            try:
                # Calculate relative path from root folder
                relative_path = source_path.relative_to(root_path)
                
                # Create destination path preserving folder structure
                dest_file_path = dest_path / relative_path.parent / source_path.name
                
                # Ensure destination directory exists
                dest_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move the file
                shutil.move(str(source_path), str(dest_file_path))
                
                moved_count += 1
                
                if progress_callback:
                    progress_callback(moved_count, total_count)
                    
            except Exception as e:
                error_count += 1
                
                if error_callback:
                    error_callback(source_path, e)
                else:
                    print(f"Error moving {source_path}: {e}")
        
        return moved_count, error_count

