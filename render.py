import pygame
from player import Player
from global_vars import *

class Render:
    def __init__(self):
        self.base_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.setup(100, 100)
        
    def setup(self, width, height):
        self.player = Player((width, height), self.sprites)
        
    def run(self, time_diff):
        self.base_surface.fill('black')
        self.sprites.draw(self.base_surface)
        self.sprites.update(time_diff)