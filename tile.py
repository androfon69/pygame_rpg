import pygame
from global_vars import *

class Tile(pygame.sprite.Sprite):
    # pos == topleft position of tile
    # group == sprite group to which to tile belongs to
    def __init__(self, pos, group, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(group)
        self.sprite_type = sprite_type
        self.image = surface
        
        # objects are twice as tall so they should be placed 1 TILESIZE lower
        if self.sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        
        # shorten hitbox a bit
        self.hitbox = self.rect.inflate(0, -10)