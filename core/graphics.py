import pygame, sys
from pygame.locals import *

screen = None
font = None

def start(scr_width, scr_height):
    global screen
    global font
    if not screen:
        pygame.init()
        pygame.display.set_caption('Ubiquitous Octo Giggle')
        font = pygame.font.SysFont('Droid Sans Mono', 16)
        screen = pygame.display.set_mode((scr_width, scr_height))
        
        return screen
    
def render_text(text, color):
    global font
    rend_text = font.render(text, True, color)
    return rend_text
    
def draw_text(text, position):
    global screen
    screen.blit(text, position)
    
def get_color(name):
    colors = {
        'bg': (10, 10, 10),
        'player': (0, 100, 200),
        'npc': (100, 100, 0),
        'dark_wall': (142, 145, 123),
        'dark_ground': (58, 119, 53)
    }
    
    return colors[name]
