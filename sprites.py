import pygame
from config import *
from game import *
import math
import random

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert() # self.sheet is going to be the loaded image containing the sprite sheet, convert loads the image in faster so our game doesnt slow down

    def get_sprite(self, x, y, width, height): # cut out sprite from sprite sheet
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height)) # selects cutout from sprite sheet image and blits that particular sprite from the image to the screen
        sprite.set_colorkey(BLACK) # Set color key so we don't have a black background
        return sprite 
class Player(pygame.sprite.Sprite): # Layer 3
    def __init__(self, game, x, y): # game object, and coordinates to position the player at

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups) # calls init for inherited class, by passing in self.groups we add the player to the all sprites group

        self.x = x * TILESIZE # everything will be 32x32 pixels
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        # image_to_load = pygame.image.load("img/single2.png")
        # self.image = pygame.Surface([self.width, self.height]) # get an image that can later be drawn to the screen
        # self.image.set_colorkey(BLACK) # makes the specified color transparent
        # self.image.blit(image_to_load, (0,0)) # draw the image we've loaded in onto a surface
        
        # x position in the sprite sheet, y position in the spritesheet, x amount of pixels across, y amount of pixels down. width & height == 32
        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height) # calling get_sprite() from the Spritesheet class we made. referring to the Spritesheet object from the Spritesheet class we created above, we created the object in our __init__ function for the game class

        self.rect = self.image.get_rect() # set self.rect to be same size of the player
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()

        self.rect.x += self.x_change # once we see a change in position due to movement
        self.collide_blocks('x') # we can check for collision
        self.rect.y += self.y_change # change is a temporary variable of sorts and we use it to update the actual rectangle that refers to the player
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0


    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: # if left arrow key pressed
            self.x_change -= PLAYER_SPEED # reduce the x axis to move the player left
            self.facing = 'left'
        if keys[pygame.K_RIGHT]: # if left arrow key pressed
            self.x_change += PLAYER_SPEED # reduce the x axis to move the player left
            self.facing = 'right'
        if keys[pygame.K_UP]: # if left arrow key pressed
            self.y_change -= PLAYER_SPEED # reduce the y axis to move the player up
            self.facing = 'up'
        if keys[pygame.K_DOWN]: # if left arrow key pressed
            self.y_change += PLAYER_SPEED # increase the y axis to move the player down
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) # function from sprite library, checks if the rect of one sprite intersects with the rect of another sprite
            # Third parameter (one marked false) asks if you want to delete the sprite when it has a collision
            if hits:
                if self.x_change > 0: # hits[0] is the wall we're colliding with
                    self.rect.x = hits[0].rect.left - self.rect.width # because we takeaway the width of the rectangle, this creates the collision effect so the player cant walk on top the bock
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right


        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

class Block(pygame.sprite.Sprite): # Layer 2
    def __init__(self, game, x, y): # game object and position on the tilemap

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE # Every sprite needs an image and rectangle
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        #self.image = pygame.Surface([self.width, self.height]) # image will always be 32 pixels long and wide 
        #self.image.fill(BLUE)

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite): # Layer 1
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups) # sets up all the sprite internals (so you get methods like .add(), .kill(), .groups()) and automatically adds the sprite to any Group objects you pass

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height) # get the image
        self.rect = self.image.get_rect() # create a rectangle and makes it the same size as self.image
        self.rect.x = self.x # assign the top left coorinates for the rectangle
        self.rect.y = self.y