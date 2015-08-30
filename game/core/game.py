# A Game's responsible for starting graphics module, creating and
# saving the world, and updating the display.

import pygame, sys
from core import graphics
from core import world
from pygame.locals import *

TILE_SIZE = 20
FPS = 20

# A Game's a single instance of a game, which contains world (including maps,
# entities, items, and everything else).
class Game(object):
    def __init__(self, scr_width, scr_height):
        self.width = scr_width
        self.height = scr_height
        self.map_width = scr_width // TILE_SIZE
        self.map_height = scr_height // TILE_SIZE
        self.screen = graphics.start(self.width, self.height)
        self.world = world.World(self.map_width, self.map_height)
        self.clock = pygame.time.Clock()

    # Runs an interactive session of a game with the player, until
    # the player stops playing. We draw the world, then we pass
    # input to the world.
    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)
            self.screen.fill(self.world.map.bg_color)
            self.world.draw()
            pygame.display.update()
            running = self.world.handle_keys(pygame.event.get())
