import tkinter
import random
import sys
import math
import time
import minefield
from settings import gSettings

class MineField:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
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
        self.num_non_mines = width * height - num_mines
        self.generate_minefield()
        self.generate_mines()
        self.calculate_adjacent_mines()
        self.print_minefield()