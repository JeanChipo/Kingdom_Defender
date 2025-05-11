import pygame
from libs.models import *

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

SCREEN.fill('white')
resize_cannonball = pygame.transform.scale(cannonball, (SCREEN.get_width() / 20, SCREEN.get_height() / 19))
tower_level=1

def resize_background ( image ):
    resized_image = (pygame.transform.scale(image,(SCREEN.get_width(),SCREEN.get_height())))
    return resized_image
#ajuste la taille du fond d'écran en fonction de la taille de la fenêtre

def height_ratio () :
    ratio= SCREEN.get_height() /600
    return ratio
#renvoie le ratio d'aggrandissement de la hauteur fenêtre actuelle par rapport à la hauteur initiale (600 pixels)

def width_ratio ():
    ratio = SCREEN.get_width() / 800
    return ratio
#renvoie le ratio d'aggrandissement de la largeur fenêtre actuelle par rapport à la largeur initiale (800 pixels)


def resize_tower_lvl_1(image):
    new_height = 365 * height_ratio()
    new_width = 123 * height_ratio()
    resized_image = (pygame.transform.scale(image,(new_width,new_height)))
    return resized_image
#modifie la largeure et la hauteure de l'image d'entrée avec les paramêtre initiaux de tower_1 en fonction de la hauteur de la fenêtre actuelle

def resize_tower_lvl_2(image):
    new_height = 442 * height_ratio()
    new_width = 121 * height_ratio()
    resized_image = (pygame.transform.scale(image,(new_width,new_height)))
    return resized_image
#modifie la largeure et la hauteure de l'image d'entrée avec les paramêtre initiaux de tower_2 en fonction de la hauteur de la fenêtre actuelle

def resize_tower_lvl_3(image):
    new_height = 507 * height_ratio()
    new_width = 121 * height_ratio()
    resized_image = (pygame.transform.scale(image,(new_width,new_height)))
    return resized_image

#modifie la largeure et la hauteure de l'image d'entrée avec les paramêtre initiaux de tower_2 en fonction de la hauteur de la fenêtre actuelle


resized_cannonball = pygame.transform.scale(cannonball, (30, 30))
#initialise la variable contenant la version de cannonball adaptée à la taille de la fenêtre

def resize_cannonball(image):
    resize = pygame.transform.scale(image,(15*height_ratio(),15*height_ratio()))
    return resize
#modifie la largeure et la hauteure de l'image d'entrée avec les paramêtre initiaux de cannonball en fonction de la hauteur de la fenêtre actuelle


def resize_baliste(image):
    resize = pygame.transform.scale(image, (100*height_ratio(), 100*height_ratio()))
    return resize
#modifie la largeure et la hauteure de l'image d'entrée avec les paramêtre initiaux de baliste en fonction de la hauteur de la fenêtre actuelle


arrow = pygame.transform.rotate(arrow,-90)
#initialise l'angle initial de la variable contenant la version de arrow adaptée à la taille de la fenêtre

def resize_fleche(image):
    resize = pygame.transform.scale(image, ((368/10) * height_ratio(), (368/10) * height_ratio()))
    return resize
#modifie la largeure et la hauteure de l'image d'entrée avec les paramêtre initiaux de la flèche tirée par le joueur en fonction de la hauteur de la fenêtre actuelle

def resize_monster(image,x,y):
    new_height = y * height_ratio()
    new_width = x * height_ratio()
    resized_monster= (pygame.transform.scale(image,(new_width,new_height)))
    resized_monster.set_colorkey(0,0)
    return resized_monster

#modifie la largeure et la hauteure de l'image d'entrée avec les paramêtre initiaux x et y en fonction de la hauteur de la fenêtre actuelle
#rend le fond de l'image transparent

def tower_height_position(tower_level):
    if tower_level == 1:
        return 333
    if tower_level == 2:
        return 410
    if tower_level == 3:
        return 470
#définit la position y de la tour en fonction de son niveau




big_monster = pygame.image.load("assets/batedor_walk.png")
litlle_monster = pygame.image.load("assets/slime.jiggle.png")
medium_monster = pygame.image.load("assets/goblinsword.png")
flying_monster = pygame.image.load("assets/flying_monster_8_frames.png")
#initialise les variables contenant les spritesheet des animations des monstres

black = (0,0,0)
#initialise la variable couleurs pour rendre le fond des spritesheet transparent




class Spritesheet() :
    def __init__(self,image):
        self.sheet = image

    def get_sprite_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image
    #selection d'une partie précise du spritesheet en fonction de la frame, de la hauteur et largeur et modification de sa taille


#création de la classe Spritesheet


big_monster_sprite_sheet = Spritesheet(big_monster)
litlle_monster_sprite_sheet = Spritesheet(litlle_monster)
medium_monster_sprite_sheet = Spritesheet(medium_monster)
flying_monster_sprite_sheet = Spritesheet(flying_monster)
#initialisation des variables de classe Spritesheet

big_monster_run = []
litlle_monster_run = []
medium_monster_run = []
flying_monster_run = []

run_animation_steps = 7
#initialisation de la variable contenant le nombre de frame de toutes les animations


for j in range (0, run_animation_steps):
    big_monster_run.append((big_monster_sprite_sheet.get_sprite_image(j,320,320,0.5,black)))
    litlle_monster_run.append((litlle_monster_sprite_sheet.get_sprite_image(j, 64, 64, 1, black)))
    medium_monster_run.append((medium_monster_sprite_sheet.get_sprite_image(j, 65, 64, 2, black)))
    flying_monster_run.append((flying_monster_sprite_sheet.get_sprite_image(j,81,71,0.7,black)))
#implémentation des différententes frames dans les listes correspondante

medium_monster_run.reverse()
#inversion du sens de lecture des frames de medium_monster_run à cause d'un mauvais spritesheet

last_update = pygame.time.get_ticks()
#initialisation de la variable contenant le moment du dernier changement de frame

animation_cooldown = 120
#initialisation de la variable contenant le temps entre chaque changement de frame

frame = 0
#initialisation de la variable contenant la position de la frame à afficher

def animation_big_monster_running(frame,time,last_update,animation_cooldown,enemies):
    if time - last_update >= animation_cooldown:
        if frame == len(big_monster_run)-1:
            frame = 0
        else:
            frame += 1
        new_update = time
    else:
        new_update = last_update
    for i in range (len(enemies)):
        if enemies[i].name == "grand":
            SCREEN.blit(resize_monster(big_monster_run[frame],320*0.5,320*0.5), (enemies[i].rect.x - 50, enemies[i].rect.y - 15))
        elif enemies[i].name == "petit":
            SCREEN.blit(resize_monster(litlle_monster_run[frame],64,64), (enemies[i].rect.x - 10, enemies[i].rect.y - 15))
        elif enemies[i].name == "moyen":
            SCREEN.blit(resize_monster(medium_monster_run[frame],65*2,64*2), (enemies[i].rect.x - 65, enemies[i].rect.y - 15))
        elif enemies[i].name == "volant":
            SCREEN.blit(resize_monster(flying_monster_run[frame],81*0.7,71*0.7), (enemies[i].rect.x - 10, enemies[i].rect.y - 5))

    return new_update,frame
    #affiche la frame correspondant au nom de l'ennemi et au numéro de frame donné
    #met à jour la variable contenant le moment du dernier changement de frame
    #renvoie le nouveau numéro de frame et la variable contenant le moment du dernier changement de frame



