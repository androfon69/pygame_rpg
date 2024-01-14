import pygame
from os import walk
from global_vars import *
from utils import *

class Player(pygame.sprite.Sprite):
    # pos == topleft position of player
    # group == sprite group to which the player belongs to
    # obstacle_sprites == sprites that the player could collide with
    # create_attack = method that exacutes an attack
    def __init__(self, pos, group, obstacle_sprites, create_attack):
        super().__init__(group)
        
        # display vars
        self.image = pygame.image.load('resources/graphics/Player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = pos)
        
        self.import_player_assets()
        self.status = 'down'
        self.animation_speed = 0.15
        self.frame_index = 0
        
        # movement vars
        self.hitbox = self.rect.inflate(-10, -26)
        self.direction = pygame.math.Vector2()
        self.speed = 10
        
        # combat vars
        self.is_attacking = False
        self.attack_cooldown = 500
        self.attack_time = None
        self.attack = create_attack
        
        # sprites to check collisons on
        self.obstacle_sprites = obstacle_sprites
    
    def import_player_assets(self):
        player_path = 'resources/graphics/player'
        self.animations = {'up' : [], 'down' : [], 'left' : [], 'right' : [],
                'up_idle' : [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : [],
                'up_attack' : [], 'down_attack' : [], 'left_attack' : [], 'right_attack' : []}
        
        for animation in self.animations.keys():
            animation_path = player_path + '/' + animation
            self.animations[animation] = import_surface_folder(animation_path)
        
    # changes player direction according to the key pressed
    def input(self):
        # return if player is attacking
        if self.is_attacking:
            return
        
        keys_pressed = pygame.key.get_pressed()
        
        # get movement input
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'        
        elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0        
                
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
            
        # get attack input
        if keys_pressed[pygame.K_j]:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.attack()
            
        if keys_pressed[pygame.K_k]:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.attack()
    
    def get_player_status(self):
        # idle 
        # check previous status to update idle position
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:    
                self.status = self.status + '_idle'
        
        if self.is_attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status: 
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        elif 'attack' in self.status:
            # once attack is over go idle
            self.status = self.status.replace('_attack', '_idle')
    
    # cooldown actions
    def cooldown(self):
        time = pygame.time.get_ticks()
        
        # attack cooldown timer
        if self.is_attacking and time - self.attack_time >= self.attack_cooldown:
            self.is_attacking = False
    
    # moves the player
    def move(self, speed):
        # normalize direction vector for constant speed
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.detect_collision('horizontal')
        
        self.hitbox.y += self.direction.y * speed
        self.detect_collision('vertical')
        
        self.rect.center = self.hitbox.center
        
    def animate(self):
        # get animation coresponding to status
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        
        # reset animation
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        #self.rect = self.image.get_rect(center = self.hitbox.center)
           
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
        self.cooldown()
        self.get_player_status() 
        self.animate()
        self.move(self.speed)