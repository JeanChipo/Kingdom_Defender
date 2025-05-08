import pygame
from libs.transitions import ScreenFader
from libs.ui import MainMenu, Button, menu_but
from libs.turrets import Turret_Gestion
from libs.models import *
from libs.enemy import update_enemy, create_wave, draw_enemy
from libs.fleche import *
from libs.music import *
from libs.display import *
from libs.steve import *

pygame.init()
WIDTH, HEIGHT = 800,600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Kingdom defender ⊹ ࣪ ﹏𓊝﹏𓂁﹏⊹ ࣪ ˖")

POLICE = pygame.font.Font(None, 24)
CLOCK = pygame.time.Clock()

NB_FPS = 60
RATIO_W, RATIO_H = 1, 1

turrets = Turret_Gestion()
B_upg_tower = Button("white", "black", "gray", "black", "upgrade tower", "kristenitc", 16, 
                 (132.5, 40), (647.5, 112.5), SCREEN.get_size(), lambda : [turrets.add_turret(), upgrade_tower()], SCREEN)

B_upg_turret = Button("white", "black", "gray", "black", "upgrade turret", "kristenitc", 16,
                 (132.5, 40), (647.5, 162.5), SCREEN.get_size(), lambda:turrets.upgrade_turrets("special"), SCREEN)

BUTTON_LIST = [B_upg_tower, B_upg_turret]

Ensemble_fleche =  []
Upgrade_arc = {"cadence" : 0, "dispersion" : [45], "salve" : 1}
upgrade = 1000
wave_number = 1
enemies, all_sprites = create_wave(wave_number,SCREEN.get_width(),420)
gold = 9999999999   # Argent de début
fader = ScreenFader(SCREEN, color=(0,0,0), duration=2000, steps=60)
main_menu = MainMenu(SCREEN, fader)

# buttons to upgrade the tower and turret
B_upg_tower = Button("white", "black", "gray", "black", "upgrade tower", "kristenitc", 16, 
                 (132.5, 40), (647.5, 112.5 + 0*50), SCREEN.get_size(), lambda : [turrets.add_turret(), upgrade_tower()], SCREEN)
B_upg_turret = Button("white", "black", "gray", "black", "upgrade turret", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 1*50), SCREEN.get_size(), turrets.upgrade_turrets, SCREEN)

def update_gold_bow(upg_function: callable):
    global gold, Upgrade_arc
    gold, Upgrade_arc = upg_function(gold, Upgrade_arc)

# buttons to upgrade the archer
B_upg_cadence = Button("white", "black", "gray", "black", "bow - fire rate", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 2*50 + 10), SCREEN.get_size(), lambda : update_gold_bow(upgrade_cadence), SCREEN)
B_upg_salve = Button("white", "black", "gray", "black", "bow - salvo", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 3*50 + 10), SCREEN.get_size(), lambda : update_gold_bow(upgrade_salve), SCREEN)
B_upg_dispersion = Button("white", "black", "gray", "black", "bow - dispersion", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 4*50 + 10), SCREEN.get_size(), lambda : update_gold_bow(upgrade_dispersion), SCREEN)

BUTTON_LIST = [B_upg_tower, B_upg_turret, B_upg_cadence, B_upg_salve, B_upg_dispersion]

B_steve = Button("white", "black", "gray", "black", "steve", "kristenitc", 16, 
                 (100, 100), (0, 0), SCREEN.get_size(), 
                 lambda: press_steve(main_menu), SCREEN)

main_menu.buttons.append(B_steve)

# pygame.key.set_repeat(100) # a held key will be counted every 100 milliseconds

PAUSE = False       # Pause works by stop calling update functions but still calling draw functions
RUNNING = True
while RUNNING:
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if main_menu.game_state == "menu":
                for but in main_menu.buttons:
                    but.handle_click(pygame.mouse.get_pos())
            elif main_menu.game_state == "running":
                mouse_pos = pygame.mouse.get_pos()
                hovering = False
                for but in BUTTON_LIST:
                    if but.is_hovered(mouse_pos):
                        but.handle_click(mouse_pos)
                        hovering = True
                        break
                if not hovering:
                    cadence(Ensemble_fleche, Upgrade_arc, mouse_pos, time, WIDTH, HEIGHT, SCREEN, Upgrade_arc)
                    turrets.select_turret(pygame.mouse.get_pos())

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = SCREEN.get_size()
            RATIO_W = WIDTH / 800
            RATIO_H = HEIGHT / 600
            for but in BUTTON_LIST:
                but.update_pos((WIDTH, HEIGHT))
            turrets.update_positions(WIDTH, HEIGHT)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                PAUSE = not PAUSE
                pygame.mixer.music.pause()
            if event.key == pygame.K_0:
                    play_next_music()
            if event.key == pygame.K_1:
                turrets.change_priorities("petit")
            if event.key == pygame.K_2:
                turrets.change_priorities("volant")
            if event.key == pygame.K_3:
                turrets.change_priorities("moyen")
            if event.key == pygame.K_4:
                turrets.change_priorities("grand")
            #Boutons d'amélioration de compétences de l'arc (modification du comportement des fléches)
            if event.key == pygame.K_a and Upgrade_arc["cadence"] <=3 and gold >= 100 +Upgrade_arc["cadence"]*100: # Permet d'avoir une préogressioon linéaire du coût des améliorations
                Upgrade_arc["cadence"] += 0.5
                gold -= 100 + Upgrade_arc["cadence"] * 100
                print(Upgrade_arc["cadence"])
            if event.key == pygame.K_z and Upgrade_arc["salve"] <=3 and gold >= 100 +Upgrade_arc["salve"]*100:
                Upgrade_arc["salve"] += 1
                gold -= 100 + Upgrade_arc["salve"] * 100
            if event.key == pygame.K_e and len(Upgrade_arc["dispersion"]) <= 9 and gold >= 100 + len(
                    Upgrade_arc["dispersion"]) * 100:
                min_angle = min(Upgrade_arc["dispersion"])
                max_angle = max(Upgrade_arc["dispersion"])
                Upgrade_arc["dispersion"].extend([min_angle - 15, max_angle + 15])  # Ajoute deux nouveaux angles
                Upgrade_arc["dispersion"].sort()  # Trie la liste
                gold -= 100 + len(Upgrade_arc["dispersion"]) * 100
                print(Upgrade_arc["dispersion"])

            else :
                print("error pas assez d'argent ou trop de palier monté")
    print(f"<game_state : {main_menu.game_state}>{' '*50}", end="\r")
    # main_menu.game_state = "running"    # A SUPPRIMER QUAND LE MENU PRINCIPAL FONCTIONNE

    match main_menu.game_state:
        case "menu":
            SCREEN.fill((230, 230, 230))
            B_steve.render(pygame.mouse.get_pos(), border_radius=8)
            main_menu.render(pygame.mouse.get_pos(), ratio=(1, 1))
            play_main_menu()

        case "options":
            ...

        case "steve":
            steve_game_loop(SCREEN, main_menu)  # Call the steve_game_loop here

        case "running": 
            SCREEN.fill('white')
            SCREEN.blit(resize_background(background), (0, 0))
            SCREEN.blit(resize_tower_lvl_1(tower_1), (50*width_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()))
            current_time = pygame.time.get_ticks()
            if not enemies:
                print("pause")
            else:
                last_update,frame = animation_running(frame,current_time, last_update, animation_cooldown,run_animation,enemies)


            menu_but(SCREEN, (0,0,0, 128), (640, 100, 147.5, 300), (RATIO_W, RATIO_H))
            for but in BUTTON_LIST:
                but.render(pygame.mouse.get_pos(),border_radius=6)
            turrets.draw(SCREEN, SCREEN.get_width(), SCREEN.get_width(), enemies)
            #draw_enemy(SCREEN, enemies)

            if not PAUSE:
                turrets.update(enemies, SCREEN.get_width(), SCREEN.get_height())
                enemies, all_sprites, wave_number = update_enemy(SCREEN, all_sprites, enemies, wave_number, turrets.turrets[0].get_bullet())
                if not pygame.mixer.music.get_busy():
                    play_next_music()
            else:
                pause_text = pygame.font.Font(None, 48).render("PAUSED", True, "Black")
                SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 10))
            money_text = pygame.font.Font(None, 21).render(f"current gold : {gold}", True, "Black")
            SCREEN.blit(money_text, (WIDTH - (money_text.get_width()+5), 10))
            dead_fleche(enemies, Ensemble_fleche)
            draw(SCREEN, time, Ensemble_fleche)
        
        case "ended":
            pygame.quit()
            exit()

    texte_fps = POLICE.render(f"{int(CLOCK.get_fps())} FPS", True, "Black")
    SCREEN.blit(texte_fps, (10, 10))

    CLOCK.tick(NB_FPS)
    DT = CLOCK.get_time() / 1000

    fader.update()
    pygame.display.flip()

pygame.quit()
