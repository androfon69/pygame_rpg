import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        # get direction status
        weapon_status = player.status.split('_')[0]
        
        # render
        self.image = pygame.image.load('resources/graphics/weapons/sword/' + weapon_status + '.png')
        
        # placement
        if weapon_status == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-12, 0))
        elif weapon_status == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-20, 0))
        elif weapon_status == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))
        else:
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))