import tkinter
import random
import sys
import math

from src.settings import gSettings
from src.gdraw import gDraw

class MineTile:
    def __init__(self, x, y, size, color, outline_color=None):
        # set x and y to be the top-left corner.  All draw calculations will come from that root
        self.x = x*size
        self.y = y*size
        self.size = size
        self.color = color
        self.outline_color = outline_color if outline_color else gSettings.TILE_OUTLINE_COLOR
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0


class MineField:
    def __init__(self, width, height, difficulty,game: gDraw):
        self.width = width
        self.height = height
        self.field=[]

        self.num_mines = int(width * height * gSettings.DIFFICULTY_MINE_MULTIPLIER[difficulty])
        game.update_mines_remaining(self.num_mines)
        self.difficulty = difficulty
        self.mines = set()
        self.flags = set()
        self.revealed = set()
        self.game_over = False
        self.start_time = None
        self.end_time = None
        self.time_taken = None
        self.num_revealed = 0
        self.num_correct_flags = 0
        self.num_incorrect_flags = 0
        self.num_mines_revealed = 0
        self.num_non_mines_revealed = 0
        self.num_non_mines = width * height - self.num_mines
        self.generate_minefield()
        self.generate_mines()
        self.calculate_adjacent_mines()
        # Mine field is created and all is ready to play.
        # Display the minefield by calling draw_minefield()
        self.game = game
        self.game.clear_canvas()
        self.draw_minefield()
        self.game.bind_click(self.handle_click, "tile")
        self.game.new_minefield_callback = self.new_minefield


    # Callback functions
    def new_minefield(self,width,height,difficulty):
        self.game.clear_canvas()
        self.game.update()
        self.__init__(width, height, difficulty, self.game)

    def handle_click(self, event):
        if self.game.start_time is None:
            self.game.start_timer()
        if self.game_over:
            return
        # Get the tile that was clicked
        x = math.floor((event.x - gSettings.MINEFIELD_PAD_X) / gSettings.TILE_SIZE)
        y = math.floor((event.y - gSettings.MINEFIELD_PAD_Y) / gSettings.TILE_SIZE)

        # Right click to toggle flag
        if event.num == 3:
            self.field[x][y].is_flagged = not self.field[x][y].is_flagged
            if self.field[x][y].is_flagged:
                self.flags.add((x,y))
                if (x, y) in self.mines:
                    self.num_correct_flags += 1
            else:
                self.flags.remove((x,y))
                if (x, y) in self.mines:
                    self.num_correct_flags -= 1
            
            self.game.update_mines_remaining(self.num_mines - len(self.flags))

            self.game.clear_canvas()
            self.draw_minefield()
            self.game.update()
            return

        # Left click to reveal
        if event.num == 1:
            # Check if the tile is a mine
            if self.field[x][y].is_mine:
                # Game over
                self.game_over = True
                
                # reveal all mines
                for mine in self.mines:
                    self.reveal_tile(mine[0], mine[1])
                
                self.game.game_over(f"You found a mine at {x},{y}")
                self.game.update()

            else:
                # Reveal the tile
                self.reveal_tile(x, y)
                self.game.clear_canvas()
                self.draw_minefield()
                self.game.update()      
                
                  
    def reveal_tile(self, x, y):
        if self.field[x][y].is_revealed:
            return
        self.field[x][y].is_revealed = True
        self.num_revealed += 1
        if self.field[x][y].is_mine:
            self.num_mines_revealed += 1
            self.draw_tile(x, y)
            return
        self.num_non_mines_revealed += 1
        if self.field[x][y].adjacent_mines == 0:
            self.draw_tile(x, y)
            for i in range(max(0, x - 1), min(self.width, x + 2)):
                for j in range(max(0, y - 1), min(self.height, y + 2)):
                    self.reveal_tile(i, j)
        else:
            self.draw_tile(x, y)
            return
        
    def draw_tile(self,x,y):
        
        if self.field[x][y].is_revealed:
            if self.field[x][y].is_mine:
                self.game.draw_tile(self.field[x][y].x, self.field[x][y].y, self.field[x][y].size, gSettings.TILE_MINE_COLOR, self.field[x][y].outline_color)
            else:
                self.game.draw_tile(self.field[x][y].x, self.field[x][y].y, self.field[x][y].size, gSettings.TILE_EMPTY_COLOR, self.field[x][y].outline_color, self.field[x][y].adjacent_mines)
        elif self.field[x][y].is_flagged:
            self.game.draw_tile(self.field[x][y].x, self.field[x][y].y, self.field[x][y].size, gSettings.TILE_FLAG_COLOR, self.field[x][y].outline_color)
        else:
            self.game.draw_tile(self.field[x][y].x, self.field[x][y].y, self.field[x][y].size, self.field[x][y].color, self.field[x][y].outline_color)

    # Generation functions
    def generate_minefield(self):
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(MineTile(i, j, gSettings.TILE_SIZE, gSettings.TILE_NORMAL_COLOR))
            self.field.append(row)

    def generate_mines(self):
        # Generate mines
        while len(self.mines) < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))
                self.field[x][y].is_mine = True
    
    def calculate_adjacent_mines(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.field[i][j].is_mine:
                    continue
                for x in range(max(0, i - 1), min(self.width, i + 2)):
                    for y in range(max(0, j - 1), min(self.height, j + 2)):
                        if self.field[x][y].is_mine:
                            self.field[i][j].adjacent_mines += 1

    def draw_minefield(self):
        for i in range(self.width):
            for j in range(self.height):
                self.draw_tile(i, j)
