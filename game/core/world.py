import pygame
import random
from core import graphics
from pygame.locals import *

# Single tile of a map. It can block player movements or sight.
class Tile(object):
    def __init__(self, blocked, block_sight = None, tile_type = 'wall'):
        self.blocked = blocked
        self.block_sight = blocked if block_sight == None else block_sight
        self.tile_type = tile_type

# A rectangle on the map. Used to characterize a room.
# x, y - upper left corner coordinates; w, h - displacement to the lower right
# corner.
class Rect(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.ax = x + w
        self.ay = y + h

    # Finds the center of a rectangle.
    def center(self):
        center_x = (self.x + self.ax) // 2
        center_y = (self.y + self.ay) // 2
        return (center_x, center_y)

# Map is a collection of tiles.
class Map(object):
    def __init__(self, width, height, theme='default'):
        self.width = width
        self.height = height
        self.theme = theme
        self.bg_color = graphics.get_color('bg_deep_ocean')
        self.rendered = self.render_tiles(self.bg_color)
        self.tiles = self.make_map()

    # Renders all tiles used in a map.
    def render_tiles(self, bg_color):
        tiles = graphics.get_tiles('all')

        rendered = {
            'space': graphics.get_space(bg_color)
        }

        for tile in tiles:
            rendered[tile] = graphics.render_text(tiles[tile],
                                    graphics.get_color(tile))
        return rendered

    # Creates map with random dungeon.
    def make_map(self):
        map = [[ Tile(True)
            for y in range(self.height) ]
                for x in range(self.width) ]

        rooms = []
        num_rooms = 0
        max_rooms = self.height

        for room in range(max_rooms):
            w = random.randint(3, max_rooms // 2)
            h = random.randint(3, max_rooms // 2)

            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)

            new_room = Rect(x, y, w, h)

            overlap = False

            for other_room in rooms:
                if self.intersect(new_room, other_room):
                    overlap = True
                    break

            if not overlap:
                self.create_room(map, new_room)

            (new_x, new_y) = new_room.center()

            if num_rooms > 0:
                (prev_x, prev_y) = rooms[num_rooms - 1].center()
                if random.randint(0, 1) == 1:
                    self.create_h_tunnel(map, prev_x, new_x, prev_y)
                    self.create_v_tunnel(map, prev_y, new_y, new_x)
                else:
                    self.create_v_tunnel(map, prev_y, new_y, new_x)
                    self.create_h_tunnel(map, prev_x, new_x, prev_y)

            rooms.append(new_room)
            num_rooms += 1

        return map

    # Goes through the tiles in rectangle and makes them passable.
    def create_room(self, map, room):
        for x in range(room.x + 1, room.ax):
            for y in range(room.y + 1, room.ay):
                map[x][y].blocked = False
                map[x][y].block_sight = False
                map[x][y].tile_type = 'ground'

    # Creates horizontal tunnel of passable tiles.
    def create_h_tunnel(self, map, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False
            map[x][y].tile_type = 'ground'

    # Creates vertical tunnel of passable tiles.
    def create_v_tunnel(self, map, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False
            map[x][y].tile_type = 'ground'

    # Returns True if two rooms overlap.
    def intersect(self, room_a, room_b):
        return (room_a.x <= room_b.ax and room_a.ax >= room_b.x and
                room_a.y <= room_b.ay and room_a.ay >= room_b.y)

# Object could be item, entity, or something else.
# It's represented by a single character, which can be moved.
class Object(object):
    def __init__(self, x, y, symbol, color):
        self.x = x
        self.y = y
        self.char = graphics.render_text(symbol, color)

    # Attemps to move Object in certain direction.
    def move(self, dx, dy, world, path=0):
        if world.is_free(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    # Draws an Object on a display. Since the display's coordinate system
    # differs from the game's coordinate system, we need to convert the
    # (x, y) values by multiplying them by TILE_SIZE.
    def draw(self, bg):
        graphics.draw_text(bg, (self.x, self.y))
        graphics.draw_text(self.char, (self.x , self.y))

# The World is a tiled game world. It contains all objects and maps.
class World(object):
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.map = Map(map_width, map_height)
        self.player = Object(0, 0, '@', graphics.get_color('player'))
        self.npc = Object(1, 1, '@', graphics.get_color('npc'))
        self.player.x, self.player.y = self.find_free()
        self.npc.x, self.npc.y = self.find_free()
        self.objects = [self.npc, self.player]

    # Draws all objects.
    def draw_objects(self):
        for obj in self.objects:
            obj.draw(self.map.rendered['space'])

    # Draws map.
    def draw_map(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                symbol = self.map.rendered[self.map.tiles[x][y].tile_type]
                graphics.draw_text(symbol, (x, y))

    # Draws world.
    def draw(self):
        self.draw_map()
        self.draw_objects()

    # Returns true if the tile is free.
    def is_free(self, x, y):
        return not self.map.tiles[x][y].blocked

    # Finds random free place.
    def find_free(self):
        while(True):
            rand_x = random.randint(0, self.map_width - 1)
            rand_y = random.randint(0, self.map_height - 1)

            if self.is_free(rand_x, rand_y):
                return (rand_x, rand_y)

    # Handles input.
    def handle_keys(self, events):
        for event in events:
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
