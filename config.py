from asyncio.windows_events import NULL


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

# spell format: [id#, name, type1, type2, type3, type1dmg, type2dmg, type3dmg, mana cost, life cost, gold cost, ability1, ability2]
spells = [ 
    # fire spells
    [0, "Flame", "fire", NULL, NULL, 10, 0, 0, 10, 0, 0, NULL, NULL], # standard fire attack
    [1,],
    [2, "Fireball", "fire", NULL, NULL, 20, 0, 0, 20, 0, 0, "burn", NULL], # burn the enemy with fire damage

    # ice spells
    [3, "Icicle", "ice", NULL, NULL, 10, 0, 0, 10, 0, 0, NULL, NULL], # standard ice attack
    [4,],
    [5,],

    # earth spells
    [6, "Rock", "earth", NULL, NULL, 10, 0, 0, 10, 0, 0, NULL, NULL], # standard earth attack
    [7,],
    [8,],

    # water spells
    [9, "Splash", "water", NULL, NULL, 10, 0, 0, 10, 0, 0, NULL, NULL], # standard water attack
    [10,], 
    [11,],

    # electric spells
    [12, "Zap", "electric", NULL, NULL, 10, 0, 0, 10, 0, 0, NULL, NULL], # standard electric attack
    [13, "Stun", "electric", NULL, NULL, 0, 0, 0, 10, 0, 0, "stun", NULL], # basic stun debuff
    [14, "Lightning Bolt", "electric", NULL, NULL, 20, 0, 0, 20, 0, 0, "stun", NULL], # stun the enemy with electric damage

    ##########
    # trifecta: spirit beats shadow, shadow beats basic, basic beats spirit. no other elemental interactions
    ##########
    # basic spells
    [15, "Punch", "basic", NULL, NULL, 5, 0, 0, 0, 0, 0, NULL, NULL], # standard basic attack
    [16,],
    [17, "Ground Pound", "basic", NULL, NULL, 30, 0, 0, 20, 0, 0, NULL, NULL], # jump up and slam the enemy
    # spirit spells
    [18, "Heal", "spirit", NULL, NULL, 0, 0, 0, 20, 0, 0, "playerHeal20", NULL], # standard heal
    [19, "Insult", "spirit", NULL, NULL, 30, 0, 0, 20, 0, 0, NULL, NULL], # call the enemy a ^%&*!&#$ *%*@$#!*#$^*
    [20,],
    # shadow spells
    [21, "Demonic Strength", "shadow", NULL, NULL, 0, 0, 0, 25, 10, 0, "playerAttackBuff2x", NULL], # trade your life for an attack boost
    [22, "Void Blast", "shadow", NULL, NULL, 50, 0, 0, 30, 5, 0, NULL, NULL], # trade your life for a powerful shadow attack
    [23,],

    # two-typed spells
    [24, "Engulfing Steam", "water", "fire", NULL, 15, 15, 0, 20, 0, 0, NULL, NULL], # scald the enemy with hot water stream that turns to steam when it hits
    [25, "Flex", "spirit", "basic", NULL, 49, 1, 0, 0, 0, 100, NULL, NULL], # throw money at enemy
    [26, "Drain Soul", "shadow", "spirit", NULL, 50, 50, 0, 100, 50, 0, "lifesteal", "enemyAttackDebuff0.5x"], # drain soul and power from enemy to heal
    # three-typed spells
    [27, "Thermal Paradox Beam", "fire", "ice", "electric", 50, 50, 50, 150, 0, 0, "burn", "freeze"],
    [28,],
    [29,],
    # ultimate spell (can only be obtained by beating final boss)
    [30, "OBLITERATE", "shadow", "spirit", "basic", 100, 100, 100, 100, 100, 100, "OBLITERATE", "OBLITERATE AGAIN"], #OBLITERATE
]

spellbook = [0, 14, 15, 27]  # For testing, player starts with Flame, Lightning Bolt, Punch, and Thermal Paradox Beam

tilemap1 = [
    [' ', 'B', ' ', 'B', ' '],
    [' ', 'B', 'B', 'B', 'P'],
    [' ', 'B', 'B', 'B', ' '],   #
    [' ', ' ', ' ', ' ', ' '],  # (FLY tile)
    ['B', ' ', ' ', ' ', ' '],   #  (Block, Enemy)
    [' ', ' ', 'N', ' ', ' '],    #  (NPC)
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' '],
]
tilemap2 = [
    [' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],   
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'FLY', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',],  
]
