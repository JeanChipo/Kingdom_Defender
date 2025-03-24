import pygame
import random

pygame.init()
SCREEN_X, SCREEN_Y = 800, 600
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, size, health, speed, power):
        super().__init__()
        # parametre
        self.size = size
        self.health = health
        self.speed = speed
        self.power = power

        self.rect = pygame.Rect((SCREEN_X - self.size[0], SCREEN_Y - 100 - self.size[1]), self.size)

    def update(self):# deplacement de l'ennemi
        # condition stop du deplacement
        if self.rect.x > 50:
            self.rect.x -= self.speed

    def hitbox(self, canon):
        self.health -= 100

    def est_mort(self):
        return self.health <= 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


def create_wave(wave_number):
    enemies = []
    for i in range(wave_number + 2):
        size = (random.randint(20, 50), random.randint(30, 70))
        health = 500 * wave_number
        speed = random.randint(1, 5) + wave_number // 2
        power = random.randint(3, 10)
        enemy = Enemy(size, health, speed, power)
        enemies.append(enemy)

    all_sprites = pygame.sprite.Group(enemies)
    return enemies, all_sprites


def run_enemy(SCREEN,all_sprites,enemies,wave_number):
    all_sprites.update()

    #for enemy in enemies:
    #    for t in list_turret:
    #        if enemy.rect.colliderect(t.rect):
    #            enemy.hitbox(t.rect)
    #    if enemy.est_mort():
    #        all_sprites.remove(enemy)
    #        enemies.remove(enemy)

    if not enemies:
        wave_number += 1
        enemies, all_sprites = create_wave(wave_number)

    for enemy in enemies:
        enemy.draw(SCREEN)
