import pygame
import random
from core import graphics
from pygame.locals import *

TILE_SIZE = 20

# Single tile of a map. It can block player movements or sight.
class Tile(object):
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        
        if block_sight is None: 
            block_sight = blocked
        
        self.block_sight = block_sight

# Map is a collection of tiles.
class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    # Creates simple map with random obstacles.
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

# Object could be item, entity, or something else. 
# It's represented by a single character, which can be moved.
class Object(object):
    def __init__(self, x, y, symbol, color):
        self.x = x
        self.y = y
        self.char = graphics.render_text(symbol, color)
    
    # Attemps to move Object in certain direction.
    def move(self, dx, dy, world):
        if world.is_free(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
    
    # Draws an Object on a display. Since the display's coordinate system
    # differs from the game's coordinate system, we need to convert the 
    # (x, y) values by multiplying them by TILE_SIZE. 
    def draw(self):
        graphics.draw_text(self.char, (self.x * TILE_SIZE, self.y * TILE_SIZE))

# The World is a tiled game world. It contains all objects and maps.
class World(object):
    def __init__(self, map_width, map_height):
        self.player = Object(map_width//2, map_height//2, '@', graphics.get_color('player'))
        self.npc = Object(map_width//2 - 5, map_height//2, '@', graphics.get_color('npc'))
        self.objects = [self.npc, self.player]
        self.wall = graphics.render_text('#', graphics.get_color('dark_wall'))
        self.ground = graphics.render_text('.', graphics.get_color('dark_ground'))
        self.bg_color = graphics.get_color('bg')
        self.map_width = map_width
        self.map_height = map_height
        self.map = Map(map_width, map_height).make_map()
    
    # Draws all objects
    def draw_objects(self):
        for obj in self.objects:
            obj.draw()
    
    # Draws map
    def draw_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                wall = self.map[x][y].block_sight
                if wall:
                    graphics.draw_text(self.wall, (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    graphics.draw_text(self.ground, (x * TILE_SIZE, y * TILE_SIZE))
    
    # Draws world
    def draw(self):
        self.draw_map()
        self.draw_objects()
    
    # Returns true if the tile is free 
    def is_free(self, x, y):
        return not self.map[x][y].blocked
    
    # Handles input
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
