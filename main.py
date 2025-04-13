try :
    import pygame
    from libs.ui import MainMenu, Button, menu_but
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
turrets = Turret_Gestion()
B_upg_tower = Button("white", "black", "gray", "black", "upgrade tower", "kristenitc", 16, 
                 (120+LONG_BANDEAU, 40), (SCREEN.get_width()-165+LONG_BANDEAU, 100+LONG_BANDEAU), SCREEN.get_size(), lambda: print("tower upgraded"), SCREEN)
B_upg_turret = Button("white", "black", "gray", "black", "upgrade turret", "kristenitc", 16, 
                 (120+LONG_BANDEAU, 40), (SCREEN.get_width()-165+LONG_BANDEAU, 150+LONG_BANDEAU), SCREEN.get_size(), turrets.turrets[0].upgrade, SCREEN)
BUTTON_LIST = [B_upg_tower, B_upg_turret]

RATIO_W = float(WIDTH  / 800)
RATIO_H = float(HEIGHT / 600)

turrets = Turret_Gestion()

main_menu = MainMenu(SCREEN)

wave_number = 1
enemies, all_sprites = create_wave(wave_number,SCREEN.get_width(),420)

# pygame.key.set_repeat(100) # a held key will be counted every 100 milliseconds

PAUSE = False       # Pause works by stop calling update functions but still calling draw functions
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if main_menu.game_state == "menu":
                for but in main_menu.buttons:
                    but.handle_click(pygame.mouse.get_pos())
            elif main_menu.game_state == "running":
                for but in BUTTON_LIST:
                    but.handle_click(pygame.mouse.get_pos())

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = SCREEN.get_size()
            RATIO_W = float(WIDTH  / 800)
            RATIO_H = float(HEIGHT / 600)
            for but in BUTTON_LIST:
                but.update_pos((WIDTH, HEIGHT))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                PAUSE = not PAUSE
            if event.key == pygame.K_a:
                NB_FPS /= 2
            if event.key == pygame.K_q:
                NB_FPS *= 2

    SCREEN.fill("white")
    print(f"<game_state : {main_menu.game_state}>{' '*50}", end="\r")
    main_menu.game_state = "running"
    match main_menu.game_state:
        case "menu":
            SCREEN.fill((230,230,230))
            main_menu.ratio = (RATIO_W, RATIO_H)
            main_menu.render(pygame.mouse.get_pos())

        case "running":
            SCREEN.fill('white')
            SCREEN.blit(background, (0, 0))
            SCREEN.blit(tower_1, (-150, 150))

            menu_but(SCREEN, (0,0,0, 128), (SCREEN.get_width() - 160, 100, 160 - 12.5, 300), (1,1))
            for but in BUTTON_LIST:
                but.render(pygame.mouse.get_pos(),border_radius=6)
            turrets.draw(SCREEN, SCREEN.get_width(), SCREEN.get_width(), enemies)
            draw_enemy(SCREEN, enemies)

            if not PAUSE:
                turrets.update(enemies)
                enemies, all_sprites, wave_number = update_enemy(
                    SCREEN, all_sprites, enemies, wave_number, turrets.turrets[0].get_bullet()
                )
            else:
                pause_text = pygame.font.Font(None, 48).render("PAUSED", True, "Black")
                SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 10))

    texte_fps = POLICE.render(f"{int(CLOCK.get_fps())} FPS", True, "Black")
    SCREEN.blit(texte_fps, (10, 10))

    CLOCK.tick(NB_FPS)
    DT = CLOCK.get_time() / 1000

    pygame.display.flip()

pygame.quit()
