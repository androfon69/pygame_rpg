import pygame
from global_vars import *

class Player(pygame.sprite.Sprite):
    # pos == topleft position of player
    # group == sprite group to which the player belongs to
    # obstacle_sprites == sprite that the player could collide with
    def __init__(self, pos, group, obstacle_sprites):
        super().__init__(group)
        
        # display vars
        self.image = pygame.image.load('resources/graphics/Player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = pos)
        
        # movement vars
        self.hitbox = self.rect.inflate(-10, -26)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
        # sprites to check collisons on
        self.obstacle_sprites = obstacle_sprites
    
    # changes player direction according to the key pressed
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
        # normalize direction vector for constant speed
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.detect_collision('horizontal')
        
        self.hitbox.y += self.direction.y * speed
        self.detect_collision('vertical')
        
        self.rect.center = self.hitbox.center
        
        
    def detect_collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        # moving right -> adjust left
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        # momving left -> adjust right
                        self.hitbox.left = sprite.hitbox.right
                        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        # moving down -> adjust up
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        # momving up -> adjust down
                        self.hitbox.top = sprite.hitbox.bottom
        
    # player event loop
    def update(self):
        self.input()
        self.move(self.speed)