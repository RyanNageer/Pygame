class Player:
    # Class attributes (optional)
    HP = 10
    XP = 0
    LEVEL = 1
    NAME = "Player"
    CLASS = "Psychic"
    SKIN = "White"
    GENDER = "Male"

    # Constructor method (optional, but common)
    def __init__(self, attribute1, attribute2):
        self.attribute1 = attribute1  # Instance attribute
        self.attribute2 = attribute2  # Instance attribute

    # Instance method
    def level_up(self):
        self.LEVEL += 1
        self.HP += self.HP * 1.2
        self.XP = 0

    def gain_xp(self, xp):
        self.XP += xp
        if self.XP >= 100:
            self.level_up()

    def take_damage(self, damage):
        self.HP -= damage
        if self.HP <= 0:
            self.die()