
import tkinter as tk
from settings import gSettings

class gDraw:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title(gSettings.GAME_TITLE)
        
        # Calculate window position for center of screen
        pos_x = (self.root.winfo_screenwidth() // 2) - (screen_width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (screen_height // 2)
        
        # Set window size and position
        self.root.geometry(f'{screen_width}x{screen_height}+{pos_x}+{pos_y}')
        self.root.resizable(False, False)  # Disable window resizing
        
        # Create main canvas
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width,
            height=screen_height,
            bg=gSettings.BACKGROUND_COLOR
        )
        self.canvas.pack()

        # Initialize game status bar
        self.status_frame = tk.Frame(
            self.root,
            height=gSettings.STATUS_BAR_HEIGHT,
            bg=gSettings.STATUS_BAR_COLOR
        )
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

    def clear_canvas(self):
        """Clear all items from the canvas"""
        self.canvas.delete("all")

    def update(self):
        """Update the display"""
        self.root.update()

    def draw_tile(self, x, y, size, color, outline_color=None):
        """Draw a single tile on the canvas"""
        return self.canvas.create_rectangle(
            x, y, x + size, y + size,
            fill=color,
            outline=outline_color if outline_color else gSettings.TILE_OUTLINE_COLOR
        )

    def bind_click(self, callback):
        """Bind mouse click events to callback function"""
        self.canvas.bind("<Button-1>", callback)  # Left click
        self.canvas.bind("<Button-3>", callback)  # Right click

    def start_main_loop(self):
        """Start the main Tkinter event loop"""
        self.root.mainloop()
