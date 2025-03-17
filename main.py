import pygame
from button import But
from Turrets import Turret_Gestion

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Testin\' shit ᓚᘏᗢ')

# Affichage du texte pour les FPS
police = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

NB_FPS = 60

but1 = But((160,25,160), (175, 175, 175), (150, 150, 150), (0, 0, 0), "im a button", None, 24, (140, 40), screen.get_size(), lambda: print("x"), screen)
turrets = Turret_Gestion()

RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            but1.handle_click(pygame.mouse.get_pos())

    screen.fill('white')
    but1.render(pygame.mouse.get_pos())
    turrets.run(screen, WIDTH)

    texte_fps = police.render(f"{int(clock.get_fps())} FPS", True, "Black")
    screen.blit(texte_fps, (10, 10))
    clock.tick(NB_FPS)

    pygame.display.flip()
