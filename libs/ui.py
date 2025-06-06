import pygame
import time
from libs.transitions import ScreenFader

class MainMenu:
    def __init__(self, screen: pygame.Surface, fader: ScreenFader):
        ''' classe de gestion des boutons et fonctions associées au menu principal. '''
        self.screen = screen
        self.fader = fader
        self.game_state = "menu"  # "menu", "running", "ended", "options", "credits", "steve"
        screen_size = screen.get_size()
        self.band_size = 12.5
        self.buttons = [
            Button((230,230,230), (175,175,175), (150,150,150), (0,0,0), "Start game", None, 32, (140, 60), (0+self.band_size, 300+self.band_size), screen_size, self.start_new_game , screen),
            Button((230,230,230), (175,175,175), (150,150,150), (0,0,0), "Settings", None, 32, (140, 60), (0+self.band_size, 300+60*1+self.band_size), screen_size, self.open_options, screen),
            Button((230,230,230), (175,175,175), (150,150,150), (0,0,0), "Credits", None, 32, (140, 60), (0+self.band_size, 300+60*2+self.band_size), screen_size, self.open_credits, screen),
            Button((230,230,230), (175,175,175), (150,150,150), (0,0,0), "Quit", None, 32, (140, 60), (0+self.band_size, 300+60*3+self.band_size), screen_size, self.quit_game, screen),
        ]

    def render(self, mouse: tuple[int, int], ratio:tuple[int,int]=(1,1)):
        ''' affiche les boutons et leur arrière plan. '''
        self.menu = menu_but(self.screen, "white", (0, 300, 140+2*self.band_size, 240+2*self.band_size), ratio)
        for button in self.buttons:     # on affiche chaque bouton du menu principal
            button.render(mouse)
        self.menu

    def start_new_game(self):
        ''' méthode de lancement d'une nouvelle partie. '''
        def switch_to_game():   # il faut une fonction en paramètre de fader.start
            self.game_state = "running"
        self.fader.start(func_on_mid=switch_to_game) # on change l'état du jeu à la moitié de la transition

    def quit_game(self):
        ''' méthode changeant l'état du jeu en "ended". '''
        self.game_state = "ended"

    def open_options(self):
        ''' méthode changant l'état du jeu en "options". '''
        self.game_state = "options"

    def open_credits(self):
        ''' méthode changant l'état du jeu en "credits". '''
        self.game_state = "credits"
        self.credits_game_loop()    # on lance la boucle de jeu pour les crédits

    def credits_game_loop(self):
        ''' boucle de jeu pour les crédits. '''
        clock = pygame.time.Clock()
        back_button = Button((255,255,255), (175,175,175), (150,150,150), (0, 0, 0), "<-- Back", None, 28, (120, 50), (20, 20),
                              self.screen.get_size(), lambda: setattr(self, "game_state", "menu"), screen_to_print_on=self.screen)

        # On initialise le texte des crédits, la police, l'espacement entre les lignes et la position de départ
        credits_text = "-- Kingdom defender --\n"                                                               \
                       "\n"                                                                                     \
                       "Game by @JeanChipo, @WarennOne, @QuentinDegouge, @Dragbnx, @Kosinix-17 on github\n"     \
                       "\n"                                                                                     \
                       "Main menu songs: \n"                                                                    \
                       "    \"Chanson d'automne\" by Chris Christodoulou - from Risk of Rain\n"                 \
                       "    \"TheInfiniteHole\" by Tom Schley - from The Stanley Parable\n"                     \
                       "\n"                                                                                     \
                       "In game songs: \n"                                                                      \
                       "    \"Michael Flatley's Lord Of The Dance\" by Ronan Hardiman\n"                        \
                       "\n"                                                                                     \
                       "Easter egg song:\n"                                                                     \
                       "    \"le poisson steve\" by @tomomp3 and @vigzvigz"
        lines = credits_text.split("\n")

        font_size = max(24, self.screen.get_height() // 30)
        font = pygame.font.Font(None, font_size)
        line_spacing = font_size + 10
        y_offset = self.screen.get_height() // 10
        
        while self.game_state == "credits":
            self.screen.fill((230, 230, 230))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    back_button.handle_click(pygame.mouse.get_pos())

                elif event.type == pygame.VIDEORESIZE:
                    back_button.update_pos(self.screen.get_size())

            current_y_offset = y_offset
            for l in lines:
                text_surface = font.render(l, True, "Black")
                x = (self.screen.get_width() - text_surface.get_width()) // 2  # center the text
                self.screen.blit(text_surface, (x, current_y_offset))
                current_y_offset += line_spacing

            back_button.render(pygame.mouse.get_pos())
            pygame.display.flip()
            clock.tick(60)
        
class Button: 
    def __init__(self,
                 normal_color:  str | tuple[int, int, int],
                 hover_color:   str | tuple[int, int, int],
                 pressed_color: str | tuple[int, int, int],
                 text_color:    str | tuple[int, int, int],
                 text:          str,
                 font:          str,
                 font_size:     int,
                 button_size:   tuple[int, int],
                 Button_coords: tuple[int, int],
                 screen_size:   tuple[int, int],
                 function_to_call:   callable,
                 screen_to_print_on: pygame.Surface
                 ) -> None:
        ''' classe de création des boutons. '''

        self.normal_color = pygame.Color(normal_color)
        self.hover_color = pygame.Color(hover_color)
        self.pressed_color = pygame.Color(pressed_color)
        self.text_color = pygame.Color(text_color)
        self.text = text
        self.font = pygame.font.SysFont(font, font_size)
        self.function_to_call = function_to_call
        self.screen_to_print_on = screen_to_print_on

        self.screen_width, self.screen_height = screen_size
        self.button_width, self.button_height = button_size
        self.coord_x, self.coord_y = Button_coords
        self.width_ratio = self.button_width / self.screen_width
        self.height_ratio = self.button_height / self.screen_height
        self.x_ratio = self.coord_x / self.screen_width
        self.y_ratio = self.coord_y / self.screen_height

        self.is_being_pressed = False


    def update_pos(self, screen_size: tuple[int, int]):
        ''' méthode permettant la mise à jour de la position du bouton. '''
        self.screen_width, self.screen_height = screen_size
        self.button_width = int(self.width_ratio * self.screen_width)
        self.button_height = int(self.height_ratio * self.screen_height)
        self.coord_x = int(self.x_ratio * self.screen_width)
        self.coord_y = int(self.y_ratio * self.screen_height)

    def is_hovered(self, mouse: tuple[int, int]) -> bool:
        ''' renvoie un booléen selon le survolement de la souris sur le bouton. '''
        return (self.coord_x <= mouse[0] <= self.coord_x + self.button_width and
                self.coord_y <= mouse[1] <= self.coord_y + self.button_height)

    def render(self, mouse: tuple[int, int]) -> None:
        ''' méthode d'affichage du bouton. '''
        color_to_use = self.normal_color
        offset = 0

        if self.is_being_pressed:
            color_to_use = self.pressed_color
            offset = 2  # slight y offset when pressed
        elif self.is_hovered(mouse):
            color_to_use = self.hover_color
            # text_color = self.normal_color  # invert colors on hover

        pygame.draw.rect(self.screen_to_print_on, color_to_use,
            [self.coord_x, self.coord_y, self.button_width, self.button_height])

        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.coord_x + (self.button_width - text_surface.get_width()) // 2
        text_y = self.coord_y + (self.button_height - text_surface.get_height()) // 2 + offset
        self.screen_to_print_on.blit(text_surface, (text_x, text_y))

    def handle_click(self, mouse: tuple[int, int]) -> None:
        ''' gestion de la pression du bouton. '''
        if self.is_hovered(mouse):
            self.is_being_pressed = True
            self.render(mouse)
            pygame.display.update([self.coord_x, self.coord_y, self.button_width, self.button_height])
            pygame.time.delay(100)  # show press with delay
            self.function_to_call()
            self.is_being_pressed = False

    def update_colors_based_on_gold(self, gold:int, cost:int):
        ''' mise à jour de la couleur du bouton selon la quantité d'or 
        et le prix de l'amélioration associée. '''
        if cost == 0:
            self.normal_color = pygame.Color((0, 60, 255))
            self.hover_color = pygame.Color((0, 60, 255))
            self.pressed_color = pygame.Color((0, 60, 255))

        elif cost == 1:
            self.normal_color = pygame.Color((140, 140, 140))
            self.hover_color = pygame.Color((140, 140, 140))
            self.pressed_color = pygame.Color((140, 140, 140))

        elif gold >= cost:    # enough gold to buy
            self.normal_color = pygame.Color((157, 205, 128))
            self.hover_color = pygame.Color((101, 191, 77))
            self.pressed_color = pygame.Color((55, 105, 42))
            
        else:
            self.normal_color = pygame.Color((205, 128, 128))
            self.hover_color = pygame.Color((191, 77, 77))
            self.pressed_color = pygame.Color((105, 42, 42))

def menu_but(screen_to_print_on: pygame.Surface, 
             bg_color: str | tuple[int,int,int] | tuple[int,int,int,int], 
             initial_coords: tuple[int, int, int, int], # (left, top, width, height)
             resize_ratio: tuple[float, float]
             )-> pygame.Rect:
    ''' affichage d'un rectangle transparent permettant un arrière plan pour les boutons. '''
    
    left, top, width, height = initial_coords
    scaled_left = int(left * resize_ratio[0])
    scaled_top = int(top * resize_ratio[1])
    scaled_width = int(width * resize_ratio[0])
    scaled_height = int(height * resize_ratio[1])

    transparent_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
    transparent_surface.fill(bg_color)
    screen_to_print_on.blit(transparent_surface, (scaled_left, scaled_top))
    return pygame.Rect(scaled_left, scaled_top, scaled_width, scaled_height)


class TimedTextManager:
    def __init__(self, screen, font_size, color=(0, 0, 0)):
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.current_text = None
        self.end_time = 0

    def show_text(self, text, duration):
        self.current_text = self.font.render(text, True, self.color)
        self.end_time = time.time() + duration

    def update(self):
        if self.current_text and time.time() < self.end_time:
            self.screen.blit(self.current_text, (self.screen.get_width() // 2 - self.current_text.get_width() // 2, 10))
        else:
            self.current_text = None

def pause():
    ''' fonction de pause du jeu. '''
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
