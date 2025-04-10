try :
    import pygame
    from libs.button import Button, menu
    from libs.turrets import Turret_Gestion
    from libs.models import *
    from libs.enemy import update_enemy, create_wave, draw_enemy
except ImportError:
    print("Erreur lors de l'importation des modules.")
    exit()

pygame.init()
WIDTH, HEIGHT = 800,600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Kingdom defender ⊹ ࣪ ﹏𓊝﹏𓂁﹏⊹ ࣪ ˖")

# Affichage du texte pour les FPS
POLICE = pygame.font.Font(None, 24)
CLOCK = pygame.time.Clock()

NB_FPS = 60

LONG_BANDEAU = 12.5
# menu_surface = pygame.Surface((WIDTH, HEIGHT))
B_upg_tower = Button((230,230,230), (175, 175, 175), (150, 150, 150), (0, 0, 0), "upgrade tower", "kristenitc", 16, 
                 (100+LONG_BANDEAU, 40), (SCREEN.get_width()-150+LONG_BANDEAU, 100+LONG_BANDEAU), SCREEN.get_size(), lambda: print("x"), SCREEN)
B_upg_turret = Button((230,230,230), (175, 175, 175), (150, 150, 150), (0, 0, 0), "upgrade turret", "kristenitc", 16, 
                 (100+LONG_BANDEAU, 40), (SCREEN.get_width()-150+LONG_BANDEAU, 150+LONG_BANDEAU), SCREEN.get_size(), lambda: print("x"), SCREEN)
BUTTON_LIST = [B_upg_tower, B_upg_turret]

RATIO_W = float(WIDTH  / 800)
RATIO_H = float(HEIGHT / 600)

turrets = Turret_Gestion()

wave_number = 1
enemies, all_sprites = create_wave(wave_number)

# pygame.key.set_repeat(100) # a held key will be counted every 100 milliseconds

PAUSE = False   # Pause works by stop calling update() but still calling draw() functions
RUNNING = True
while RUNNING:
    SCREEN.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for but in BUTTON_LIST:
                but.handle_click(pygame.mouse.get_pos())
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = SCREEN.get_size()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                PAUSE = not PAUSE
            if event.key == pygame.K_a:
                NB_FPS /= 2
            if event.key == pygame.K_q:
                NB_FPS *= 2

    SCREEN.blit(background, (0, 0))
    SCREEN.blit(tower, (-150, 150))

    menu(SCREEN, (240, 240, 240), (SCREEN.get_width() - 150, 100, 150 - 12.5, 300), (RATIO_W, RATIO_W))
    for but in BUTTON_LIST:
        but.render(pygame.mouse.get_pos())
    turrets.draw(SCREEN, WIDTH)
    draw_enemy(SCREEN, enemies)

    if not PAUSE:
        turrets.update()
        enemies, all_sprites, wave_number = update_enemy(
            all_sprites, enemies, wave_number, turrets.turrets[0].get_bullet()
        )
    else:
        pause_text = pygame.font.Font(None, 48).render("PAUSED", True, "Black")
        SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 10))

    texte_fps = POLICE.render(f"{int(CLOCK.get_fps())} FPS", True, "Black")
    SCREEN.blit(texte_fps, (10, 10))

    CLOCK.tick(NB_FPS)
    DT = NB_FPS / 10

    pygame.display.flip()


pygame.quit()
