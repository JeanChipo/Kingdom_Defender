import pygame

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
                 normal_color: str | tuple[int, int, int],
                 hover_color: str | tuple[int, int, int],
                 pressed_color: str | tuple[int, int, int],
                 text_color: str | tuple[int, int, int],
                 text: str,
                 font: str,
                 font_size: int,
                 button_size: tuple[int, int],
                 Button_coords: tuple[int, int],
                 screen_size: tuple[int, int],
                 function_to_call: callable,
                 screen_to_print_on: pygame.Surface
                 ) -> None:

        self.normal_color = pygame.Color(normal_color)
        self.hover_color = pygame.Color(hover_color)
        self.pressed_color = pygame.Color(pressed_color)
        self.text_color = pygame.Color(text_color)
        self.text = text
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.font.render(text, True, self.text_color)
        self.function_to_call = function_to_call
        self.screen_to_print_on = screen_to_print_on
        self.screen_width, self.screen_height = screen_size
        self.button_width, self.button_height = button_size
        self.coord_x, self.coord_y = Button_coords  

    def is_pressed(self, mouse: tuple[int, int]) -> bool:
        return (self.coord_x <= mouse[0] <= self.coord_x + self.button_width and
                self.coord_y <= mouse[1] <= self.coord_y + self.button_height)

    def render(self, mouse: tuple[int, int]) -> None:
        if self.is_pressed(mouse):
            pygame.draw.rect(self.screen_to_print_on, self.hover_color, 
                            [self.coord_x, self.coord_y, self.button_width, self.button_height])
        else:
            pygame.draw.rect(self.screen_to_print_on, self.normal_color,
                            [self.coord_x, self.coord_y, self.button_width, self.button_height])
        self.screen_to_print_on.blit(self.text_surface, (self.coord_x + 10 , self.coord_y + self.button_height//4))

    def handle_click(self, mouse: tuple[int, int]) -> None:
        if self.is_pressed(mouse):
            pygame.draw.rect(self.screen_to_print_on, self.hover_color,
                            [self.coord_x, self.coord_y, self.button_width, self.button_height])
            self.function_to_call()
            pygame.display.update([self.coord_x, self.coord_y, self.button_width, self.button_height])

def menu_but(screen_to_print_on:pygame.Surface, 
         bg_color: str | tuple[int, int, int], 
         initial_dimensions: tuple[int, int, int, int], # (left, top, width, height)
         resize_ratio: tuple[float, float],
         ) -> pygame.Rect:
    left, top, width, height = initial_dimensions
    scaled_width = int(width * resize_ratio[0])
    scaled_height = int(height * resize_ratio[1])
    scaled_rect = pygame.Rect(left, top, scaled_width, scaled_height)
    return pygame.draw.rect(screen_to_print_on, bg_color, scaled_rect)

