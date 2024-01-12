import pygame
import sys
from render import Render
from global_vars import *

class Game:
    def __init__(self):
        pygame.init();
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Ne hotaram la final cum se numeste')
        self.clock = pygame.time.Clock()
        self.render = Render()
        
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('white')
            self.render.run()
            pygame.display.update()
            self.clock.tick(FPS)

            
if __name__ == '__main__':
    game = Game()
    game.run()