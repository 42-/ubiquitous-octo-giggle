import pygame, sys
from core import graphics
from core import world
from pygame.locals import *

TILE_SIZE = 20
FPS = 20

class Game(object):
    def __init__(self, scr_width, scr_height):
        self.width = scr_width
        self.map_width = scr_width // TILE_SIZE
        self.height = scr_height
        self.map_height = scr_height // TILE_SIZE
        self.screen = graphics.start(self.width, self.height)
        self.ground = graphics.render_text('.', graphics.get_color('dark_ground'))
        self.wall = graphics.render_text('#', graphics.get_color('dark_wall'))
        self.bg_color = graphics.get_color('bg')
        self.world = world.World(self.map_width, self.map_height)
        self.clock = pygame.time.Clock()
    
    def run(self):
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            self.screen.fill(self.bg_color)
            
            for y in range(self.map_height):
                for x in range(self.map_width):
                    wall = self.world.map[x][y].block_sight
                    if wall:
                        graphics.draw_text(self.wall, (x * TILE_SIZE, y * TILE_SIZE))
                    else:
                        graphics.draw_text(self.ground, (x * TILE_SIZE, y * TILE_SIZE))
            
            self.world.draw_objects()
            pygame.display.update()
            running = self.world.handle_keys(pygame.event.get())
