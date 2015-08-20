import pygame, sys
from pygame.locals import *

class Game():
    def __init__(self):
        self.font = pygame.font.SysFont('Droid Sans Mono', 16)
        self.player_char = '@'
        self.player = self.font.render(self.player_char, True, (0, 100, 200))
        self.player_position = (0, 0)
        self.ground = self.font.render('.', True, (50, 150, 50))
        self.bg_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def handle_keys(self, events):
        for event in events:
            if not hasattr(event, 'key'): continue
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_w:
                    self.player_move('up')
                if event.key == K_e:
                    self.player_move('right-up')
                if event.key == K_d:
                    self.player_move('right')
                if event.key == K_c:
                    self.player_move('right-down')
                if event.key == K_x:
                    self.player_move('down')
                if event.key == K_z:
                    self.player_move('left-down')
                if event.key == K_a:
                    self.player_move('left')
                if event.key == K_q:
                    self.player_move('left-up')
                if event.key == K_s:
                    self.player_move('start')
        return True
    
    def player_move(self, direction):
        x, y = self.player_position
        
        if direction == 'up':
            self.player_position = (x, y - 20)
        elif direction == 'right-up':
            self.player_position = (x + 20, y - 20)
        elif direction == 'right':
            self.player_position = (x + 20, y)
        elif direction == 'right-down':
            self.player_position = (x + 20, y + 20)
        elif direction == 'down':
            self.player_position = (x, y + 20)
        elif direction == 'left-down':
            self.player_position = (x - 20, y + 20)
        elif direction == 'left':
            self.player_position = (x - 20, y)
        elif direction == 'left-up':
            self.player_position = (x - 20, y - 20)
        elif direction == 'start':
            self.player_position = (0, 0)
    
    def run(self):        
        running = True
        
        while running:
            self.screen.fill(self.bg_color)
            
            for i in range(0, SCREEN_HEIGHT, 20):
                for j in range(0, SCREEN_WIDTH, 20):
                    if (j, i) != self.player_position:
                        self.screen.blit(self.ground, (j, i))
            
            self.screen.blit(self.player, self.player_position)
            pygame.display.flip()
            
            running = self.handle_keys(pygame.event.get())
    
def main():
    pygame.init()
    pygame.display.set_caption('Waterfall')
    
    global SCREEN_WIDTH
    SCREEN_WIDTH = int(input('SCREEN_WIDTH: '))
    global SCREEN_HEIGHT
    SCREEN_HEIGHT = int(input('SCREEN_HEIGHT: '))
    
    game = Game()
    game.run()
    
    print("\n\nThanks for playing! ;)")
    
if __name__ == "__main__":
    main()
