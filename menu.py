import pygame

class Menu():
    def __init__(self, game): #reference to ourself and to a game object. for clarity python doesnt enforce types automatically so "game" here could techincally be any data type or object type, but we are gonna pass in a Game object.
        self.game = game # By doing self.game = game, you save a reference on the Menu instance, so other methods (e.g., draw(), update(), handle_input()) can access it later as self.game.
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 # Save a reference to the middle of the screen in a variable
        self.run_display = True # tells our menu to keep running
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) # we create a rectangle to act as our cursor. its 20x20 pixels
        self.offset = -100 # offset by -100 shift the cursor horizontally so it appears to the left of the text instead of directly on top of it
    
    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y) # defined in the game class

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0)) # copy our canvas onto the visible window that our player sees are our top-left XY coordinates
        # Copy the pixels from self.game.display (the off-screen canvas) onto self.game.window (the visible screen), starting at coordinates (0, 0)
        pygame.display.update()
        self.game.reset_keys() # reset inputs to false

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
                self.game.new()
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
