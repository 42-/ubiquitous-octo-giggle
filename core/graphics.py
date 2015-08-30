import pygame, sys
from pygame.locals import *

TILE_SIZE = 20
screen = None
font = None

# Initiates pygame (also font), starts up and returns screen
def start(scr_width, scr_height):
    global screen
    global font
    global space
    if not screen:
        pygame.init()
        pygame.display.set_caption('Ubiquitous Octo Giggle')
        font_path = "./core/fonts/Droid_Sans_Mono/DroidSansMono.ttf"
        font_size = 16
        font = pygame.font.Font(font_path, font_size)
        screen = pygame.display.set_mode((scr_width, scr_height))

        return screen

# Renders and returns colored text
def render_text(text, color):
    global font
    rend_text = font.render(text, True, color)
    return rend_text

# Draws text at the given position
def draw_text(text, position):
    global screen
    screen.blit(text, transform_to_screen(position))

# Transforms real screen coordinates to game map coordinates (in tiles)
def transform_to_game(position):
    if isinstance(position, int):
        return position // TILE_SIZE
    else:
        return tuple([x // TILE_SIZE for x in position])

# Transforms game map coordinates to screen coordinates (approximately)
def transform_to_screen(position):
    if isinstance(position, int):
        return TILE_SIZE * position
    else:
        return tuple([TILE_SIZE * x for x in position])

# Generates one tile of a background, so there's no need to generate it
# every time to erase text
def get_space(color):
    background = pygame.Surface((TILE_SIZE, TILE_SIZE))
    background.fill(color)
    return background

# Returns color in (R, G, B) format by given name
def get_color(name):
    colors = {
        'bg_deep_ocean': (5, 26, 56),
        'player': (150, 200, 160),
        'npc': (175, 131, 159),
        'wall': (76, 102, 140),
        'ground': (45, 72, 111)
    }

    return colors[name]

# Returns all tiles or certain tile (represented by symbol) by given name
def get_tiles(name):
    tiles = {
        'wall': '#',
        'ground': '.'
    }

    if name == 'all':
        return tiles
    else:
        return tiles[name]
