import pygame
import random

pygame.init()
SCREEN_X, SCREEN_Y = 800, 600
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, size, health, speed, power, pos):
        super().__init__()
        # parametre
        self.size = size
        self.health = health
        self.speed = speed
        self.power = power

        self.rect = pygame.Rect((SCREEN_X - self.size[0] - pos, SCREEN_Y - 100 - self.size[1]), self.size)

    def update(self):# deplacement de l'ennemi
        # condition stop du deplacement
        if self.rect.x > 100:
            self.rect.x -= (self.speed)

    def hitbox(self, canon):
        self.health -= 100

    def est_mort(self):
        return self.health <= 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


def create_wave(wave_number):
    enemies = []
    p = [random.randint(wave_number,wave_number*3),1]
    m = [random.randint(wave_number,wave_number*3),1]
    g = [random.randint(wave_number,wave_number*3),1]
    type = [p,m,g]
    for i in range(3):
        while  type[i][0] > 5:
            type[i][0] = type[i][0] - 5
            type[i][1] += 1
            print(type[i][1])

    for i in range(type[0][0]):
        enemy_moyen = Enemy((30,50), 10000, 2, 10,i*20)
        enemies.append(enemy_moyen)
    for i in range(type[1][0]):
        enemy_petit = Enemy((15,30), 5000, 3, 5,i*30)
        enemies.append(enemy_petit)
    for i in range(type[2][0]):
        enemy_grand = Enemy((50,70), 20000, 1, 20,i*50)
        enemies.append(enemy_grand)

    all_sprites = pygame.sprite.Group(enemies)
    return enemies, all_sprites


def update_enemy(all_sprites, enemies, wave_number, list_turret):
    all_sprites.update()

    if list_turret:
        for enemy in enemies[:]:
            for t in list_turret:
                if enemy.rect.colliderect(t):
                    enemy.hitbox(t)
            if enemy.est_mort():
                all_sprites.remove(enemy)
                enemies.remove(enemy)

    if not enemies:
        wave_number += 1
        enemies, all_sprites = create_wave(wave_number)

    return enemies, all_sprites, wave_number


def draw_enemy(SCREEN, enemies):
    for enemy in enemies:
        enemy.draw(SCREEN)
