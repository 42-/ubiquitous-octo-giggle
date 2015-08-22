#!/usr/bin/python3

from core import game

def main():
    scr_width = int(input('SCREEN_WIDTH: '))
    scr_height = int(input('SCREEN_HEIGHT: '))
    
    new_game = game.Game(scr_width, scr_height)
    new_game.run()
    
    print('Thanks for playing! ;)')
    
if __name__ == "__main__":
    main()
