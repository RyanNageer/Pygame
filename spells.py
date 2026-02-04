class Spell:
    def __init__(self, spell_data):
        # metadata
        self.id = spell_data[0]
        self.name = spell_data[1]
        # number of types: 1, 2, or 3
        self.types = [
            t for t in (spell_data[2], spell_data[3], spell_data[4])
            if t not in (None, "", "none")
        ]
        self.damages = [
            d for d in [spell_data[5], spell_data[6], spell_data[7]]
            if d not in (None)
        ]
        # costs order: mana, life, gold
        self.costs = [spell_data[8], spell_data[9], spell_data[10]]
        # number of abilities: 0, 1, or 2
        self.abilities = [spell_data[11], spell_data[12]]

    # conversions functions
    @staticmethod
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
    @staticmethod
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

    def cast(self, player, enemy):
        # check costs
        if self.costs[0] > player.CUR_MANA:
            return "Not enough mana!"
        elif self.costs[1] > player.CUR_HP:
            return "Not enough life!"
        elif self.costs[2] > player.GOLD:
            return "Not enough gold!"

        # deduct costs
        player.CUR_MANA -= self.costs[0]
        player.CUR_HP -= self.costs[1]
        player.GOLD -= self.costs[2]

        # calculate damage based on all elemental interactions of the 3 possible spell types and 3 possible enemy types
        total_damage = 0
        for i in range(len(self.types)):  # number of types
            cur_element_dmg = self.damages[i]
            for j in range (len(enemy.TYPES)):
                cur_element_dmg *= spell_interactions[Spell.type_to_int(self.types[i])][Spell.type_to_int(enemy.TYPES[j])]
            total_damage += cur_element_dmg
        total_damage = max(0, total_damage)  # prevent negative damage, shouldn't ever happen but just in case
        damage_dealt = min(enemy.CUR_HP, int(total_damage))
        enemy.CUR_HP = max(0, enemy.CUR_HP - damage_dealt)

        # apply abilities
        for ability in self.abilities:
            match ability:
                case "burn":
                    enemy.BURN = 5  # burn for 5 turns
                case "stun":
                    enemy.STUN = 1  # stun for 1 turn
                case "freeze":
                    enemy.FREEZE = 3  # freeze for 3 turns
                case "lifesteal":
                    player.CUR_HP = min(player.MAX_HP, player.CUR_HP + int(damage_dealt) / 2) # heal for half damage dealt
                case "playerHeal20":
                    player.CUR_HP = min(player.MAX_HP, player.CUR_HP + 20) # heal for 20 HP
                case "playerAttackBuff2x":
                    player.ATTACK_BUFF2X = 3  # double attack for 3 turns
                case "enemyAttackDebuff2x":
                    enemy.ATTACK_DEBUFF2X = 3  # halve enemy attack for 3 turns
                case "OBLITERATE":
                    OBLITERATE()
                case "OBLITERATE AGAIN":
                    OBLITERATEAGAIN()

        return f"{player.NAME} uses {self.name}!"


# spell format: [id#, name, num_types, type1, type2, type3, type1dmg, type2dmg, type3dmg, mana cost, life cost, gold cost, ability1, ability2]
spell_database = [ 
    # fire spells
    Spell([0, "Flame", "fire", None, None, 10, 0, 0, 10, 0, 0, None, None]), # standard fire attack
    [1,],
    Spell([2, "Fireball", "fire", None, None, 20, 0, 0, 20, 0, 0, "burn", None]), # burn the enemy with fire damage

    # ice spells
    Spell([3, "Icicle", "ice", None, None, 10, 0, 0, 10, 0, 0, None, None]), # standard ice attack
    [4,],
    [5,],

    # earth spells
    Spell([6, "Rock", "earth", None, None, 10, 0, 0, 10, 0, 0, None, None]), # standard earth attack
    [7,],
    [8,],

    # water spells
    Spell([9, "Splash", "water", None, None, 10, 0, 0, 10, 0, 0, None, None]), # standard water attack
    [10,], 
    [11,],

    # electric spells
    Spell([12, "Zap", "electric", None, None, 10, 0, 0, 10, 0, 0, None, None]), # standard electric attack
    Spell([13, "Stun", "electric", None, None, 0, 0, 0, 10, 0, 0, "stun", None]), # standard stun debuff
    Spell([14, "Lightning Bolt", "electric", None, None, 20, 0, 0, 20, 0, 0, "stun", None]), # stun the enemy with electric damage

    ##########
    # trifecta: spirit beats shadow, shadow beats basic, basic beats spirit. no other elemental interactions
    ##########
    # basic spells
    Spell([15, "Punch", "basic", None, None, 5, 0, 0, 0, 0, 0, None, None]), # standard basic attack
    [16,],
    Spell([17, "Ground Pound", "basic", None, None, 30, 0, 0, 20, 0, 0, None, None]), # jump up and slam the enemy
    # spirit spells
    Spell([18, "Heal", "spirit", None, None, 0, 0, 0, 20, 0, 0, "playerHeal20", None]), # standard heal
    Spell([19, "Insult", "spirit", None, None, 30, 0, 0, 20, 0, 0, None, None]), # call the enemy a ^%&*!&#$ *%*@$#!*#$^*
    [20,],
    # shadow spells
    Spell([21, "Demonic Strength", "shadow", None, None, 0, 0, 0, 25, 10, 0, "playerAttackBuff2x", None]), # trade your life for an attack boost
    Spell([22, "Void Blast", "shadow", None, None, 50, 0, 0, 30, 5, 0, None, None]), # trade your life for a powerful shadow attack
    [23,],

    # two-typed spells
    Spell([24, "Engulfing Steam", "water", "fire", None, 15, 15, 0, 20, 0, 0, None, None]), # scald the enemy with hot water stream that turns to steam when it hits
    Spell([25, "Flex", "spirit", "basic", None, 49, 1, 0, 0, 0, 100, None, None]), # throw money at enemy
    Spell([26, "Drain Soul", "shadow", "spirit", None, 50, 50, 0, 100, 50, 0, "lifesteal", "enemyAttackDebuff2x"]), # drain soul and power from enemy to heal
    # three-typed spells
    Spell([27, "Thermal Paradox Beam", "fire", "ice", "electric", 50, 50, 50, 150, 0, 0, "burn", "freeze"]),
    [28,],
    [29,],
    # ultimate spell (can only be obtained by beating final boss)
    Spell([30, "OBLITERATE", "shadow", "spirit", "basic", 100, 100, 100, 100, 100, 100, "OBLITERATE", "OBLITERATE AGAIN"]), #OBLITERATE
]

#  fire,  ice,   earth, water,electric,basic,spirit,shadow
spell_interactions = [
    [1,     2,     0.5,   0.5,   1,     1,     1,     1],    # fire damage
    [0.5,   1,     1.5,   2,     1,     1,     1,     1],    # ice damage
    [1.5,   1.5,   1,     0.75,  2,     1,     1,     1],    # earth damage
    [2,     0.5,   2,     1,     0.75,  1,     1,     1],    # water damage
    [1,     1.5,   0.5,   2,     1,     1,     1,     1],    # electric damage
    [1,     1,     1,     1,     1,     1,     2.5,   0.25], # basic damage
    [1,     1,     1,     1,     1,     0.25,  1,     2.5],    # spirit damage
    [1,     1,     1,     1,     1,     2.5,   0.25,  1],    # shadow damage
 ]