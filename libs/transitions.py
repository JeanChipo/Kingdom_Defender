import pygame

class ScreenFader:
    def __init__(self, screen: pygame.Surface, color=(0,0,0), duration=1000, steps=30):
        self.screen = screen    # display surface
        self.color = color
        self.duration = duration
        self.steps = steps   # nb of steps to achieve transition

        self.overlay = pygame.Surface(screen.get_size()).convert()
        self.overlay.fill(color)
        self.delay = duration // (2 * steps)
        self.step_alpha = 255 / steps
        self.reset()    # initialize the variables

    def reset(self):
        self.alpha = 0
        self.phase = 0     # 0=idle, 1=fading out, 2=fading in
        self.func_on_mid = None  # called once when fully black

    def start(self, func_on_mid: callable = None):
        if self.phase != 0:
            return      # can only start when idling 
        
        self.func_on_mid = func_on_mid    # /!\ func_on_mid is a function to call when the screen is fully covered
        self.phase = 1

    def update_overlay_size(self):
        self.overlay = pygame.Surface(self.screen.get_size()).convert()
        self.overlay.fill(self.color)

    def update(self):
        if self.phase == 0:
            return      # can only start when not idling 

        if self.phase == 1: # fading out
            self.alpha += self.step_alpha
            if self.alpha >= 128: pygame.mixer.music.fadeout(self.duration//2)
            if self.alpha >= 255:
                self.alpha = 255
                # pygame.mixer.music.stop()
                if self.func_on_mid:
                    self.func_on_mid()
                self.phase = 2

        elif self.phase == 2:   # fading back in
            self.alpha -= self.step_alpha
            if self.alpha <= 0:
                self.alpha = 0
                self.phase = 0

        self.overlay.set_alpha(int(self.alpha))
        self.screen.blit(self.overlay, (0, 0))
        pygame.time.wait(self.delay)