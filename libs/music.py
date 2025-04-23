import pygame
from libs.ui import Button

### To replace when done
# from ui import draw_text
def draw_text(screen:pygame.Surface, text:str, x:int, y:int, size:int=24):
    font = pygame.font.Font(None, size)
    img = font.render(text, True, "black")
    screen.blit(img, (x, y))
###

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))

playlist = [
    "./assets/musics/LePoissonSteve.mp3",
    "./assets/musics/test.mp3",
    "./assets/musics/HappyNation.mp3",
]

current_track = 0
pygame.mixer.music.load(playlist[current_track])
# pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

def play_main_menu(song_path:str="./assets/musics/TheInfiniteHole.mp3"):
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()


def get_next_music():
    global current_track
    if current_track == len(playlist)-1:
        song_id = (current_track+1) % len(playlist)
        print(f"now playing {playlist[song_id]}")
        play_next_music()
        current_track += 1

def play_next_music():
    global current_track
    song_id = (current_track+1) % len(playlist)
    pygame.mixer.music.load(playlist[song_id])
    pygame.mixer.music.play()
    print(song_id)
    current_track += 1

def play_last_music():
    global current_track
    song_id = (current_track-1) % len(playlist)
    pygame.mixer.music.load(playlist[song_id])
    pygame.mixer.music.play()   
    current_track -= 1


class VolumeSlider:
    def __init__(self, x, y, width, height, initial_volume=0.5):
        self.rect = pygame.Rect(x, y, width, height)  # track area
        self.knob_radius = 10  # knob size
        self.knob_x = x + int(0.5 * width)  # start at 50% volume
        self.dragging = False
        self.volume = initial_volume # 0.0 -> 1.0

    def draw(self, surface):
        pygame.draw.rect(surface, "gray", self.rect)  # Slider track
        pygame.draw.circle(surface, "blue", (self.knob_x, self.rect.centery), self.knob_radius)  # Knob

    def update(self, mouse_x):
        self.knob_x = max(self.rect.left, min(mouse_x, self.rect.right))  # clamp the knob in the slider area
        pos_x = self.knob_x - self.rect.left
        self.volume = pos_x / self.rect.width
        pygame.mixer.music.set_volume(self.volume)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.knob_x - self.knob_radius, self.rect.centery - self.knob_radius, self.knob_radius * 2, self.knob_radius * 2).collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update(event.pos[0])

volume_slider = VolumeSlider(100, 200, 300, 10, initial_volume=0.5)


def option_game_loop(screen, main_menu):
    clock = pygame.time.Clock()
    back_button = Button((230,230,230), (175,175,175), (150,150,150), (0, 0, 0), "<-- Back", None, 28, (120, 50), (20, 20),
                          screen.get_size(), lambda: setattr(main_menu, "game_state", "menu"), screen_to_print_on=screen)
    while main_menu.game_state == "options":
        screen.fill("white")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_next_music()
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()

            volume_slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                back_button.handle_click(pygame.mouse.get_pos())

            elif event.type == pygame.VIDEORESIZE:
                volume_slider.rect.width = int(screen.get_width() * 0.6)
                volume_slider.rect.x = (screen.get_width() - volume_slider.rect.width) // 2
                volume_slider.knob_x = int(volume_slider.rect.x + volume_slider.volume * volume_slider.rect.width)
                back_button.update_pos(screen.get_size())

        if not pygame.mixer.music.get_busy():
            play_next_music()

        draw_text(screen, "Volume Control", 180, 150)
        volume_slider.draw(screen)
        back_button.render(pygame.mouse.get_pos(), border_radius=8)

        pygame.display.flip()
        clock.tick(60)
