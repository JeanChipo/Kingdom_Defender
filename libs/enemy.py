import pygame
import random
from libs.Display import*

class Enemy(pygame.sprite.Sprite):
    def __init__(self, size, health, speed, power, pos, WIDTH, HEIGHT):
        super().__init__()
        # parametre
        self.size = size # taille
        self.health = health # point de vie
        self.speed = speed # vitesse de déplacement
        self.power = power # nombre de déga
        self.ratio = 10000 # ratio pour calcule du déplacement

        # position initiale
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.rect = pygame.Rect((WIDTH - self.size[0] + 2*pos, HEIGHT - 100 - self.size[1]), self.size)



    def update(self,WIDTH, HEIGHT):# deplacement de l'ennemi

        # déplacement en x
        if self.rect.x > WIDTH/10 :
            self.ratio -= self.speed # calcule du déplacement sur un axe de 10000
            self.rect.x = (WIDTH*self.ratio)/10000 # produit en crois pour apliquer la position de l'axe 10000 a la taille de l'écran
        else:
            self.rect.x = WIDTH/10

        # déplacement en y
        self.rect.y = HEIGHT - 100 - self.size[1]


    def hitbox(self, damage): # calcule des point de vie
        self.health -= damage

    def est_mort(self): #vérifiation de mort
        return self.health <= 0

    def draw(self, surface): # méthode d'affichage
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


def create_wave(wave_number, WIDTH, HEIGHT): # créateur d'énnemies
    enemies = [] # lite des ennemies

    # choix du nombre d'enemie de mainère aléatoire
    p = [random.randint(wave_number,wave_number*3),1]
    m = [random.randint(wave_number,wave_number*3),1]
    g = [random.randint(wave_number,wave_number*3),1]
    type = [p,m,g]

    # si le nombre d'ennemies est trop grand on le baisse et on change de tière
    for i in range(3):
        while  type[i][0] > 5:
            type[i][0] = type[i][0] - 5
            type[i][1] += 1
            print(type[i][1])

    # création de tout les ennemie et implémentation dans la liste des ennemies
    for i in range(type[1][0]):
        enemy_petit = Enemy((15,30), 5000*type[1][1], 30, 5,i*30,WIDTH, HEIGHT)
        enemies.append(enemy_petit)
    for i in range(type[0][0]):
        enemy_moyen = Enemy((30,50), 10000*type[0][1], 20, 10,i*20,WIDTH, HEIGHT)
        enemies.append(enemy_moyen)
    for i in range(type[2][0]):
        enemy_grand = Enemy((50,70), 20000*type[2][1], 10, 20,i*50,WIDTH, HEIGHT)
        enemies.append(enemy_grand)

    all_sprites = pygame.sprite.Group(enemies)
    return enemies, all_sprites


def run_enemy(SCREEN,all_sprites,enemies,wave_number,list_turret): # fonction d'exécution du scripte enemy.py
    # déplacement des ennemies
    all_sprites.update(SCREEN.get_width(),600 * height_ratio())

    # vérification si les ennemies sont touchés  par une tourelle et s'il meurt

    for enemy in enemies[:]:  # sécurisation de boucle
        if enemy.est_mort():
            all_sprites.remove(enemy)
            enemies.remove(enemy)

    # création d'une nouvelle vague quand tout les ennemies sont mort
    if not enemies:
        wave_number += 1
        enemies, all_sprites = create_wave(wave_number,SCREEN.get_width(),SCREEN.get_height())

    # affichage des ennemies
    for enemy in enemies:
        enemy.draw(SCREEN)

    return enemies, all_sprites,  wave_number

def futur(posx,speed):
    ratio = posx * 10000 / WIDTH
    ratio -= speed * 120
    posx = (WIDTH * ratio) / 10000
    return posx

