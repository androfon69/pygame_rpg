import pygame
from player import Player
from tile import Tile
from global_vars import *

class Render:
    def __init__(self):
        self.base_surface = pygame.display.get_surface()
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        
        self.create_map()
         
    def create_map(self):
        for i, row in enumerate(MAP):
            for j, col in enumerate(row):
                x_offset = j * TILESIZE
                y_offset = i * TILESIZE
                if col == 'x':
                    Tile((x_offset, y_offset), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x_offset, y_offset), [self.visible_sprites], self.obstacle_sprites)
                
    def run(self):
        self.visible_sprites.draw(self.base_surface)
        self.visible_sprites.update()