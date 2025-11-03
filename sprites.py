import pygame
from config import *
from game import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

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

        self.image = pygame.Surface([self.width, self.height]) # get an image that can later be drawn to the screen
        self.image.fill(RED) # make the image red

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