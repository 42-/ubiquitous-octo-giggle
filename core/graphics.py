import pygame, sys
from pygame.locals import *

screen = None
font = None

# Initiates pygame (also font), starts up and returns screen
def start(scr_width, scr_height):
    global screen
    global font
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
    screen.blit(text, position)

# Returns color in (R, G, B) format by its name
def get_color(name):
    colors = {
        'bg': (5, 26, 56),
        'player': (126, 167, 137),
        'npc': (175, 131, 159),
        'dark_wall': (76, 102, 140),
        'dark_ground': (45, 72, 111)
    }
    
    return colors[name]
