import pygame, sys
import ctypes

from pygame import sprite

from defs import *
from grid import Grid
from tile import Tile

def run_game():
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware() #fixaa resoluution

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")

    clock = pygame.time.Clock()

    grid = Grid()
    grid_sprite = pygame.sprite.GroupSingle(grid)


    text_font = pygame.font.SysFont("comic sans", FONT_SIZE)

    running = True
    while running:
        delta_time = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
        
        SCREEN.fill("#FFDFAA")
        grid_sprite.draw(SCREEN)
        grid_sprite.update(SCREEN, text_font)

        pygame.display.update()

if __name__ ==  "__main__":
    run_game()
