from pygame_widgets.constants import USEREVENT
PATH = "D:/Jáchym/Programování/Python/Pampuch"
SQUARE_SIZE = 32
STEP = 8  # must be a divider of SQUARE_SIZE, should be 1/4 of SQUARE SIZE
CHAR_WALL = '#'
CHAR_POINT = '.'
CHAR_EMPTY = ' '
CHAR_MONSTER = 'X'
CHAR_PAMPUCH = 'P'
FPS = 16
# E_GAME_STARTED = USEREVENT
E_DEATH = USEREVENT + 1
E_GAME_FINISHED = USEREVENT + 2
E_STATE_CHANGED = USEREVENT + 3
INSPECTION = 2000
LABEL_RATIO = 18
QUEUE_SIZE = 4
LIVES = {'Original': 4, 'Test': 3, None: 0}
STARTING_LEVEL = {'Original': 0, 'Test': 0, None: None}

