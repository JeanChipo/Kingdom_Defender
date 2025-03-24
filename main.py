import pygame
from libs.button import Button, menu
from libs.Turrets import Turret_Gestion
from libs.models import *

pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Testin\' shit ᓚᘏᗢ')

# Affichage du texte pour les FPS
POLICE = pygame.font.Font(None, 24)
CLOCK = pygame.time.Clock()

NB_FPS = 60

LONG_BANDEAU = 12.5
# menu_surface = pygame.Surface((WIDTH, HEIGHT))
button1 = Button((230,230,230), (175, 175, 175), (150, 150, 150), (0, 0, 0), "im a button", "kristenitc", 16, 
                 (100+LONG_BANDEAU, 40), (SCREEN.get_width()-150+LONG_BANDEAU, 100+LONG_BANDEAU), SCREEN.get_size(), lambda: print("x"), SCREEN)
turrets = Turret_Gestion()

# pygame.key.set_repeat(100) # a held key will be counted every 100 milliseconds

PAUSE = False
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button1.handle_click(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p :
                print("<Paused>")
                if not PAUSE : PAUSE = True
                else : PAUSE = False
            if event.key == pygame.K_a :
                NB_FPS /= 2
            if event.key == pygame.K_q :
                NB_FPS *= 2

    SCREEN.fill('white')
    SCREEN.blit(background, (0,0))
    SCREEN.blit(tower, (-150,150))

    if PAUSE :
        SCREEN.blit(pygame.font.Font(None, 48).render("PAUSED", True, "Black"),   (WIDTH//2 - 6*12, 10)) # 6 is the lenght of "PAUSED", 12 is the width of each character

 
    menu(SCREEN, (240,240,240), (SCREEN.get_width()-150, 100, 150-12.5, 300))
    button1.render(pygame.mouse.get_pos())
    turrets.run(SCREEN, WIDTH)

    texte_fps = POLICE.render(f"{int(CLOCK.get_fps())} FPS", True, "Black")
    SCREEN.blit(texte_fps, (10, 10))
    CLOCK.tick(NB_FPS)

    pygame.display.flip()

pygame.quit()
