WIN_WIDTH = 1920
WIN_HEIGHT = 1080
TILESIZE = 32

PLAYER_LAYER = 5 # Which layer we want the player on
ENEMY_LAYER = 4
NPC_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 2

RED = (255, 0 ,0)
BLACK = (0,0,0)
BLUE = (0, 0, 240)
WHITE = (255,255,255)
FPS = 60
# GROUND_LAYER = 1

tilemap = [
    [' ', ' ', 'B', 'P', ' '],   # Row 1
    [' ', 'FLY', ' ', ' ', ' '],  # Row 2 (FLY tile)
    ['B', ' ', ' ', 'E', ' '],   # Row 3 (Block, Enemy)
    [' ', ' ', 'N', ' ', ' ']    # Row 4 (NPC)
]
