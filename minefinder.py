from src.gdraw import gDraw
from src.minefield import MineField
from src.settings import gSettings

def main():
    """Main function to run the game"""
    # Create the game window
    screen_width = gSettings.SCREEN_WIDTH
    screen_height = gSettings.SCREEN_HEIGHT
    gdraw = gDraw(screen_width, screen_height)

    # Create the minefield
    minefield = MineField(
        gSettings.MINEFIELD_WIDTH,
        gSettings.MINEFIELD_HEIGHT,
        gSettings.NUMBER_MINES,
        gdraw
    )
    print("Minefield created")
    # minefield is created and drawn, start main loop and test
    gdraw.start_main_loop()

if __name__ == "__main__":
    main()
