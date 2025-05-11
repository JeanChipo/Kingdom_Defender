import pygame
from random import choice
from libs.ui import Button

pygame.init()
pygame.font.init()
pygame.mixer.init()

playlist = [
    "./assets/musics/Breakout.mp3",
    "./assets/musics/Celtic Dream.mp3",
    "./assets/musics/Cry Of The Celts.mp3",
    "./assets/musics/Fiery Nights.mp3",
    "./assets/musics/Gypsy.mp3",
    "./assets/musics/Lament.mp3",
    "./assets/musics/Lord Of The Dance.mp3",
    "./assets/musics/Nightmare.mp3",
    "./assets/musics/Our Wedding Day.mp3",
    "./assets/musics/Siamsa.mp3",
    "./assets/musics/Suil A Ruin.mp3",
    "./assets/musics/Victory.mp3",
    "./assets/musics/Warriors.mp3",
]

current_track = 0
pygame.mixer.music.load(playlist[current_track])
pygame.mixer.music.set_volume(0.5)

def shuffle_playlist():
    ''' fonction pour jouer une musique aléatoire dans le jeu pricipal depuis la playlist. '''
    global playlist
    music_index_list = [i for i in range(len(playlist))]
    shuffled_playlist = []
    while music_index_list:
        random_index = choice(music_index_list)
        shuffled_playlist.append(playlist[random_index])
        music_index_list.remove(random_index)
    playlist = shuffled_playlist

def play_main_menu(playlist:list[str]):
    ''' fonction pour jouer une musique aléatoire dans le menu principal. '''
    song_path = choice(playlist)
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

def play_next_music():
    ''' fonction pour jouer la prochaine musique dans la playlist. '''
    global current_track
    song_id = (current_track+1) % len(playlist)
    pygame.mixer.music.load(playlist[song_id])
    pygame.mixer.music.play()
    current_track += 1

# def play_last_music():
    # ''' fonction permettant de  '''
    # global current_track
    # song_id = (current_track-1) % len(playlist)
    # pygame.mixer.music.load(playlist[song_id])
    # pygame.mixer.music.play()   
    # current_track -= 1

class VolumeSlider:
    def __init__(self, x, y, width, height, initial_volume=0.5):
        ''' classe permettant de créer un slider de volume dans le menu des paramètres. '''
        self.rect = pygame.Rect(x, y, width, height)  # track area
        self.knob_radius = 10  # knob size
        self.knob_x = x + int(0.5 * width)  # start at 50% volume
        self.dragging = False
        self.volume = initial_volume # 0.0 -> 1.0

    def draw(self, surface):
        ''' afficher le slider de volume. '''
        pygame.draw.rect(surface, "gray", self.rect)  # Slider track
        pygame.draw.circle(surface, "blue", (self.knob_x, self.rect.centery), self.knob_radius)  # Knob

    def update(self, mouse_x):
        ''' met à jour la position du slider de volume. '''
        self.knob_x = max(self.rect.left, min(mouse_x, self.rect.right))  # clamp the knob in the slider area
        pos_x = self.knob_x - self.rect.left
        self.volume = pos_x / self.rect.width
        pygame.mixer.music.set_volume(self.volume)

    def handle_event(self, event):
        ''' permet de faire glisser le bouton de slider de volume. '''
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if pygame.Rect(self.knob_x - self.knob_radius, self.rect.centery - self.knob_radius, self.knob_radius * 2, self.knob_radius * 2).collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update(event.pos[0])

volume_slider = VolumeSlider(100, 200, 300, 10, initial_volume=0.5)


def option_game_loop(screen, main_menu):
    ''' boucle de jeu pour le menu des options. '''
    clock = pygame.time.Clock()
    back_button = Button((230,230,230), (175,175,175), (150,150,150), (0, 0, 0), "<-- Back", None, 28, (120, 50), (20, 20),
                          screen.get_size(), lambda: setattr(main_menu, "game_state", "menu"), screen_to_print_on=screen)
    
    volume_slider.rect.width = int(screen.get_width() * 0.6)
    volume_slider.rect.x = (screen.get_width() - volume_slider.rect.width) // 2
    volume_slider.knob_x = int(volume_slider.rect.x + volume_slider.volume * volume_slider.rect.width)

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                back_button.handle_click(pygame.mouse.get_pos())

            elif event.type == pygame.VIDEORESIZE:
                volume_slider.rect.width = int(screen.get_width() * 0.6)
                volume_slider.rect.x = (screen.get_width() - volume_slider.rect.width) // 2
                volume_slider.knob_x = int(volume_slider.rect.x + volume_slider.volume * volume_slider.rect.width)
                back_button.update_pos(screen.get_size())

        if not pygame.mixer.music.get_busy():
            play_next_music()

        texte_volume_control = pygame.font.Font(None, 24).render("Volume Control", True, "Black")
        screen.blit(texte_volume_control, ((screen.get_width() // 2 - texte_volume_control.get_width() // 2,
                                            volume_slider.rect.bottom + 20)))
        volume_slider.draw(screen)
        back_button.render(pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(60)
