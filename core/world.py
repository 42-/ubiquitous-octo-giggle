import pygame
import random
from core import graphics
from pygame.locals import *

TILE_SIZE = 20

class Tile(object):
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        
        if block_sight is None: 
            block_sight = blocked
        
        self.block_sight = block_sight
    
class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def make_map(self):
        map = [[ Tile(False)
            for y in range(self.height) ]
                for x in range(self.width) ]
        
        for y in range(self.height):
            for x in range(self.width):
                if random.randint(0, 100) < 10:
                    map[x][y].blocked = True
                    map[x][y].block_sight = True
        return map
    
class Object(object):
    def __init__(self, x, y, symbol, color):
        self.x = x
        self.y = y
        self.char = graphics.render_text(symbol, color)
    
    def move(self, dx, dy, world):
        if world.is_free(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
    
    def draw(self):
        graphics.draw_text(self.char, (self.x * TILE_SIZE, self.y * TILE_SIZE))
    
    
class World(object):
    def __init__(self, map_width, map_height):
        self.player = Object(map_width//2, map_height//2, '@', graphics.get_color('player'))
        self.npc = Object(map_width//2 - 5, map_height//2, '@', graphics.get_color('npc'))
        self.objects = [self.npc, self.player]
        self.map = Map(map_width, map_height).make_map()
    
    def draw_objects(self):
        for obj in self.objects:
            obj.draw()
    
    def is_free(self, x, y):
        return not self.map[x][y].blocked
    
    def handle_keys(self, events):
        for event in events:
            if not hasattr(event, 'key'):
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_w:
                    self.player.move(0, -1, self)
                if event.key == K_e:
                    self.player.move(1, -1, self)
                if event.key == K_d:
                    self.player.move(1, 0, self)
                if event.key == K_c:
                    self.player.move(1, 1, self)
                if event.key == K_x:
                    self.player.move(0, 1, self)
                if event.key == K_z:
                    self.player.move(-1, 1, self)
                if event.key == K_a:
                    self.player.move(-1, 0, self)
                if event.key == K_q:
                    self.player.move(-1, -1, self)
        return True
