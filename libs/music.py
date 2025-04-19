import pygame
from ui import draw_text

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))

playlist = [
    "./assets/musics/oo.wav",
    "./assets/musics/LePoissonSteve.mp3",
    "./assets/musics/MP.wav",
    "./assets/musics/HappyNation.mp3",
]

current_track = 0
pygame.mixer.music.load(playlist[current_track])
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

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


running = True
while running:
    screen.fill("white")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # get_next_music()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                play_next_music()
            if event.key == pygame.K_p:
                pygame.mixer.music.pause()
        
        volume_slider.handle_event(event)

    if not pygame.mixer.music.get_busy():
        play_next_music()

    draw_text(screen, "Volume Control", 180, 150)
    volume_slider.draw(screen)

    pygame.display.flip()

pygame.quit()