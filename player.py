import pygame
from global_vars import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        
        # display vars
        self.image = pygame.image.load('resources/graphics/Player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center = pos)
        
        # movement vars
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
            
        
    def input(self):
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_UP]:
            self.direction.y = -1        
        elif keys_pressed[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0        
                
        if keys_pressed[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys_pressed[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
    def move(self, time_diff, speed):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        self.pos.x += self.direction.x * speed * time_diff
        self.rect.centerx = self.pos.x
        
        self.pos.y += self.direction.y * speed * time_diff
        self.rect.centery = self.pos.y
        
    def update(self, time_diff):
        self.input()
        self.move(time_diff, 300)