import pygame
import sys

# global vars
screen_width = 1080
screen_height = 720

class Game:
    def __init__(self):
        pygame.init();
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Ne hotaram la final cum se numeste')
        self.clock = pygame.time.Clock()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            time_diff = self.clock.tick() / 1000
            pygame.display.update()
            
if __name__ == '__main__':
    game = Game()
    game.run()