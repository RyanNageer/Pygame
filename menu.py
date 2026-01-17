import pygame
import inflect
from config import *
from sprites import * 

# menu class from CD Codes
class Menu():
    def __init__(self, game): #reference to ourself and to a game object. for clarity python doesnt enforce types automatically so "game" here could techincally be any data type or object type, but we are gonna pass in a Game object.
        self.game = game # By doing self.game = game, you save a reference on the Menu instance, so other methods (e.g., draw(), update(), handle_input()) can access it later as self.game.
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 # Save a reference to the middle of the screen in a variable
        self.run_display = True # tells our menu to keep running
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) # we create a rectangle to act as our cursor. its 20x20 pixels
        self.offset = -100 # offset by -100 shift the cursor horizontally so it appears to the left of the text instead of directly on top of it
    
    def draw_cursor(self, surface=None):
        if surface is None:
            surface = self.game.display
        
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y, surface=surface) # defined in the game class

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0)) # copy our canvas onto the visible window that our player sees are our top-left XY coordinates
        # Copy the pixels from self.game.display (the off-screen canvas) onto self.game.window (the visible screen), starting at coordinates (0, 0)
        pygame.display.update()
        self.game.reset_keys() # reset inputs to false

    # Source - https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font
# Posted by SpoonMeiser, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-22, License - CC BY-SA 3.0

    def renderTextCenteredAt(self, text, font, colour, x, y, screen, allowed_width):
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = ' '.join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x - fw / 2
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh

    def renderTextLeft(self, text, font, colour, x, y, screen, allowed_width):
        words = text.split()
        lines = []

        while words:
            line_words = []
            while words:
                line_words.append(words.pop(0))
                fw, fh = font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break
            lines.append(' '.join(line_words))

        y_offset = 0
        for line in lines:
            screen.blit(font.render(line, True, colour), (x, y + y_offset))
            y_offset += font.size(line)[1]
    
    def wait_for_keypress(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the window is closed
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e or event.key == pygame.K_RETURN:
                        return  # Exit the loop when 'e' is pressed



class MainMenu(Menu): # class Child(Parent) MainMenu extends the Menu class. Menu is the parent, MainMenu is the child
    def __init__(self, game): # needs its own init function and reference to the game
        Menu.__init__(self,game) # Parent.__init__ We reuse menu's init, so now we have all the same menu-class variables for the MainMenu object
        self.state = "Start" # state variable that keeps track of which option the cursor is pointing at in the Main Menu
        self.startx, self.starty = self.mid_w, self.mid_h + 30 # Aligning where on the screen we want to place our "start game" text
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50 # Aligning options below the "start game"
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) # midpoint of the top edge of the rectangle
        # midtop is one of the position attributes of a Pygame Rect object

    def display_menu(self):
        self.run_display = True # Show the updated menu screen (canvas), based off user inputs, to the user.
        while self.run_display:
            self.game.check_events() # check for inputs. function from the game class
            self.check_input()
            self.game.display.fill(self.game.BLACK) # display is our canvas, from the game class.
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20) # using our draw_text(self, text, size, x,y) function from the game class. this gets a rectangle, puts it in the position we want, and then puts the text in that rectangle at the position on the screen we want.
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            
            self.draw_cursor()
            self.blit_screen() # put our updated canvas onto the visible screen

    def move_cursor(self): # the menu from Top to bottom will be Start Game, Options, Credits
        if self.game.DOWN_KEY:
            if self.state == 'Start': # if cursor is at start and we receive an input to move the cursor down, we  must adjust the cursor to move down to options
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy) # midtop is a variable from our MainMenu class
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        
        if self.game.UP_KEY:
            if self.state == 'Credits': 
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy) # midtop is a variable from our MainMenu class
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
                

    def check_input(self):
        self.move_cursor() # every frame we will check for input and adjust the cursor accordingly
        if self.game.ENTER_KEY: # If the player clicks Enter
            if self.state == 'Start':     
                self.game.playing = True
                self.game.new(tilemap1)
                self.game.main()
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu): # Menu subclass
    def __init__(self, game): # pass in game object
        Menu.__init__(self, game) # run init function for Menu
        self.state = 'Volume'
        self.volx, self.voly, = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display: # While the options menu is running
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0,0,0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30) # title of the sreeen
            self.game.draw_text("Volume", 15, self.volx, self.voly)  # First option
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self): # check input for the optionsmenu class
        if self.game.BACK_KEY or self.game.ESC_KEY: # if back_key is set to ON meaning it's been pressed this frame
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY: # allows us to navigate between volume and controls in the options menu
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

        elif self.game.ENTER_KEY:
        # TO-DO: Create a Volume Menu and a Controls Menu
            pass

class CreditsMenu(Menu): # child of Menu
    def __init__(self, game):
        Menu.__init__(self,game)

    def display_menu(self):
        self.run_display = True
        while self.run_display: # runs every frame
            self.game.check_events()
            if self.game.ENTER_KEY or self.game.BACK_KEY or self.game.ESC_KEY: # if enter or backspace are pressed
                self.game.curr_menu = self.game.main_menu # exit credits
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20) # draw_text function we made in the game class
            self.game.draw_text('Ryan Nageer', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen() # display shit to screen and set inputs back to false every frame

class BattleMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        # Use integer dimensions for the surface
        self.battle_display = pygame.Surface((self.game.DISPLAY_W, 300)) # Canvas(dimensions)
        self.player_stats = pygame.Surface((380, 167))
        self.enemy_stats = pygame.Surface((500, 200))
        self.superstate = "Base"
        self.state = "Attack"
        self.attackx, self.attacky = 200, 180 # Aligning where on the screen we want to place our "start game" text
        self.itemx, self.itemy = 600, 180 # Aligning options below the "start game"
        self.talkx, self.talky = 1000, 180
        self.fleex, self.fleey = 1400, 180
        self.textx, self.texty = 150, 60
        
        self.player_namex, self.player_namey =  110, 40
        self.player_hpx, self.player_hpy = 120, 80
        self.player_xpx, self.player_xpy = 120, 120
        
        self.enemy_hpx, self.enemy_hpy = 120, 60
        self.enemy_namex, self.enemy_namey = 120, 120
        self.enemy_moving = 0
        
        self.cursor_rect.midtop = (self.attackx + self.offset, self.attacky) # midpoint of the top edge of the rectangle
        self.textbox = "An enemy approaches!"
        # midtop is one of the position attributes of a Pygame Rect object
        
        

    def battle_init(self, enemy):
        p = inflect.engine() # use the inflect module to check for vowels
        self.textbox = f"{p.a(enemy.name)[0].upper()}{p.a(enemy.name)[1:]} appears!" # picks between a and an and capitalizes the A
        self.state = "Attack"
        

    def display_menu(self, player, enemy, enemy_defeated_flag=0): # Does NOT adjust any values, only displays.
        # Draw a single frame of the battle UI.
        # The outer `Game.battle` loop handles the event polling and input,
        # so this method should only render and return each frame.
        
        
        self.battle_display.fill(self.game.BLACK)
        self.player_stats.fill(self.game.WHITE)
        self.enemy_stats.fill(self.game.BLACK)

        # Draw text directly onto the battle surface so it will be visible
        if self.superstate == "Base":
            self.game.draw_text('Attack', 40, self.attackx, self.attacky, surface=self.battle_display) # using updated draw_text that accepts surface variable
            self.game.draw_text('Item', 40, self.itemx, self.itemy, surface=self.battle_display)
            self.game.draw_text('Talk', 40, self.talkx, self.talky, surface=self.battle_display)
            self.game.draw_text('Flee', 40, self.fleex, self.fleey, surface=self.battle_display)
        elif self.superstate == "Spells":
            self.game.draw_text(spells[player_spellbook[0]][1], 40, self.attackx, self.attacky, surface=self.battle_display) # using updated draw_text that accepts surface variable
            self.game.draw_text(spells[player_spellbook[1]][1], 40, self.itemx, self.itemy, surface=self.battle_display)
            self.game.draw_text(spells[player_spellbook[2]][1], 40, self.talkx, self.talky, surface=self.battle_display)
            self.game.draw_text(spells[player_spellbook[3]][1], 40, self.fleex, self.fleey, surface=self.battle_display)
        
        self.game.draw_text(f"HP: {enemy.CUR_HP} / {enemy.MAX_HP}", 40, self.enemy_hpx, self.enemy_hpy, surface=self.enemy_stats)
        self.game.draw_text(f"{enemy.name}", 40, self.enemy_namex, self.enemy_namey, surface=self.enemy_stats)
        
        self.game.draw_text(f"HP: {player.CUR_HP} / {player.MAX_HP}", 40, self.player_hpx, self.player_hpy, color=self.game.BLACK, surface=self.player_stats)
        self.game.draw_text(f"{player.name}", 40, self.player_namex, self.player_namey, color=self.game.BLACK, surface=self.player_stats)       
        self.game.draw_text(f"XP: {player.CUR_XP} / {player.XP_NEEDED}", 40, self.player_xpx, self.player_xpy, color=self.game.BLACK, surface=self.player_stats)
        
       #(text, font, colour, x, y, screen, allowed_width)    
       
        font = pygame.font.Font(self.game.font_name, 40)
        self.renderTextLeft(self.textbox, font, WHITE, self.textx, self.texty, self.battle_display, 1600)
        if self.enemy_moving == 0:
            self.draw_cursor(surface=self.battle_display)
        self.blit_battle_menu(enemy, enemy_defeated_flag)

    def blit_battle_menu(self, enemy, enemy_defeated_flag=0): # Redisplays the whole battle menu, does NOT affect any values
        self.game.window.blit(enemy.battle_background, (0,0)) # Draw background image
        if enemy.CUR_HP > 0 and enemy_defeated_flag == 0:
            self.game.window.blit(enemy.battle_sprite, (self.game.DISPLAY_W / 2, 350))
        self.game.window.blit(self.battle_display, (0, int((self.game.DISPLAY_H / 2) + 300))) # copy our canvas onto the visible window that our player sees are our top-left XY coordinates
        self.game.window.blit(self.player_stats, (1420, 673))
        self.game.window.blit(self.enemy_stats, (0, 0))
        
        # Copy the pixels from self.game.display (the off-screen canvas) onto self.game.window (the visible screen), starting at coordinates (0, 0)
        pygame.display.update()
        self.game.reset_keys() # reset inputs to false

    def move_cursor(self, key): # the menu from Top to bottom will be Start Game, Options, Credits
        if key == pygame.K_RIGHT:
            if self.superstate == "Base":
                if self.state == 'Attack': # if cursor is at start and we receive an input to move the cursor down, we  must adjust the cursor to move down to options
                    self.cursor_rect.midtop = (self.itemx + self.offset, self.itemy) # midtop is a variable from our MainMenu class
                    self.state = 'Item'
                elif self.state == 'Item':
                    self.cursor_rect.midtop = (self.talkx + self.offset, self.talky)
                    self.state = 'Talk'
                elif self.state == 'Talk':
                    self.cursor_rect.midtop = (self.fleex + self.offset, self.fleey)
                    self.state = 'Flee'
                elif self.state == 'Flee':
                    self.cursor_rect.midtop = (self.attackx + self.offset, self.attacky)
                    self.state = 'Attack'
            elif self.superstate == "Spells":
                if self.state == 'Spell1':
                    self.cursor_rect.midtop = (self.itemx + self.offset, self.itemy) # midtop is a variable from our MainMenu class
                    self.state = 'Spell2'
                elif self.state == 'Spell2':
                    self.cursor_rect.midtop = (self.talkx + self.offset, self.talky)
                    self.state = 'Spell3'
                elif self.state == 'Spell3':
                    self.cursor_rect.midtop = (self.fleex + self.offset, self.fleey)
                    self.state = 'Spell4'
                elif self.state == 'Spell4':
                    self.cursor_rect.midtop = (self.attackx + self.offset, self.attacky)
                    self.state = 'Spell1'
        
        if key == pygame.K_LEFT:
            if self.superstate == "Base":
                if self.state == 'Attack': 
                    self.cursor_rect.midtop = (self.fleex + self.offset, self.fleey) # midtop is a variable from our MainMenu class
                    self.state = 'Flee'
                elif self.state == 'Item':
                    self.cursor_rect.midtop = (self.attackx + self.offset, self.attacky)
                    self.state = 'Attack'
                elif self.state == 'Talk':
                    self.cursor_rect.midtop = (self.itemx + self.offset, self.itemy)
                    self.state = 'Item'
                elif self.state == 'Flee':
                    self.cursor_rect.midtop = (self.talkx + self.offset, self.talky)
                    self.state = 'Talk'
            elif self.superstate == "Spells":
                if self.state == 'Spell1': 
                    self.cursor_rect.midtop = (self.fleex + self.offset, self.fleey) # midtop is a variable from our MainMenu class
                    self.state = 'Spell4'
                elif self.state == 'Spell2':
                    self.cursor_rect.midtop = (self.attackx + self.offset, self.attacky)
                    self.state = 'Spell1'
                elif self.state == 'Spell3':
                    self.cursor_rect.midtop = (self.itemx + self.offset, self.itemy)
                    self.state = 'Spell2'
                elif self.state == 'Spell4':
                    self.cursor_rect.midtop = (self.talkx + self.offset, self.talky)
                    self.state = 'Spell3'

    def attempt_move(self, player, enemy, spell_index):
        if spell_index >= len(player_spellbook):
            print("ERROR: spell_index out of range")
            return 0
        elif spells[player_spellbook[spell_index]][9] > player.CUR_MANA:
            self.textbox = "Not enough mana!"
            return 0
        elif spells[player_spellbook[spell_index]][10] > player.CUR_HP:
            self.textbox = "Not enough life!"
            return 0
        elif spells[player_spellbook[spell_index]][11] > player.GOLD:
            self.textbox = "Not enough gold!"
            return 0
        else:
            self.textbox = f"{player.name} uses {spells[player_spellbook[spell_index]][1]}!"

            # deduct costs
            player.CUR_MANA -= spells[player_spellbook[spell_index]][9]
            player.CUR_HP -= spells[player_spellbook[spell_index]][10]
            player.GOLD -= spells[player_spellbook[spell_index]][11]

            # calculate damage based on all elemental interactions of the 3 possible spell types and 3 possible enemy types
            damage = 0.0
            for i in range(0, spells[player_spellbook[spell_index]][2]):
                cur_element_dmg = spells[player_spellbook[spell_index]][6+i]
                for j in range (0, enemy.NUM_TYPES):
                    cur_element_dmg *= spell_interactions[type_to_int(spells[player_spellbook[spell_index]][3+i])][type_to_int(enemy.TYPES[j])]
                damage += cur_element_dmg
            enemy.CUR_HP = max(0, enemy.CUR_HP - int(damage))

            # attempt to resolve abilities
            
            self.display_menu(player, enemy)
            pygame.time.delay(1000)
            return 1

    def check_input(self, key, player, enemy):
        successful_move = 0
        self.move_cursor(key) # every frame we will check for input and adjust the cursor accordingly
        if key == pygame.K_RETURN or key == pygame.K_e: # If the player clicks Enter or INTERACT_KEY
            if self.superstate == "Base":
                if self.state == 'Attack':     
                #    self.textbox = "Player Attacks!"               
                #    enemy.CUR_HP = max(0, enemy.CUR_HP - player.ATK)
                #    self.display_menu(player, enemy)
                #    pygame.time.delay(1000)
                #    successful_move = 1
                    self.superstate = "Spells"
                    self.state = "Spell1"
                    successful_move = 0
                elif self.state == 'Item':
                    self.textbox = "You don't have any items"
                    successful_move = 0
                elif self.state == 'Talk':
                   self.textbox ="The enemy doesn't seem to be very talkative"
                   successful_move = 0
                elif self.state == 'Flee':
                    self.textbox ="Unable to flee!"
                    successful_move = 0
                else:
                    print ("ERROR: State self.malfunctioned")
                    successful_move = 0
            elif self.superstate == "Spells":
                if self.state == "Spell1":
                    successful_move = self.attempt_move(player, enemy, 0)
                elif self.state == "Spell2":
                    successful_move = self.attempt_move(player, enemy, 1)
                elif self.state == "Spell3":
                    successful_move = self.attempt_move(player, enemy, 2)
                elif self.state == "Spell4":
                    successful_move = self.attempt_move(player, enemy, 3)
                else:
                    print ("ERROR: Spell State self.malfunctioned")
                    successful_move = 0
        return successful_move
    

    def enemy_move(self, player, enemy):
        if enemy.CUR_HP <= 0:
            pygame.time.delay(1000) # wait 1 second
            self.textbox = f"{enemy.name} has been defeated! 2 XP gained. Press e to return to overworld."
            player.CUR_XP += 2
            self.display_menu(player, enemy, 1) # This will remove the enemy's sprite from the screen
            self.wait_for_keypress()
            self.textbox = ""
            return
        self.textbox = f"{enemy.name} attacks!"
        player.CUR_HP = max(0, player.CUR_HP - enemy.ATK)
        self.enemy_moving = 1
        self.display_menu(player, enemy)
        # I want the cursor to stop being drawn to the screen when an enemy is attacking
        
        pygame.time.delay(1000)
        self.enemy_moving = 0
        
            
