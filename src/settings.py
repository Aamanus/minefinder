class gDifficulties:
    EASY = 0
    MEDIUM = 1
    HARD = 2
    VEASY = 3

class gMinefieldSizes:
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

class gSettings:

    GAME_TITLE = "Minefinder"
    BACKGROUND_COLOR = "#c0c0c0"  # Grey background
    STATUS_BAR_HEIGHT = 30
    STATUS_BAR_COLOR = "#f0f0f0"
    TILE_OUTLINE_COLOR = "#808080"
    TILE_NORMAL_COLOR = "#c0c0c0"
    TILE_EMPTY_COLOR = "#e0e0e0"
    TILE_MINE_COLOR = "#ff0000"
    TILE_FLAG_COLOR = "#ffff00"
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1100
    SCREEN_MENUS_WIDTH = 300
    MINEFIELD_PAD_X = 50
    MINEFIELD_PAD_Y = 50
    # Add other game settings as needed

    MINEFIELD_WIDTH = 25
    MINEFIELD_HEIGHT = 25
    NUMBER_MINES = (MINEFIELD_HEIGHT*MINEFIELD_WIDTH)//5
    NUM_MINES_EASY = 0.2
    NUM_MNIES_MEDIUM = 0.3
    NUM_MINES_HARD = 0.5
    DIFFICULTY_MINE_MULTIPLIER = {
        gDifficulties.EASY: NUM_MINES_EASY,
        gDifficulties.MEDIUM: NUM_MNIES_MEDIUM,
        gDifficulties.HARD: NUM_MINES_HARD,
        gDifficulties.VEASY: 0.1
    }
    MINEFIELD_SIZES = {
        gMinefieldSizes.SMALL: (10, 10),
        gMinefieldSizes.MEDIUM: (25, 25),
        gMinefieldSizes.LARGE: (50, 50)
    }
    NUMBER_COLORS = {
        1: "#0000ff",
        2: "#008000",
        3: "#ff0000",
        4: "#000080",
        5: "#800000",
        6: "#008080",
        7: "#000000",
        8: "#808080",
    }

