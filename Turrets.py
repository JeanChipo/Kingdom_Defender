import pygame
from models.py import*


class Turret_Gestion:
    def __init__(self):
        self.turrets = []
        self.turrets.append(Turret())

    def run(self, window, WIDTH):
        for elm in self.turrets:
            elm.update()
            elm.draw(window, WIDTH)


class Turret:
    def __init__(self):
        self.x = 40
        self.y = 40
        self.name = "Basic"
        self.width = 50
        self.height = 25
        self.turret = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullet = []
        self.damage = 10
        self.upgrade = []
        self.level = 1
        self.fire_rate = 10
        self.time = 0

    def update(self):
        self.time += 1
        self.firing()

    def firing(self):
        if self.time % self.fire_rate == 0:
            self.bullet.append(Bullet(self.x + self.width, self.y + self.height // 4, self.damage))

    def draw(self, screen, dist):
        screen.blit(pygame.transform.rotate(turret_model,-40.0), (25, 180))
        for elm in self.bullet:
            elm.update()
            elm.draw(screen)
        self.bullet = [elm for elm in self.bullet if elm.x <= dist]


class Bullet:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = 10
        self.width = 10
        self.height = 10
        self.bullet = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += self.speed
        self.bullet.move_ip(self.speed, 0)


    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.bullet)
