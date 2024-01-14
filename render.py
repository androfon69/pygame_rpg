import pygame
from player import Player
from tile import Tile
from weapon import Weapon
from global_vars import *
from utils import *
from random import choice

class Render:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = CameraGroup()
        
        self.create_map()
    
    # render tilemap
    # each tile sits at (j * TILESIZE, i * TILESIZE)
    # this method renders the entire map + player
    def create_map(self):
        # positions of all assets
        layouts = {
            'boundary' : import_csv_layout('resources/graphics/map_csvs/Map_Blocks.csv'),
            'foliage' : import_csv_layout('resources/graphics/map_csvs/Map_Foliage.csv'),
            'objects' : import_csv_layout('resources/graphics/map_csvs/Map_Objects.csv')
        }
        # renders of all assets
        graphics = {
            'foliage' : import_surface_folder('resources/graphics/grass'),
            'objects' : import_surface_folder('resources/graphics/objects')
        }
        
        # render all map objects
        for label, layout in layouts.items():    
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if col != '-1':
                        x_offset = j * TILESIZE
                        y_offset = i * TILESIZE
                        if label == 'boundary': # invisible map boundary
                            Tile((x_offset, y_offset), [self.obstacle_sprites], 'invisible')
                        if label == 'foliage': # visible foliage
                            random_foliage = choice(graphics['foliage']) 
                            Tile((x_offset, y_offset), [self.visible_sprites, self.obstacle_sprites], 'foliage', random_foliage)
                        if label == 'objects': # collidable objects
                            # object files are named {index}.png to more easily get and render them
                            object_surface = graphics['objects'][int(col)]
                            Tile((x_offset, y_offset), [self.visible_sprites, self.obstacle_sprites], 'object', object_surface)
                            
        self.player = Player((1600, 1900), [self.visible_sprites], self.obstacle_sprites, self.create_attack)
                
    def create_attack(self):
        Weapon(self.player, [self.visible_sprites])
    
    def run(self):
        self.visible_sprites.draw_camera_group(self.player)
        self.visible_sprites.update()
        
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # camera should follow the player in the middle of the screen
        self.width = self.display_surface.get_size()[0] // 2
        self.height = self.display_surface.get_size()[1] // 2
    
        # offset for all visible sprites
        self.pos_offset = pygame.math.Vector2()
        
        # game floor
        self.floor_surface = pygame.image.load('resources/graphics/tilemap/Ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0, 0))
        
    def draw_camera_group(self, player):
        # get the offset from the player coordinates - midscreen coordinates
        self.pos_offset.x = player.rect.centerx - self.width
        self.pos_offset.y = player.rect.centery - self.height
        
        # move background
        floor_offset = self.floor_rect.topleft - self.pos_offset
        self.display_surface.blit(self.floor_surface, floor_offset)
        
        # move all sprites with the calculated offset
        # they are rendered top-down so we don't get any weird clippings
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            pos_offset_rect = sprite.rect.topleft - self.pos_offset
            self.display_surface.blit(sprite.image, pos_offset_rect)