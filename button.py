import pygame
from typing import Callable, Tuple, Optional

class But:
    def __init__(self,
                 normal_color: str | Tuple[int, int, int],
                 hover_color: str | Tuple[int, int, int],
                 pressed_color: str | Tuple[int, int, int],
                 text_color: str | Tuple[int, int, int],
                 text: str,
                 font: Optional[str],
                 font_size: int,
                 button_size: Tuple[int, int],
                 screen_size: Tuple[int, int],
                 function_to_call: Callable,
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
        self.coord_x = (self.screen_width - self.button_width) // 2
        self.coord_y = (self.screen_height - self.button_height) // 2

    def is_pressed(self, mouse: Tuple[int, int]) -> bool:
        return (self.coord_x <= mouse[0] <= self.coord_x + self.button_width and
                self.coord_y <= mouse[1] <= self.coord_y + self.button_height)

    def render(self, mouse: Tuple[int, int]) -> None:
        if self.is_pressed(mouse):
            pygame.draw.rect(self.screen_to_print_on, self.hover_color, 
                            [self.coord_x, self.coord_y, self.button_width, self.button_height])
        else:
            pygame.draw.rect(self.screen_to_print_on, self.normal_color,
                            [self.coord_x, self.coord_y, self.button_width, self.button_height])
        self.screen_to_print_on.blit(self.text_surface, (self.coord_x + 10 , self.coord_y + self.button_height//4))

    def handle_click(self, mouse: Tuple[int, int]) -> None:
        if self.is_pressed(mouse):
            self.function_to_call()
