import pygame
from libs.transitions import fade_to

class MainMenu:
    def __init__(self, screen:pygame.Surface):
        self.game_state = "menu"     # "menu", "running", "ended", "options"
        screen_size = screen.get_size()
        self.screen = screen
        self.band_size = 12.5
        self.buttons = [
            Button((230,230,230), (175,175,175), (150,150,150), (0,0,0), "New Game", None, 32, (140, 60), (0+self.band_size, 300+self.band_size), screen_size, self.start_new_game , screen),
            Button((230,230,230), (175,175,175), (150,150,150), (0,0,0), "Load Game", None, 32, (140, 60), (0+self.band_size, 300+60*1+self.band_size), screen_size, self.load_game, screen),
            Button((230,230,230), (175,175,175), (150,150,150), (0,0,0), "Options", None, 32, (140, 60), (0+self.band_size, 300+60*2+self.band_size), screen_size, self.open_options, screen),
            Button((230,230,230), (175,175,175), (150,150,150), (0,0,0), "Quit", None, 32, (140, 60), (0+self.band_size, 300+60*3+self.band_size), screen_size, self.quit_game, screen),
        ]

    def render(self, mouse: tuple[int, int], ratio:tuple[int,int]=(1,1)):
        self.menu = menu_but(self.screen, "white", (0, 300, 140+2*self.band_size, 240+2*self.band_size), ratio)
        for button in self.buttons:
            button.render(mouse)
        self.menu

    def start_new_game(self):
        self.game_state = "running"
        fade_to(self.screen, (0,0,0), 2000)

    def quit_game(self):
        self.game_state = "ended"
        pygame.quit()
        exit()

    def load_game(self):
        self.game_state = "running"

    def open_options(self):
        self.game_state = "options"

    


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

        self.normal_color = pygame.Color(normal_color)
        self.hover_color = pygame.Color(hover_color)
        self.pressed_color = pygame.Color(pressed_color)
        self.text_color = pygame.Color(text_color)
        self.original_text_color = self.text_color
        self.text = text
        self.font = pygame.font.SysFont(font, font_size)
        self.function_to_call = function_to_call
        self.screen_to_print_on = screen_to_print_on
        self.screen_width, self.screen_height = screen_size
        self.button_width, self.button_height = button_size
        self.coord_x, self.coord_y = Button_coords
        self.rel_x = Button_coords[0] / screen_size[0]
        self.rel_y = Button_coords[1] / screen_size[1]
        self.is_being_pressed = False

    def update_pos(self, screen_size: tuple[int, int]):
        self.screen_width, self.screen_height = screen_size
        self.coord_x = int(self.rel_x * self.screen_width)
        self.coord_y = int(self.rel_y * self.screen_height)

    def is_hovered(self, mouse: tuple[int, int]) -> bool:
        return (self.coord_x <= mouse[0] <= self.coord_x + self.button_width and
                self.coord_y <= mouse[1] <= self.coord_y + self.button_height)

    def render(self, mouse: tuple[int, int], border_radius:int=0) -> None:
        color_to_use = self.normal_color
        text_color = self.text_color
        offset = 0

        if self.is_being_pressed:
            color_to_use = self.pressed_color
            offset = 2  # slight y offset when pressed
        elif self.is_hovered(mouse):
            color_to_use = self.hover_color
            text_color = self.normal_color  # invert colors on hover

        pygame.draw.rect(self.screen_to_print_on, color_to_use,
            [self.coord_x, self.coord_y, self.button_width, self.button_height])

        text_surface = self.font.render(self.text, True, text_color)
        text_x = self.coord_x + (self.button_width - text_surface.get_width()) // 2
        text_y = self.coord_y + (self.button_height - text_surface.get_height()) // 2 + offset
        self.screen_to_print_on.blit(text_surface, (text_x, text_y))

    def handle_click(self, mouse: tuple[int, int]) -> None:
        if self.is_hovered(mouse):
            self.is_being_pressed = True
            self.render(mouse)
            pygame.display.update([self.coord_x, self.coord_y, self.button_width, self.button_height])
            pygame.time.delay(100)  # short delay to show press
            self.function_to_call()
            self.is_being_pressed = False


def menu_but(screen_to_print_on: pygame.Surface, 
             bg_color: str | tuple[int,int,int] | tuple[int,int,int,int], 
             initial_coords: tuple[int, int, int, int], # (left, top, width, height)
             resize_ratio: tuple[float, float]) -> pygame.Rect:
    
    left, top, width, height = initial_coords
    scaled_width = int(width * resize_ratio[0])
    scaled_height = int(height * resize_ratio[1])
    transparent_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
    transparent_surface.fill(bg_color)
    screen_to_print_on.blit(transparent_surface, (left, top))
    return pygame.Rect(left, top, scaled_width, scaled_height)

