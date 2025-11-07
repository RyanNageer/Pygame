WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32

PLAYER_LAYER = 4 # Which layer we want the player on
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 2

RED = (255, 0 ,0)
BLACK = (0,0,0)
BLUE = (0, 0, 240)
FPS = 60
# GROUND_LAYER = 1

tilemap = [ # 640 / 32 = 20, 480 / 32 = 15 # B is wall, . is nothing, P is player
    'BBBBBBBBBBBBBBBBBBBB', # List of Strings
'B..E...............B',
'B..................B',
'B....BBB...........B',
'B..................B',
'B.........P........B',
'B..................B',
'B..................B',
'B.....BBB..........B',
'B.......B..........B',
'B.......B..........B',
'B.............E....B',
'B..................B',
'B..................B',
'BBBBBBBBBBBBBBBBBBBB',
]