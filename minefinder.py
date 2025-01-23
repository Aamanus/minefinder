from src.gdraw import gDraw
from src.minefield import MineField
from src.settings import gSettings, gDifficulties
import argparse

def main():
    """Main function to run the game"""
    # collect input args from the command line to allow some testing overrides.  
    # --veasy, which whill set initial game mode to VEASY
    # --width, which will set the width of the minefield
    # --height, which will set the height of the minefield
    # --difficulty, which will set the difficulty of the minefield
    # --help, which will display the help message
    parser = argparse.ArgumentParser(description="Minefinder")
    parser.add_argument("--veasy", action="store_true", help="Set initial game mode to VEASY")
    parser.add_argument("--width", type=int, help="Set the width of the minefield")
    parser.add_argument("--height", type=int, help="Set the height of the minefield")
    parser.add_argument("--difficulty", type=str, help="Set the difficulty of the minefield")
    args = parser.parse_args()
    init_difficulty = gDifficulties.EASY
    init_width = gSettings.MINEFIELD_WIDTH
    init_height = gSettings.MINEFIELD_HEIGHT
    if args.width:
        init_width = args.width

    if args.height:
        init_height = args.height

    if args.veasy:
        init_difficulty = gDifficulties.VEASY
        init_width = 5
        init_height = 5
    # Create the game window
    screen_width = gSettings.SCREEN_WIDTH
    screen_height = gSettings.SCREEN_HEIGHT
    gdraw = gDraw(screen_width, screen_height)

    # Create the minefield
    minefield = MineField(
        init_width,
        init_height,
        init_difficulty,
        gdraw
    )
    print("Minefield created")
    # minefield is created and drawn, start main loop and test
    gdraw.start_main_loop()

if __name__ == "__main__":
    main()
