import pygame # package
from menu import * # now we have access to the MainMenu class
from sprites import *
from config import *

class Game(): # Contains our info and variables related to the game, user inputs, game loop, drawing stuff to the screen,
    def __init__(self):
        pygame.init()
        #Menu code
        self.running, self.playing = True, False # game is running but player is not currently playing
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False # Controls for our menu initialized to false. Upon keystroke (ex. UP arrow) they will be set to true
        self.DISPLAY_W, self.DISPLAY_H = 640, 480 # width and height of our canvas
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H)) # Canvas(dimensions)
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H))) # we want player to see what we're drawing. so this line displays the canvas
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.main_menu = MainMenu(self) #  create a MainMenu object called main_menu. the "self" allows game to be passed as an argument to MainMenu, giving MainMenu full access to our game's funtions and variables   
        self.options = OptionsMenu(self) # options menu object, pass in game object     
        self.credits = CreditsMenu(self) # pass in game
        self.curr_menu = self.main_menu # this allows us to swap between what menu is currently being shown to the player

        # ShawCode RPG Tutorial Code
        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(self.font_name)

        self.character_spritesheet= Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')

# CD Codes game loop that just displays text to the screen
#     def game_loop(self):
#         while self.playing: # while player is playing
#             self.check_events() #  for inputs
#             if self.ENTER_KEY: # if start key is pressed
#                 self.playing = False # breaks the while self.playing loop on line 17
#             self.display.fill(self.BLACK) # reset our Canvas before drawing the next image. without this line it's like drawing on the same page in a flip book instead of turning to the next page
#             self.draw_text('Start diggin in yo butt twin', 20, self.DISPLAY_W/2, self.DISPLAY_H/2) # calling the draw_text function we made. we use font size 20 and 480/2 and 270/2 for our coordinates which should put the text in the center of the screen.
#             self.window.blit(self.display, (0,0)) # "BLock Image Transfer" aka copy our canvas onto the visible window that our player sees (0,0) are our top-left XY coordinates
#             pygame.display.update() # physically puts this on the monitor/computer screen
#             self.reset_keys() # sets our flags back to false so we can accept new inputs
    
            
    #CD Codes Menu Tutorial Code

    def check_events(self):
        for event in pygame.event.get(): # checks what the player can do on the computer
            if event.type == pygame.QUIT: # checks if player quits game (for example, hits the X button)
                self.running, self.playing = False, False
                self.curr_menu.run_display = False # turn off the display_menu function
            # check for keyboard inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # player has pressed the Enter key
                    self.ENTER_KEY = True
                if event.key == pygame.K_BACKSPACE: # player has pressed the Enter key
                    self.BACK_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True
                if event.key == pygame.K_DOWN: # player has pressed the Enter key
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP: # player has pressed the Enter key
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False

    def draw_text(self, text, size, x,y): # renders a surface (text_surface) containing our text (text), get_rect() just gives you a Rect object that matches the size of the rendered text surface, then move the rectangle onto the canvas
        font = pygame.font.Font(self.font_name, size) # Font(file_path=None, size=12)
        text_surface = font.render(text, True, self.WHITE) # render(text, antialias, color, background=None): creates a new Surface with the specified text rendered on it. draw text on a new Surface
        # you get a Surface object — basically an image in memory that contains your drawn text pixels.
        text_rect = text_surface.get_rect() # text_rect is a rectangle. This doesn’t draw anything; it’s just metadata describing the position and size of the text surface. rectangle class has 4 main components, x, y, width, and height. this rectangle has the same width & height as our text surface
        text_rect.center = (x,y) # moves the text’s center point to (x, y) coordinates on the canvas (self.display). assigns a x and y position to the center of the rectangle. so we can center the text wherever we want it to be.
        self.display.blit(text_surface, text_rect) # blit(source, dest, area=None, special_flags=0) -> Rect # copy the pixels from text_surface onto our canvas self.display, at the position text_rect

    # ShawCode

    def createTilemap(self):
        for i, row in enumerate(tilemap): # enumerate makes i set to the index and row is [i]
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i) # x, y. Creates a block at this position
                if column == 'P':
                    Player(self, j, i) # j is the column (x) and i is the row (y)
                if column == 'E':
                    Enemy(self, j, i) # pass in game object (self) and coordinates
     
    def new(self):
        
        # pygame.sprite.Sprite is a Simple base class for visible game objects.
        self.all_sprites = pygame.sprite.LayeredUpdates() # Object that will contain all our sprites, walls, and enemies LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates.
        self.blocks = pygame.sprite.LayeredUpdates() # For collisions
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        # self.player = Player(self, 1, 2)
        self.createTilemap()
        

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update() # calls the update function on all_sprites in sprites.py
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen) # All_sprites group, draw will look through all sprites in all_sprites, finds the image and the rectangle and draws it to the window
        self.clock.tick(FPS) # 1 tick per frame, 60 FPS
        pygame.display.update()
    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass
    def intro_screen(self):
        pass

    
# Surface = the photo or picture itself.
# Rect = the picture frame that holds that photo and decides where to hang it on the wall.
