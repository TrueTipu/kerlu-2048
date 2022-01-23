import pygame, sys
import ctypes

from defs import *
from grid import Grid

#pääosin pelin asetusten ja UI:n hallinnointia, sisältää peli logiikan häviö ja voitto screenille(koska UI) muttei paljon muuta
def run_game(): 
    
    #päätin että heitän metodit tähän ylimmäksi, näyttää erikoisen tyhmältä kuin tässä on vain yksi mutta näillä mennään

    def display_text(text: str, font: pygame.font.Font, pos, color): #tekstien piirtämistä helpoittava metodi
        lines = text.splitlines() #jakaa multiline tekstin riveihin
        for i, l in enumerate(lines):
            text_surf = font.render(l, True, color) #renderoi tekstit
            text_rect = text_surf.get_rect(center = pos) #luo niille rectanglet joila keskitys helpompaa
            SCREEN.blit(text_surf, (text_rect.x, text_rect.y +FONT_SIZE_1*i)) #hallitsee rivinvaihdon koon

    pygame.init() #käynnistää pygamen
    ctypes.windll.user32.SetProcessDPIAware() #fixaa resoluution windows laitteilla

    #perus pygame setuppaus juttuja
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 by Samuli")

    clock = pygame.time.Clock()

    #luodaan gridit eli ruudukot joka halinnoi kaiken gameplay logiikan
    #ruudukkojen sijainnit muistiin HUOM 1d lista!!!
    grid_poses = [(GRID_CAP, GRID_TOP_OFFSET + GRID_CAP), (GRID_CAP + (GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP), (GRID_CAP + 2*(GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP), (GRID_CAP + 3*(GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP),
                 (GRID_CAP, GRID_TOP_OFFSET + GRID_CAP * 2 + GRID_SIZE), (GRID_CAP + (GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP * 2 + GRID_SIZE), (GRID_CAP + 2*(GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP * 2 + GRID_SIZE), (GRID_CAP + 3*(GRID_SIZE + GRID_CAP), GRID_TOP_OFFSET + GRID_CAP * 2 + GRID_SIZE)]

    grid_sprites = pygame.sprite.Group() #lista grideille
    grids_lost = []

    for pos in grid_poses:
        grid_sprites.add(Grid(pos[0], pos[1]))



    #luodaan teksti fontteja joiden käyttö on tosi epäloogista ja ympäri koodia mutten nyt ala siistimäänkään
    text_font = pygame.font.SysFont("arial", FONT_SIZE_2)
    go_text_font = pygame.font.SysFont("calibri Black", FONT_SIZE_1)
    #haetaan kuvat häviö ja voitto stateen kansiosta (ainoa artti pelissä)
    game_over_bc = pygame.image.load(BC_RED_ART)

    #ai stufd begins
    gen = 0 #generaatio mis mennään

    #pistetään peli käyntiin
    running = True

    while running:
        #pistää max framerateksi 60, toivottavasti ei mene myöskään sitä alemmaksi
        #toisinsanoen tämä while loop mikä hallitsee muita pelin asioita, tapahtuu vain 60 kertaa sekunnissa, eikä sitä normaalia 100-1000 mitä se ehkä voisi pyörittää
        delta_time = clock.tick(FPS) 
        fps = 1000 / delta_time

        #pygame eventtejen hallinta
        for event in pygame.event.get():
            #sammuttaa pelin sulkiessa
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            
            #game_over ja game_won statesta poispääsy inputtien avulla, helpompi tehdä täällä kuin gridissä
            # if grid.game_over_state and event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_r:
            #         grid.reset()
        
        #värjää taustan 
        SCREEN.fill("#FFDFAA")
        #piirtää ja kutsuu ruudukon päivitystoimintoa
        grid_sprites.draw(SCREEN)
        grid_sprites.update(SCREEN)

        #piirtää scoren ja highscoren

        for grid in grid_sprites.sprites(): 
            grid: Grid
            display_text(str(grid.get_score()), text_font, (grid.rect.x +10, grid.rect.y+10), (0,0,0))
            if grid.game_over_state and not grid in grids_lost:
                grids_lost.append(grid)

        for grid in grids_lost:
            grid: Grid
            SCREEN.blit(game_over_bc, (grid.rect.x,grid.rect.y)) #gameover kuva
        if len(grids_lost) == 8:
            for grid in grids_lost: grid.reset()
            gen += 1
            grids_lost.clear()



        #piirtää otsikot niille
        display_text('FPS: ' + str(round(fps,1)), go_text_font, (WIDTH //2, 25), (0,0,0))
        display_text('GEN:' + str(gen), go_text_font, (TEXT_OFFSET, 50), (0,0,0))
        display_text('HIGHSCORE:', go_text_font, (WIDTH - TEXT_OFFSET, 50), (0,0,0))



        pygame.display.update() #päivitetään ikkuna johon muutokset on tehty

if __name__ ==  "__main__": #tarkistetaan namespace koska kaikki aina netissä käskee :D
    run_game()
