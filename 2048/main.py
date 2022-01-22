import pygame, sys
import ctypes

from pygame import sprite

from defs import *
from grid import Grid


def run_game():
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware() #fixaa resoluution

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")

    clock = pygame.time.Clock()

    grid = Grid()
    grid_sprite = pygame.sprite.GroupSingle(grid)

    text_font = pygame.font.SysFont("arial Black", FONT_SIZE_2)

    go_text_font = pygame.font.SysFont("calibri Black", FONT_SIZE_1)
    game_over_bc = pygame.image.load(BC_BLACK_ART)
    game_won_bc = pygame.image.load(BC_YELLOW_ART)

    running = True

    def display_text(text: str, font: pygame.font.Font, pos, color):
        lines = text.splitlines()
        for i, l in enumerate(lines):
            text_surf = font.render(l, True, color)
            text_rect = text_surf.get_rect(center = pos)
            SCREEN.blit(text_surf, (text_rect.x, text_rect.y +FONT_SIZE_1*i))



    while running:
        delta_time = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            if grid.game_over_state and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid.reset()
            if grid.game_won_state and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.continue_game()
        
        SCREEN.fill("#FFDFAA")
        grid_sprite.draw(SCREEN)
        grid_sprite.update(SCREEN)

        display_text(str(grid.get_score()), text_font, (TEXT_OFFSET, 100), (0,0,0))
        display_text(str(grid.get_high_score()), text_font, (WIDTH - TEXT_OFFSET, 100), (0,0,0))

        display_text('SCORE:', go_text_font, (TEXT_OFFSET, 50), (0,0,0))
        display_text('HIGHSCORE:', go_text_font, (WIDTH - TEXT_OFFSET, 50), (0,0,0))


        if grid.game_over_state:
            SCREEN.blit(game_over_bc, (0,0))
            display_text('''GAME OVER \n PRESS "R" TO RETRY''', go_text_font, (WIDTH / 2, HEIGHT / 2), (255, 50,50))
        if grid.game_won_state:
            SCREEN.blit(game_won_bc, (0,0))
            display_text('''YOU WON \n PRESS "SPACE" TO CONTINUE''', go_text_font, (WIDTH / 2, HEIGHT / 2), (50, 255,150))

        pygame.display.update()

if __name__ ==  "__main__":
    run_game()
