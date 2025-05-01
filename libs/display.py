import pygame
from libs.models import *
from libs.Turrets import *
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

def width_ratio ():
    ratio = SCREEN.get_width() / 800
    return ratio

def resize_tower_lvl_1(image):
    new_height = 365 * height_ratio()
    new_width = 123 * height_ratio()
    resized_image = (pygame.transform.scale(image,(new_width,new_height)))
    return resized_image

def resize_tower_lvl_2(image):
    new_height = 442 * height_ratio()
    new_width = 121 * height_ratio()
    resized_image = (pygame.transform.scale(image,(new_width,new_height)))
    return resized_image


resized_cannonball = pygame.transform.scale(cannonball, (30, 30))

def resize_cannonball(image):
    resize = pygame.transform.scale(image,(28*height_ratio(),28*height_ratio()))
    return resize

def resize_baliste(image):
    resize = pygame.transform.scale(image, (100*height_ratio(), 100*height_ratio()))
    return resize

def tower_height_position(tower_level):
    if tower_level == 1:
        return 333
    if tower_level == 2:
        return 410

def upgrade_tower():
    if tower_level<3:
        tower_level+=1
        print(tower_level)
        return tower_level

#SCREEN.blit(tower_1, (-100, SCREEN.get_height()-450 )) #"colle" la tour en bas à gauche de la fenètre

#resized_tower_1 = pygame.transform.scale(tower_1, (SCREEN.get_width() / 1.7, SCREEN.get_height() / 2))
#fonction affichage continue à développer

#resized_background = pygame.transform.scale(background,(SCREEN.get_width(),SCREEN.get_height()))
#ajuste la taille du fond d'écran en fonction de la taille de la fenêtre

sprite_sheet_image_test = pygame.image.load("assets/doux.png").convert_alpha()
big_monster = pygame.image.load("assets/batedor_walk.png")

black = (0,0,0)
def get_sprite_image(sheet,frame,width,height,scale,colour):
    image = pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet,(0,0),(frame*width,0,width,height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image



class Spritesheet() :
    def __init__(self,image):
        self.sheet = image

    def get_sprite_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image = pygame.transform.flip(image,False,False)
        image.set_colorkey(colour)
        return image

sprite_sheet = Spritesheet(sprite_sheet_image_test)
big_monster_sprite_sheet = Spritesheet(big_monster)

run_animation=[]
sprint_animation=[]
big_monster_run = []
run_animation_steps = 7
sprint_animation_steps = 7
big_monster_run_steps = 8
for x in range (4,4+run_animation_steps):
    run_animation.append(sprite_sheet.get_sprite_image(x, 24, 24, 3, black))
for y in range (18,18+sprint_animation_steps ):
    sprint_animation.append(sprite_sheet.get_sprite_image(y, 24, 24, 3, black))
for j in range (0, run_animation_steps):
    big_monster_run.append((big_monster_sprite_sheet.get_sprite_image(j,320,320,0.2,black)))


last_update = pygame.time.get_ticks()
animation_cooldown = 120
frame = 0

def animation_running(frame,time,last_update,animation_cooldown,run_animation,enemies):
    if time - last_update >= animation_cooldown:
        if frame == len(big_monster_run)-1:
            frame = 0
        else:
            frame += 1
        new_update = time
    else:
        new_update = last_update
    for i in range (len(enemies)):
        SCREEN.blit(big_monster_run[frame], (enemies[i].rect.x-10,enemies[i].rect.y-15))
    return new_update,frame

def rotation_baliste(enemys):
    x,y= turrets.get_first_enemy_pos(enemys)
    angle=x/y
    return angle


