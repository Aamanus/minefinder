
import tkinter as tk
from src.settings import gSettings, gDifficulties
import time

class gDraw:
    def __init__(self, screen_width=gSettings.SCREEN_WIDTH, screen_height=gSettings.SCREEN_HEIGHT):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title(gSettings.GAME_TITLE)
        
        self.start_time = None
        self.end_time = None
        self.time_taken = None

        # Calculate window position for center of screen
        pos_x = (self.root.winfo_screenwidth() // 2) - (screen_width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (screen_height // 2)
        # Get the primary screen dimensions using _root.maxsize() which returns main screen size
        main_screen_width, main_screen_height = self.root.maxsize()
        pos_x = (main_screen_width // 2) - (screen_width // 2)
        pos_y = (main_screen_height // 2) - (screen_height // 2)        
        # Set window size and position
        self.root.geometry(f'{screen_width}x{screen_height}+{pos_x}+{pos_y}')
        self.root.resizable(False, False)  # Disable window resizing
        # generate_minefield param, which will hold a function reference for callback into the minefield object
        self.new_minefield_callback = None
        # Create main canvas

           # Create options frame FIRST
        self.options_frame = tk.Frame(
            self.root,
            width=300,
            height=screen_height,
            bg=gSettings.BACKGROUND_COLOR
        )
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.options_frame.pack_propagate(False)  # Prevent frame from shrinking
        # Create canvas AFTER options frame, with adjusted width
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width - 300,  # Subtract options frame width
            height=screen_height,
            bg=gSettings.BACKGROUND_COLOR
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialize game status bar
        self.status_frame = tk.Frame(
            self.root,
            height=gSettings.STATUS_BAR_HEIGHT,
            bg=gSettings.STATUS_BAR_COLOR
        )
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # use the reserved space on the left side to provide some input options.  This will let us generate a new map with new size options, and we want a selector that
        # lets us choose between easy, medium and hard setting. And finally a button to generate the new minefield

        # Create a label for the options
        tk.Label(
            self.options_frame,
            text="Options",
            font=("Arial", 24),
            bg=gSettings.BACKGROUND_COLOR
        ).pack(pady=10)
        # Create a label for the difficulty
        tk.Label(
            self.options_frame,
            text="Difficulty",
            font=("Arial", 16),
            bg=gSettings.BACKGROUND_COLOR
        ).pack(pady=5)
        # Create a dropdown for the difficulty
        self.difficulty = tk.StringVar(self.root)
        self.difficulty.set("Easy")  # default value
        tk.OptionMenu(
            self.options_frame,
            self.difficulty,
            "Easy",
            "Medium",
            "Hard"
        ).pack(pady=5)
        # Create a button to generate the minefield
        tk.Button(
            self.options_frame,
            text="Generate Minefield",
            font=("Arial", 16),
            command=self.new_minefield
        ).pack(pady=5)
        # Create a label for the status
        tk.Label(
            self.options_frame,
            text="Status",
            font=("Arial", 16),
            bg=gSettings.BACKGROUND_COLOR
        ).pack(pady=5)
        # Create a label for the status
        self.status = tk.Label(
            self.options_frame,
            text="Ready",
            font=("Arial", 16),
            bg=gSettings.BACKGROUND_COLOR
        )
        self.status.pack(pady=5)
        # create a label for the total number of mines
        self.total_mines = tk.Label(
            self.options_frame,
            text="Total Mines: 0",
            font=("Arial", 16),
            bg=gSettings.BACKGROUND_COLOR
        )
        # Create a label for the mines remaining
        self.mines_remaining = tk.Label(
            self.options_frame,
            text="Mines Remaining: 0",
            font=("Arial", 16),
            bg=gSettings.BACKGROUND_COLOR
        )
        self.mines_remaining.pack(pady=5)
        # Create a label for the time elapsed
        self.time_elapsed = tk.Label(
            self.options_frame,
            text="Time Elapsed: 0",
            font=("Arial", 16),
            bg=gSettings.BACKGROUND_COLOR
        )
        self.time_elapsed.pack(pady=5)
        # Create a label for the game over message
        self.game_over_message = tk.Label(
            self.options_frame,
            text="",
            font=("Arial", 16),
            fg="red",
            bg=gSettings.BACKGROUND_COLOR
        )
        self.game_over_message.pack(pady=5)

    def start_timer(self):
        """Start the timer"""
        print("timer started")
        self.start_time = time.time()
        self.update_timer()  # Start the timer updates

    def update_timer(self):
        """Update the timer display"""
        if self.start_time is not None and self.end_time is None:  # Only update if timer is running
            current_time = time.time() - self.start_time
            self.time_elapsed.config(text=f"Time Elapsed: {current_time:.1f}")
            # Schedule the next update in 100ms (10 updates per second)
            self.root.after(100, self.update_timer)

    def stop_timer(self):
        """Stop the timer"""
        print("timer stopped")
        self.end_time = time.time()
        self.time_taken = self.end_time - self.start_time
        self.time_elapsed.config(text=f"Time Elapsed: {self.time_taken:.1f}")

    def reset_timer(self):
        """Reset the timer"""
        self.start_time = None
        self.end_time = None
        self.time_taken = None
        self.time_elapsed.config(text="Time Elapsed: 0.0")

    def update_total_mines(self, num_mines):
        """Update the total number of mines"""
        self.total_mines.config(text=f"Total Mines: {num_mines}")
        self.update_mines_remaining(num_mines)
    
    def update_mines_remaining(self, num_mines):
        """Update the number of mines remaining"""
        self.mines_remaining.config(text=f"Mines Remaining: {num_mines}")
    def new_minefield(self):
        """Generate a new minefield"""
        # Get the difficulty
        difficulty = self.difficulty.get()
        # Get the number of mines
        if difficulty == "Easy":
            difficulty = gDifficulties.EASY
        elif difficulty == "Medium":
            difficulty = gDifficulties.MEDIUM
        else:
            difficulty = gDifficulties.HARD
        # Call the callback function
        # clear the canvas
        self.clear_canvas()
        # reset timer
        self.reset_timer()

        self.new_minefield_callback(gSettings.MINEFIELD_WIDTH,
                                    gSettings.MINEFIELD_HEIGHT,
                                    difficulty)
        # Update the status
        self.status.config(text="Ready")
        # Update the mines remaining
        self.mines_remaining.config(text=f"Mines Remaining: {num_mines}")
        # Update the time elapsed
        self.time_elapsed.config(text="Time Elapsed: 0")
        # Update the game over message
        self.game_over_message.config(text="")

    def game_over(self,message):
        """Display game over message"""
        # write the gameover message to the lable in self._game_over_message
        self.game_over_message.config(text=message)
        # stop the timer
        self.stop_timer()
        #  redraw the label
        self.game_over_message.update()

    def clear_canvas(self):
        """Clear all items from the canvas"""
        self.canvas.delete("all")

    def update(self):
        """Update the display"""
        self.root.update()

    def draw_tile(self, x, y, size, color, outline_color=None,number=None):
        coord_tag = f"{x}, {y}"
        # if a tile with this tag exists, delete it
        if self.canvas.find_withtag(coord_tag):
            self.canvas.delete(coord_tag)
        
        """Draw a single tile on the canvas"""
        # add an x indent of 300
        tags = ("tile", coord_tag)
        x = x + gSettings.MINEFIELD_PAD_X
        # add a y indent from settings
        y = y + gSettings.MINEFIELD_PAD_Y
        # draw a rectangle. If number is not none, draw it with a number, using NUMBER_COLORS, else, just draw the rectangle without
        if number is not None and number > 0:
            return self.canvas.create_rectangle(
                x, y, x + size, y + size,
                fill=color,
                outline=outline_color if outline_color else gSettings.TILE_OUTLINE_COLOR,
                tags=tags
            ), self.canvas.create_text(
                x + size // 2, y + size // 2,
                text=str(number),
                fill=gSettings.NUMBER_COLORS[number],
                tags=tags
            )
        
        return self.canvas.create_rectangle(
            x, y, x + size, y + size,
            fill=color,
            outline=outline_color if outline_color else gSettings.TILE_OUTLINE_COLOR,
            tags=tags
        )
    

        

    def bind_click(self, callback, tag):
        """Bind mouse click events to callback function for elements with specified tag"""
        self.canvas.tag_bind(tag, "<Button-1>", callback)  # Left click
        self.canvas.tag_bind(tag, "<Button-3>", callback)  # Right click

    def start_main_loop(self):
        """Start the main Tkinter event loop"""
        self.root.mainloop()
