import pygame
from libs.models import *
from libs.Turrets import *
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

SCREEN.fill('white')
resize_cannonball = pygame.transform.scale(cannonball, (SCREEN.get_width() / 20, SCREEN.get_height() / 19))

def resize_background ( image ):
    resized_image = (pygame.transform.scale(image,(SCREEN.get_width(),SCREEN.get_height())))
    return resized_image
#ajuste la taille du fond d'écran en fonction de la taille de la fenêtre

def height_ratio () :
    ratio= SCREEN.get_height() /600
    return ratio

def width_ratio ():
    ratio = SCREEN.get_width() / 800
    return ratio
def resize_tower (image):
    new_height = 565 * height_ratio()
    new_width = 475 * height_ratio()
    resized_image = (pygame.transform.scale(image,(new_width,new_height)))
    return resized_image


resized_cannonball = pygame.transform.scale(cannonball, (30, 30))

def resize_cannonball(image):
    resize = pygame.transform.scale(image,(28*height_ratio(),28*height_ratio()))
    return resize

#SCREEN.blit(tower_1, (-100, SCREEN.get_height()-450 )) #"colle" la tour en bas à gauche de la fenètre

#resized_tower_1 = pygame.transform.scale(tower_1, (SCREEN.get_width() / 1.7, SCREEN.get_height() / 2))
#fonction affichage continue à développer

#resized_background = pygame.transform.scale(background,(SCREEN.get_width(),SCREEN.get_height()))
#ajuste la taille du fond d'écran en fonction de la taille de la fenêtre


