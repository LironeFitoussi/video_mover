"""
Main entry point for the Video Mover application.
"""

import tkinter as tk

from src.gui import VideoMoverApp


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = VideoMoverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

