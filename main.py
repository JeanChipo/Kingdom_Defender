import pygame
from libs.transitions import ScreenFader
from libs.ui import MainMenu, Button, menu_but, TimedTextManager
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
tower_level=1

def upgrade_tower():
    global tower_level
    if tower_level<3:
        tower_level+=1
    print(tower_level)

def gain_gold(amount):
    global gold
    gold += amount

POLICE = pygame.font.Font(None, 24)
CLOCK = pygame.time.Clock()

NB_FPS = 60
RATIO_W, RATIO_H = 1, 1

turrets = Turret_Gestion(gain_gold)

Ensemble_fleche =  []
Upgrade_arc = {"cadence" : 0, "dispersion" : [45], "salve" : 1}
upgrade = 1000
wave_number = 1
enemies, all_sprites = create_wave(wave_number,SCREEN.get_width(),420)
gold = 0    # Argent de début
fader = ScreenFader(SCREEN, color=(0,0,0), duration=2000, steps=60)
main_menu = MainMenu(SCREEN, fader)
hp_tower = 10000000000 # vie de la tour
TextManager = TimedTextManager(SCREEN, 25)

# buttons to upgrade the tower and turret
B_upg_tower = Button("white", "black", "gray", "black", "upgrade tower", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 0*50), SCREEN.get_size(), lambda : [turrets.add_turret(), upgrade_tower()], SCREEN)
B_upg_turret = Button("white", "black", "gray", "black", f"turret - speed", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 1*50), SCREEN.get_size(), lambda: turrets.upgrade_turrets("speed", gold, TextManager), SCREEN)
B_upg_turret1 = Button("white", "black", "gray", "black", f"turret - bullet", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 2*50), SCREEN.get_size(), lambda: turrets.upgrade_turrets("bullet", gold, TextManager), SCREEN)
B_upg_turret2 = Button("white", "black", "gray", "black", f"turret - special", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 3*50), SCREEN.get_size(), lambda: turrets.upgrade_turrets("special", gold, TextManager), SCREEN)

def update_gold_bow(upg_function: callable):
    global gold, Upgrade_arc, TextManager
    gold, Upgrade_arc = upg_function(gold, Upgrade_arc, TextManager)

# buttons to upgrade the archer
B_upg_cadence = Button("white", "black", "gray", "black", "bow - fire rate", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 4*50 + 10), SCREEN.get_size(), lambda : update_gold_bow(upgrade_cadence), SCREEN)
B_upg_salve = Button("white", "black", "gray", "black", "bow - salvo", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 5*50 + 10), SCREEN.get_size(), lambda : update_gold_bow(upgrade_salve), SCREEN)
B_upg_dispersion = Button("white", "black", "gray", "black", "bow - dispersion", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 6*50 + 10), SCREEN.get_size(), lambda : update_gold_bow(upgrade_dispersion), SCREEN)

B_steve = Button("white", "black", "gray", "black", "steve", "kristenitc", 16,
                 (100, 100), (0, 0), SCREEN.get_size(),
                 lambda: press_steve(main_menu), SCREEN)

BUTTON_LIST = [B_upg_tower, B_upg_turret, B_upg_turret1, B_upg_turret2, B_upg_cadence, B_upg_salve, B_upg_dispersion]

def upg_turret_text():
    return turrets.selected_turret.name if turrets.selected_turret else '[No turret selected]'
def upg_turret_price(upg_name:str):
    if upg_name not in ["bullet", "special", "speed"]: return 0
    return turrets.get_next_price(upg_name) if turrets.get_next_price(upg_name) != 0 else '...'

main_menu.buttons.append(B_steve)

shuffle_playlist()

PAUSE = False       # Pause works by stop calling update functions but still calling draw functions
RUNNING = True

LAST_TEXT_UPDATE_TIME = 0
money_text = wave_text = tower_text = upgrade_cadence_text = upgrade_bullet_text = upgrade_special_text = upgrade_arrow_cadence_text = upgrade_arrow_dispersion_text = upgrade_arrow_salve_text = None

while RUNNING:
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
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
                    turrets.select_turret(pygame.mouse.get_pos(),TextManager)

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = SCREEN.get_size()
            RATIO_W = WIDTH / 800
            RATIO_H = HEIGHT / 600
            for but in BUTTON_LIST:
                but.update_pos((WIDTH, HEIGHT))
            turrets.update_positions(WIDTH, HEIGHT)
            fader.update_overlay_size()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                PAUSE = not PAUSE
                if PAUSE:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_0:
                    play_next_music()
            elif event.key == pygame.K_1:
                turrets.change_priorities("petit")
            elif event.key == pygame.K_2:
                turrets.change_priorities("volant")
            elif event.key == pygame.K_3:
                turrets.change_priorities("moyen")
            elif event.key == pygame.K_4:
                turrets.change_priorities("grand")

    main_menu.game_state = "running"    # A SUPPRIMER APRES DEBUGUAGE

    match main_menu.game_state:
        case "menu":
            SCREEN.fill((230, 230, 230))
            B_steve.render(pygame.mouse.get_pos(), border_radius=8)
            main_menu.render(pygame.mouse.get_pos(), ratio=(1, 1))
            play_main_menu(["./assets/musics/TheInfiniteHole.mp3", "./assets/musics/ChansonDAutomne.mp3"])

        case "options":
            option_game_loop(SCREEN, main_menu)

        case "steve":
            steve_game_loop(SCREEN, main_menu)

        case "running": 
            SCREEN.fill('white')
            SCREEN.blit(resize_background(background), (0, 0))
            if tower_level == 1 :
                SCREEN.blit(resize_tower_lvl_1(tower_1), (50*width_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()))

                pygame.draw.circle(screen,0,(50*width_ratio()+55*height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+225*height_ratio()),10)

            elif tower_level == 2:
                SCREEN.blit(resize_tower_lvl_2(tower_2), (50*width_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()))
                pygame.draw.circle(screen,0,(50*width_ratio()+55*height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+225*height_ratio()),10)
                pygame.draw.circle(screen,0,(50*width_ratio()+55*height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+295*height_ratio()),10)

            else :
                SCREEN.blit(resize_tower_lvl_3(tower_3), (50*width_ratio()-3,SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()))
                pygame.draw.circle(screen, 0, (50 * width_ratio() + 55 * height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio() + 225 * height_ratio()), 10)
                pygame.draw.circle(screen, 0, (50 * width_ratio() + 55 * height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio() + 295 * height_ratio()), 10)
                pygame.draw.circle(screen, 0, (50 * width_ratio() + 55 * height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio() + 362 * height_ratio()), 10)

            current_time = pygame.time.get_ticks()
            if not enemies:
                print("pause")
            else:
                last_update,frame = animation_running(frame,current_time, last_update, animation_cooldown,run_animation,enemies)

            menu_but(SCREEN, (0,0,0, 128), (640, 100, 147.5, 375), (RATIO_W, RATIO_H))
            for but in BUTTON_LIST:
                #but.update_colors_based_on_gold(gold, cost=10000)
                but.render(pygame.mouse.get_pos(),border_radius=6)
            turrets.draw(SCREEN, SCREEN.get_width(), SCREEN.get_width(), enemies)
            #draw_enemy(SCREEN, enemies)

            if not PAUSE:
                turrets.update(enemies, SCREEN.get_width(), SCREEN.get_height())
                TextManager.update()
                enemies, all_sprites, wave_number,damage = update_enemy(SCREEN, all_sprites, enemies, wave_number)
                if not pygame.mixer.music.get_busy():
                    play_next_music()
            else:
                pause_text = pygame.font.Font(None, 48).render("PAUSED", True, "Black")
                SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 10))

            if current_time - LAST_TEXT_UPDATE_TIME > 100:  # Update text every 100ms to prevent lagging
                money_text = pygame.font.SysFont("Lucida Sans", 18).render(f"current gold : {gold}", True, "Black")
                wave_text = pygame.font.SysFont("Lucida Sans", 18).render(f"current wave : {wave_number}", True, "Black")
                tower_text = pygame.font.SysFont("Lucida Sans", 18).render(f"life : {hp_tower//100000000}", True, "Black")
                upgrade_cadence_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s speed : {upg_turret_price('speed')} gold", True, "Black")
                upgrade_bullet_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s bullet : {upg_turret_price('bullet')} gold", True, "Black")
                upgrade_special_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s special : {upg_turret_price('special')} gold", True, "Black")
                upgrade_arrow_cadence_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade bow's fire rate {...} : gold", True, "Black")
                upgrade_arrow_dispersion_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade bow's salvo : {...} gold", True, "Black")
                upgrade_arrow_salve_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade bow's dispersion : {...} gold", True, "Black")
                LAST_TEXT_UPDATE_TIME = current_time

            B_upg_turret.update_colors_based_on_gold(gold, turrets.get_next_price("speed"))
            B_upg_turret1.update_colors_based_on_gold(gold, turrets.get_next_price("bullet"))
            B_upg_turret2.update_colors_based_on_gold(gold, turrets.get_next_price("special"))

            SCREEN.blit(money_text, (WIDTH - (money_text.get_width()+5), 5))
            SCREEN.blit(upgrade_cadence_text, (WIDTH - (upgrade_cadence_text.get_width()+5), 25))
            SCREEN.blit(upgrade_bullet_text, (WIDTH - (upgrade_bullet_text.get_width()+5), 45))
            SCREEN.blit(upgrade_special_text, (WIDTH - (upgrade_special_text.get_width()+5), 65))

            SCREEN.blit(upgrade_arrow_cadence_text, (5, 80))
            SCREEN.blit(upgrade_arrow_dispersion_text, (5, 100))
            SCREEN.blit(upgrade_arrow_salve_text, (5, 120))

            SCREEN.blit(wave_text, (5, 25))
            SCREEN.blit(tower_text, (5, 40))
            dead_fleche(enemies, Ensemble_fleche)
            draw(SCREEN, time, Ensemble_fleche)

            hp_tower -= damage
            if hp_tower <= 0:
                main_menu.game_state = "ended"
        
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
