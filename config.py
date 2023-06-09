WINDOW_TITLE = "Minesweeper"

# Sizes
ROWS = 10
COLS = 10
NUM_OF_MINES = 10
WIN_CELLS = ROWS * COLS - NUM_OF_MINES
CELL_WIDTH = 2
CELL_HEIGHT = 2
ICON_SIZE = (32, 32)

# Styles
NORMAL_STYLE = "Normal.TButton"
SWEEPED_STYLE = "Sweeped.TButton"
FLAG_STYLE = "Flag.TButton"
MINE_STYLE = "Mine.TButton"

# Images
WINDOW_ICON = "assets/bomb.ico"
FLAG_ICON = "assets/flag.png"
MINE_ICON = "assets/mine.png"

# Events
GAME_WON_EVENT = "<<GameWon>>"
GAME_LOST_EVENT = "<<GameLost>>"
