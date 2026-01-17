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

# spell format: [id#, name, num_types, type1, type2, type3, type1dmg, type2dmg, type3dmg, mana cost, life cost, gold cost, ability1, ability2]
spells = [ 
    # fire spells
    [0, "Flame", 1, "fire", None, None, 10, 0, 0, 10, 0, 0, None, None], # standard fire attack
    [1,],
    [2, "Fireball", 1, "fire", None, None, 20, 0, 0, 20, 0, 0, "burn", None], # burn the enemy with fire damage

    # ice spells
    [3, "Icicle", 1, "ice", None, None, 10, 0, 0, 10, 0, 0, None, None], # standard ice attack
    [4,],
    [5,],

    # earth spells
    [6, "Rock", 1, "earth", None, None, 10, 0, 0, 10, 0, 0, None, None], # standard earth attack
    [7,],
    [8,],

    # water spells
    [9, "Splash", 1, "water", None, None, 10, 0, 0, 10, 0, 0, None, None], # standard water attack
    [10,], 
    [11,],

    # electric spells
    [12, "Zap", 1, "electric", None, None, 10, 0, 0, 10, 0, 0, None, None], # standard electric attack
    [13, "Stun", 1, "electric", None, None, 0, 0, 0, 10, 0, 0, "stun", None], # basic stun debuff
    [14, "Lightning Bolt", 1, "electric", None, None, 20, 0, 0, 20, 0, 0, "stun", None], # stun the enemy with electric damage

    ##########
    # trifecta: spirit beats shadow, shadow beats basic, basic beats spirit. no other elemental interactions
    ##########
    # basic spells
    [15, "Punch", 1, "basic", None, None, 5, 0, 0, 0, 0, 0, None, None], # standard basic attack
    [16,],
    [17, "Ground Pound", 1, "basic", None, None, 30, 0, 0, 20, 0, 0, None, None], # jump up and slam the enemy
    # spirit spells
    [18, "Heal", 1, "spirit", None, None, 0, 0, 0, 20, 0, 0, "playerHeal20", None], # standard heal
    [19, "Insult", 1, "spirit", None, None, 30, 0, 0, 20, 0, 0, None, None], # call the enemy a ^%&*!&#$ *%*@$#!*#$^*
    [20,],
    # shadow spells
    [21, "Demonic Strength", 1, "shadow", None, None, 0, 0, 0, 25, 10, 0, "playerAttackBuff2x", None], # trade your life for an attack boost
    [22, "Void Blast", 1, "shadow", None, None, 50, 0, 0, 30, 5, 0, None, None], # trade your life for a powerful shadow attack
    [23,],

    # two-typed spells
    [24, "Engulfing Steam", 2, "water", "fire", None, 15, 15, 0, 20, 0, 0, None, None], # scald the enemy with hot water stream that turns to steam when it hits
    [25, "Flex", 2, "spirit", "basic", None, 49, 1, 0, 0, 0, 100, None, None], # throw money at enemy
    [26, "Drain Soul", 2, "shadow", "spirit", None, 50, 50, 0, 100, 50, 0, "lifesteal", "enemyAttackDebuff0.5x"], # drain soul and power from enemy to heal
    # three-typed spells
    [27, "Thermal Paradox Beam", 3, "fire", "ice", "electric", 50, 50, 50, 150, 0, 0, "burn", "freeze"],
    [28,],
    [29,],
    # ultimate spell (can only be obtained by beating final boss)
    [30, "OBLITERATE", 3, "shadow", "spirit", "basic", 100, 100, 100, 100, 100, 100, "OBLITERATE", "OBLITERATE AGAIN"], #OBLITERATE
]

player_spellbook = [0, 14, 15, 27]  # For testing, player starts with Flame, Lightning Bolt, Punch, and Thermal Paradox Beam

def type_to_int(t):
    return {
        "fire": 0,
        "ice": 1,
        "earth": 2,
        "water": 3,
        "electric": 4,
        "basic": 5,
        "spirit": 6,
        "shadow": 7
    }[t]

def int_to_type(i):
    return {
        0: "fire",
        1: "ice",
        2: "earth",
        3: "water",
        4: "electric",
        5: "basic",
        6: "spirit",
        7: "shadow"
    }[i]

#  fire,  ice,   earth, water,electric,basic,spirit,shadow
spell_interactions = [
    [1,     2,     0.5,   0.5,   1,     1,     1,     1],    # fire damage
    [0.5,   1,     1.5,   2,     1,     1,     1,     1],    # ice damage
    [1.5,   1.5,   1,     0.75,  2,     1,     1,     1],    # earth damage
    [2,     0.5,   2,     1,     0.75,  1,     1,     1],    # water damage
    [1,     1.5,   0.5,   2,     1,     1,     1,     1],    # electric damage
    [1,     1,     1,     1,     1,     1,     4,     0.25], # basic damage
    [1,     1,     1,     1,     1,     0.25,  1,     4],    # spirit damage
    [1,     1,     1,     1,     1,     4,     0.25,  1],    # shadow damage
 ]

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
