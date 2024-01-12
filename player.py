import pygame
from global_vars import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, obstacle_sprites):
        super().__init__(group)
        
        # display vars
        self.image = pygame.image.load('resources/graphics/Player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center = pos)
        
        # movement vars
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 5
            
        self.obstacle_sprites = obstacle_sprites
        
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
        
    def move(self, speed):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        self.pos.x += self.direction.x * speed
        self.rect.x = self.pos.x
        self.detect_collision('horizontal')
        
        self.pos.y += self.direction.y * speed
        self.rect.y = self.pos.y
        self.detect_collision('vertical')
        
    def detect_collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        # moving right -> adjust left
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        # momving left -> adjust right
                        self.rect.left = sprite.rect.right
                        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        # moving down -> adjust up
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        # momving up -> adjust down
                        self.rect.top = sprite.rect.bottom
        
        
    def update(self):
        self.input()
        self.move(self.speed)
        self.detect_collision('vertical')