import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, size, health, speed, power, pos, WIDTH, HEIGHT):
        super().__init__()
        # parametre
        self.name = name
        self.size = size # taille
        self.health = health # point de vie
        self.speed = speed # vitesse de déplacement
        self.power = power # nombre de déga
        self.ratio = 10000 + (pos*50+600) # ratio pour calcule du déplacement

        # position initiale
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        if self.name == "volant":
            self.rect = pygame.Rect((self.WIDTH - self.size[0] + 30*pos, self.HEIGHT - 200 - self.size[1]), self.size)
        else:
            self.rect = pygame.Rect((self.WIDTH - self.size[0] + 30*pos, self.HEIGHT - 100 - self.size[1]), self.size)

    def update(self,WIDTH, HEIGHT):# deplacement de l'ennemi

        # déplacement en y
        if self.name == "volant":
            self.rect.y = HEIGHT - 300 - self.size[1]
        else:
            self.rect.y = HEIGHT - 100 - self.size[1]

        # déplacement en x
        if self.rect.x > WIDTH/10 :
            self.ratio -= self.speed # calcule du déplacement sur un axe de 10000
            self.rect.x = (WIDTH*self.ratio)/10000 # produit en crois pour apliquer la position de l'axe 10000 a la taille de l'écran
            return 0
        else:
            self.rect.x = WIDTH/10-1
            return self.power



    def hitbox(self, damage): # calcule des point de vie
        self.health -= damage

    def est_mort(self): #vérifiation de mort
        return self.health <= 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def futur(self, frames, screen_width):
        if self.rect.x <= screen_width/10:
            return self.rect.x - 50, self.rect.y
        ratio = self.rect.x * 10000 / screen_width
        ratio -= self.speed * frames
        posx = (screen_width * ratio) / 10000
        return posx, self.rect.y  # retourne une position (x, y)


def create_wave(wave_number, WIDTH, HEIGHT): # créateur d'énnemies
    enemies = [] # lite des ennemies

    # choix du nombre d'enemie de mainère aléatoire
    p = [random.randint(wave_number,wave_number*3),1]
    m = [random.randint(wave_number,wave_number*3),1]
    g = [random.randint(wave_number,wave_number*3),1]
    v = [random.randint(wave_number,wave_number*3),1]
    type = [p,m,g,v]

    # si le nombre d'ennemies est trop grand on le baisse et on change de tière
    for i in range(3):
        while  type[i][0] > 5:
            type[i][0] = type[i][0] - 5
            type[i][1] += 1


    # création de tout les ennemie et implémentation dans la liste des ennemies
    for i in range(type[1][0]):
        enemy_petit = Enemy("petit", (15,30), 5000*type[1][1], 30, 5,i*20,WIDTH, HEIGHT)
        enemies.append(enemy_petit)
    for i in range(type[3][0]):
        enemy_volant = Enemy("volant", (50,30), 20000*type[3][1], 20, 20,i*50,WIDTH, HEIGHT)
        enemies.append(enemy_volant)
    for i in range(type[0][0]):
        enemy_moyen = Enemy("moyen", (30,50), 10000*type[0][1], 19, 10,i*20,WIDTH, HEIGHT)
        enemies.append(enemy_moyen)
    for i in range(type[2][0]):
        enemy_grand = Enemy("grand", (50,70), 20000*type[2][1], 10, 20,i*50,WIDTH, HEIGHT)
        enemies.append(enemy_grand)
    
        

    all_sprites = pygame.sprite.Group(enemies)
    return enemies, all_sprites

def update_enemy(SCREEN ,all_sprites, enemies, wave_number):
    damage = 0
    for i in all_sprites:
        damage += i.update(SCREEN.get_width(), SCREEN.get_height()) # mise a jour de la position de l'ennemi

    for enemy in enemies[:]:  # sécurisation de boucle
        if enemy.est_mort():
            all_sprites.remove(enemy)
            enemies.remove(enemy)

    if not enemies:
        wave_number += 1
        enemies, all_sprites = create_wave(wave_number,SCREEN.get_width(),SCREEN.get_height())

    return enemies, all_sprites, wave_number, int(damage)


def draw_enemy(SCREEN, enemies):
    for enemy in enemies:
        enemy.draw(SCREEN)
    return enemies
