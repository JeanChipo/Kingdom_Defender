import pygame
from libs.ui import Button

pygame.init()
pygame.mixer.init()

def back_button_func(main_menu):
    setattr(main_menu, "game_state", "menu")
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def press_steve(main_menu):
    setattr(main_menu, "game_state", "steve")
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

def steve_game_loop(screen, main_menu):
    setattr(main_menu, "game_state", "steve")
    clock = pygame.time.Clock()
    back_button = Button((230, 230, 230), (175, 175, 175), (150, 150, 150), (0, 0, 0), "<-- Back", None, 28, (120, 50), (20, 20),
                          screen.get_size(), lambda: back_button_func(main_menu), screen_to_print_on=screen)

    while main_menu.game_state == "steve":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("./assets/musics/LePoissonSteve.mp3")
                pygame.mixer.music.play()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                back_button.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.VIDEORESIZE:
                back_button.update_pos(screen.get_size())

        screen.fill("white")
        steve_img = pygame.image.load("./assets/steve.jpeg")
        steve_img = pygame.transform.scale(steve_img, (screen.get_width(), screen.get_height()))
        screen.blit(steve_img, (0, 0))

        back_button.render(pygame.mouse.get_pos(), border_radius=8)
        pygame.display.flip()
        clock.tick(60)
