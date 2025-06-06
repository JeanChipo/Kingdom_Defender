import pygame
from libs.transitions import ScreenFader
from libs.ui import MainMenu, Button, menu_but, TimedTextManager, pause
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

def upgrade_tower():
    global tower_level, gold
    price = 40000
    if gold < price * tower_level:
        return
    if tower_level<3:
        gain_gold(-(price * tower_level))
        tower_level+=1
        turrets.add_turret()
    print(tower_level)

def upgrade_tower_price():
    global tower_level
    if tower_level == 1:
        return 40000
    elif tower_level == 2:
        return 80000
    return 1


def gain_gold(amount):
    global gold
    gold += amount

POLICE = pygame.font.Font(None, 24)
CLOCK = pygame.time.Clock()

NB_FPS = 60
RATIO_W, RATIO_H = 1, 1

turrets = Turret_Gestion(gain_gold)

Ensemble_fleche =  []
price_upgrade = []
# Upgrade_arc["prices_upgrade"][0] = prix de la cadence ; Upgrade_arc["prices_upgrade"][1] = prix de la salve ; Upgrade_arc["prices_upgrade"][2] = prix de la dispersion
Upgrade_arc = {"cadence" : 0, "salve" : 1, "dispersion" : [0],
               "prices_upgrade" : [5000,5000,6000]}
upgrade = 1000
wave_number = 1
enemies, all_sprites = create_wave(wave_number,SCREEN.get_width(),420)
gold = 0    # Argent de début
fader = ScreenFader(SCREEN, color=(0,0,0), duration=2000, steps=60)
main_menu = MainMenu(SCREEN, fader)
hp_tower = 10000000000 # vie de la tour
TextManager = TimedTextManager(SCREEN, 25)

PAUSE_START_TIME = 0
PAUSE_DURATION = 0 

# buttons to upgrade the tower and turret
B_upg_tower = Button("white", "black", "gray", "black", "upgrade tower", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 0*50), SCREEN.get_size(), lambda : [upgrade_tower()], SCREEN)
B_upg_turret = Button("white", "black", "gray", "black", f"turret - speed", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 1*50), SCREEN.get_size(), lambda: turrets.upgrade_turrets("speed", gold, TextManager), SCREEN)
B_upg_turret1 = Button("white", "black", "gray", "black", "turret - bullet", "kristenitc", 16,
                 (132.5, 40), (647.5, 112.5 + 2*50), SCREEN.get_size(), lambda: turrets.upgrade_turrets("bullet", gold, TextManager), SCREEN)
B_upg_turret2 = Button("white", "black", "gray", "black", "turret - special", "kristenitc", 16,
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

B_steve = Button("orange", (214,139,0), "gray", "black", "<º))))><", "kristenitc", 16,
                 (50, 20), (250, 515), SCREEN.get_size(), lambda: press_steve(main_menu), SCREEN)
main_menu.buttons.append(B_steve)

BUTTON_LIST = [B_upg_tower, B_upg_turret, B_upg_turret1, B_upg_turret2, B_upg_cadence, B_upg_salve, B_upg_dispersion]

def upg_turret_text():
    return turrets.selected_turret.name if turrets.selected_turret else '[No turret selected]'
def upg_turret_price(upg_name:str):
    if upg_name not in ["bullet", "special", "speed"]: return 0
    return turrets.get_next_price(upg_name) if turrets.get_next_price(upg_name) != 0 else '...'


shuffle_playlist()

PAUSE = False       # Pause works by stop calling update functions but still calling draw functions
RUNNING = True

LAST_TEXT_UPDATE_TIME = 0
money_text = wave_text = tower_text = upgrade_cadence_text = upgrade_bullet_text = upgrade_special_text = upgrade_arrow_cadence_text = upgrade_arrow_dispersion_text = upgrade_arrow_salve_text = None

while RUNNING:
    time = pygame.time.get_ticks() - PAUSE_DURATION  # get the correct time by subtracting the duration of the pause
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
                    cadence(tower_level,Ensemble_fleche,RATIO_W, RATIO_H, mouse_pos, time, SCREEN, Upgrade_arc)
                    turrets.select_turret(pygame.mouse.get_pos(),TextManager)

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = SCREEN.get_size()
            RATIO_W = WIDTH / 800
            RATIO_H = HEIGHT / 600
            for but in BUTTON_LIST:
                but.update_pos((WIDTH, HEIGHT))
                B_steve.update_pos((WIDTH, HEIGHT))
            turrets.update_positions(WIDTH, HEIGHT)
            fader.update_overlay_size()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not PAUSE:
                    PAUSE = True
                    PAUSE_START_TIME = pygame.time.get_ticks()
                    pygame.mixer.music.pause()
                    pause_text = pygame.font.Font(None, 48).render("PAUSED", True, "Black")
                    SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 10))
                    pygame.display.flip()
                    pause()
                    PAUSE = False
                    PAUSE_DURATION += pygame.time.get_ticks() - PAUSE_START_TIME
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

    match main_menu.game_state:
        case "menu":
            SCREEN.blit(resize_background(menu_background), (0, 0))
            B_steve.render(pygame.mouse.get_pos())
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
                SCREEN.blit(resize_baliste(new_baliste),(25 * width_ratio() + 28 * height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+75*height_ratio()))

            elif tower_level == 2:
                SCREEN.blit(resize_tower_lvl_2(tower_2), (50*width_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()))
                SCREEN.blit(resize_baliste(new_baliste),(25 * width_ratio() + 28 * height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+75*height_ratio()))

            else :
                SCREEN.blit(resize_tower_lvl_3(tower_3), (50*width_ratio()-3,SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()))
                SCREEN.blit(resize_baliste(new_baliste),(25 * width_ratio() + 28 * height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+75*height_ratio()))

            current_time = pygame.time.get_ticks()
            if enemies:
                last_update,frame = animation_big_monster_running(frame,current_time, last_update, animation_cooldown,enemies)

            menu_but(SCREEN, (0,0,0, 128), (640, 100, 147.5, 375), (RATIO_W, RATIO_H))
            for but in BUTTON_LIST:
                but.render(pygame.mouse.get_pos())
            turrets.draw(SCREEN, SCREEN.get_width(), SCREEN.get_width(), enemies)

            turrets.update(enemies, SCREEN.get_width(), SCREEN.get_height())
            TextManager.update()
            enemies, all_sprites, wave_number,damage = update_enemy(SCREEN, all_sprites, enemies, wave_number)
            if not pygame.mixer.music.get_busy():
                play_next_music()

            if current_time - LAST_TEXT_UPDATE_TIME > 100:  # Update text every 100ms to prevent lagging
                def upg_turret_text():
                    if turrets.selected_turret:
                        return turrets.selected_turret.name
                    else:
                        return '[No turret selected]'
                def upg_turret_price(upg_name:str):
                    if upg_name not in ["bullet", "special", "speed"]:
                        return 0
                    if turrets.get_next_price(upg_name) != 0:
                        return turrets.get_next_price(upg_name)
                    else :
                        return '...'

                money_text = pygame.font.SysFont("Lucida Sans", 18).render(f"current gold : {gold}", True, "Black")
                wave_text = pygame.font.SysFont("Lucida Sans", 18).render(f"current wave : {wave_number}", True, "Black")
                tower_text = pygame.font.SysFont("Lucida Sans", 18).render(f"life : {hp_tower//100000000}", True, "Black")
                upg_tower_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade tower cost : {upgrade_tower_price()}", True, "Black")
                if turrets.selected_turret: 
                    if upg_turret_price('speed') == 1:
                        upgrade_cadence_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s speed : out of stock", True, "Black")
                    else:
                        upgrade_cadence_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s speed : {upg_turret_price('speed')} gold", True, "Black")

                    if upg_turret_price('bullet') == 1:
                        upgrade_bullet_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s bullet : out of stock", True, "Black")
                    else:
                        upgrade_bullet_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s bullet : {upg_turret_price('bullet')} gold", True, "Black")

                    if upg_turret_price('special') == 1:
                        upgrade_special_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s special : out of stock", True, "Black")
                    else:
                        upgrade_special_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade {upg_turret_text()}'s special : {upg_turret_price('special')} gold", True, "Black")
                else: 
                    upgrade_cadence_text = pygame.font.SysFont("Lucida Sans", 18).render('', True, "Black")
                    upgrade_bullet_text = pygame.font.SysFont("Lucida Sans", 18).render('', True, "Black")
                    upgrade_special_text = pygame.font.SysFont("Lucida Sans", 18).render('', True, "Black")                    

                if int(Upgrade_arc['prices_upgrade'][0]) == 1:
                    upgrade_arrow_cadence_text = pygame.font.SysFont("Lucida Sans", 18).render("upgrade bow's fire rate : out of stock", True, "Black")
                else:
                    upgrade_arrow_cadence_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade bow's fire rate : {int(Upgrade_arc['prices_upgrade'][0])} gold", True, "Black")

                if int(Upgrade_arc['prices_upgrade'][1]) == 1:
                    upgrade_arrow_dispersion_text = pygame.font.SysFont("Lucida Sans", 18).render("upgrade bow's salvo : out of stock", True, "Black")
                else:
                    upgrade_arrow_dispersion_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade bow's salvo : {int(Upgrade_arc['prices_upgrade'][1])} gold", True, "Black")

                if int(Upgrade_arc['prices_upgrade'][2]) == 1:
                    upgrade_arrow_salve_text = pygame.font.SysFont("Lucida Sans", 18).render("upgrade bow's dispersion : out of stock", True, "Black")
                else:
                    upgrade_arrow_salve_text = pygame.font.SysFont("Lucida Sans", 18).render(f"upgrade bow's dispersion : {int(Upgrade_arc['prices_upgrade'][2])} gold", True, "Black")
                LAST_TEXT_UPDATE_TIME = current_time

            B_upg_turret.update_colors_based_on_gold(gold, turrets.get_next_price("speed"))
            B_upg_turret1.update_colors_based_on_gold(gold, turrets.get_next_price("bullet"))
            B_upg_turret2.update_colors_based_on_gold(gold, turrets.get_next_price("special"))
            B_upg_cadence.update_colors_based_on_gold(gold, Upgrade_arc["prices_upgrade"][0])
            B_upg_salve.update_colors_based_on_gold(gold, Upgrade_arc["prices_upgrade"][1])
            B_upg_dispersion.update_colors_based_on_gold(gold, Upgrade_arc["prices_upgrade"][2])
            B_upg_tower.update_colors_based_on_gold(gold, upgrade_tower_price())


            SCREEN.blit(money_text, (WIDTH - (money_text.get_width()+5), 5))
            SCREEN.blit(upgrade_cadence_text, (WIDTH - (upgrade_cadence_text.get_width()+5), 25))
            SCREEN.blit(upgrade_bullet_text, (WIDTH - (upgrade_bullet_text.get_width()+5), 45))
            SCREEN.blit(upgrade_special_text, (WIDTH - (upgrade_special_text.get_width()+5), 65))

            SCREEN.blit(upgrade_arrow_cadence_text, (5, 80))
            SCREEN.blit(upgrade_arrow_dispersion_text, (5, 100))
            SCREEN.blit(upgrade_arrow_salve_text, (5, 120))
            SCREEN.blit(upg_tower_text, (5, 150))

            SCREEN.blit(wave_text, (5, 25))
            SCREEN.blit(tower_text, (5, 40))
            dead_fleche(enemies, Ensemble_fleche)
            draw(SCREEN, time, Ensemble_fleche,tower_level)

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
