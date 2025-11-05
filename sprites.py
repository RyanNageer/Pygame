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
class Player(pygame.sprite.Sprite):
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

        self.rect.x += self.x_change
        self.rect.y += self.y_change # change is a temporary variable of sorts and we use it to update the actual rectangle that refers to the player

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

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # game object and position on the tilemap

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE # Every sprite needs an image and rectangle
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height]) # image will always be 32 pixels long and wide 
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y