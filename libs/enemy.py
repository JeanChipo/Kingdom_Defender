import pygame
import random
from libs.display import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name : str, size : int, health : int, speed : int, power : int, pos : int, valeur : int, WIDTH : int, HEIGHT : int):

        ### classe qui gère les ennemies ###

        super().__init__()
        # parametre

        self.name = name                        # nom de l'ennemi
        self.size = size                        # taille
        self.health = health                    # point de vie
        self.speed = speed                      # vitesse de déplacement
        self.power = power                      # nombre de déga
        self.ratio = 10000 + (pos*50+600)       # ratio pour calcule du déplacement
        self.valeur = valeur                    # valeur de l'ennemi pour le calcul de l'argent


        # position initiale
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        if self.name == "volant":
            self.rect = pygame.Rect((self.WIDTH - self.size[0] + 30*pos, self.HEIGHT - 200 - self.size[1]), self.size) # position de l'ennemi volant a 200 pixel du sol
        else:
            self.rect = pygame.Rect((self.WIDTH - self.size[0] + 30*pos, self.HEIGHT - 100 - self.size[1]), self.size) # position des l'ennemis normaux a 100 pixel du sol


    def update(self,WIDTH : int, HEIGHT : int):
        ### déplacement des l'ennemis ###

        # déplacement en y (permet de faire apparaitre les ennemies tout le temps en bas de l'écran meme si la taille de l'écran change)
        if self.name == "volant":
            self.rect.y = (HEIGHT - 300 - self.size[1]) * (1/height_ratio())
        else:
            self.rect.y = HEIGHT - 100 - self.size[1]

        # mise a jour de la taille de l'ennemi
        new_size = (self.size[0] * WIDTH / 800, self.size[1] * HEIGHT / 600) # meme calcul que lors de la création de l'ennemi
        self.rect.size = new_size  # mis à jour la taille du rect

        # déplacement en x
        if self.rect.x > WIDTH/10 : 
            self.ratio -= self.speed # calcule du déplacement sur un axe de 10000
            self.rect.x = (WIDTH*self.ratio)/10000 # produit en crois pour appliquer la position de l'axe 10000 a la taille de l'écran
            return 0
        else: # condition d'arret de l'ennemi
            self.rect.x = WIDTH/10-1
            return self.power



    def hitbox(self, damage : int):
        ### calcule des point de vie ###

        self.health -= damage

    def est_mort(self):
        ###vérification de mort ###

        return self.health <= 0

    def draw(self, surface):
        ### dessine l'ennemi (utilisé pour le débug) ###

        pygame.draw.rect(surface, (255, 0, 0), self.rect)



    def futur(self, frames : int, screen_width : int):
        ### fonction de prévision de la position de l'ennemi pour le tir des tourelles ###

        if self.rect.x <= (125*screen_width/800)+(screen_width/10): # condition d'arret de prédiction quand l'ennemi est trop proche de la tour
            return screen_width/10-1 + (self.size[0] * screen_width / 800)/2, self.rect.centery
        # calcule de la position futur de l'ennemi
        ratio = self.rect.centerx * 10000 / screen_width
        ratio -= self.speed * frames
        posx = (screen_width * ratio) / 10000
        return posx, self.rect.centery

    def money(self):
        ### fonction de renvoie de la valeur de l'ennemi pour le calcul de l'argent ###

        return self.valeur


def create_wave(wave_number : int, WIDTH : int, HEIGHT : int):
    ### créateur d'ennemies ###


    enemies = [] # lite des ennemies

    
    # choix du nombre d'enemie de mainère aléatoire
    if wave_number <= 3:
        p = [random.randint(wave_number,wave_number+5),0]
        m = [0, 0]
        g = [0, 0]
        v = [0, 0]
    elif wave_number <= 5:
        p = [random.randint(wave_number,wave_number+10),0]
        m = [random.randint(1,wave_number),0]
        v = [random.randint(wave_number, wave_number*3), 0]
        g = [0, 0]
    else :
        p = [random.randint(wave_number,wave_number + 10),0]
        m = [random.randint(wave_number,wave_number + 10),0]
        g = [random.randint(wave_number,wave_number + 10),0]
        v = [random.randint(wave_number,wave_number + 10),0]
    type = [p,m,g,v]

    # si le nombre d'ennemies est trop grand on le baisse et on change de tière
    for i in range(4):
        while  type[i][0] > 5:
            type[i][0] = type[i][0] - 5
            type[i][1] += 1



    # création de tout les ennemie et implémentation dans la liste des ennemies
    for i in range(type[0][0]):
        enemy_petit = Enemy("petit", (30,40), 2000 + 500*type[0][1], 20, 5,i*10, 500, WIDTH, HEIGHT)
        enemies.append(enemy_petit)
    for i in range(type[3][0]):
        enemy_volant = Enemy("volant", (30,30), 1000 + 500 * type[3][1], 20, 20,i*20, 100,WIDTH, HEIGHT)
        enemies.append(enemy_volant)
    for i in range(type[1][0]):
        enemy_moyen = Enemy("moyen", (30,90), 6000+2000*type[1][1], 15, 10,i*20, 1000,WIDTH, HEIGHT)
        enemies.append(enemy_moyen)
    for i in range(type[2][0]):
        enemy_grand = Enemy("grand", (100,140), 15000+6000*type[2][1], 10, 20,i*50, 5000,WIDTH, HEIGHT)
        enemies.append(enemy_grand)
    
        

    all_sprites = pygame.sprite.Group(enemies)
    return enemies, all_sprites


def update_enemy(SCREEN : pygame.Surface, all_sprites : list, enemies : list, wave_number : int):
    ### fonction main du fichier enemy.py ###

    damage = 0

    # mise a jour de la position de tout l'ennemi
    for i in all_sprites:
        damage += i.update(SCREEN.get_width(), SCREEN.get_height()) 

    # suppression des ennemies mort
    for enemy in enemies[:]:  
        if enemy.est_mort():
            all_sprites.remove(enemy)
            enemies.remove(enemy)

    # création d'une nouvelle vague si il n'y a plus d'ennemies
    if not enemies:
        wave_number += 1
        enemies, all_sprites = create_wave(wave_number,SCREEN.get_width(),SCREEN.get_height())

    # save des changements dans le main
    return enemies, all_sprites, wave_number, int(damage)


def draw_enemy(SCREEN : pygame.Surface, enemies : int):
    for enemy in enemies:
        enemy.draw(SCREEN)
    return enemies
