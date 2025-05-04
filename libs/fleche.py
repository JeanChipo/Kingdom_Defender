import math
import pygame
from pygame.examples.moveit import WIDTH

from libs.display import upgrade_tower
from libs.music import HEIGHT

amelioration_tower=1/8
class Fleche:
    def __init__(self, WIDTH, HEIGHT, angle, mouse_pos, time, SCREEN):
        self.width = WIDTH
        self.height = HEIGHT
        self.time_start = time
        self.time = 0
        self.x_end = mouse_pos[0]
        self.y_end = mouse_pos[1]
        self.gravity = 500
        self.angle = angle  # angle en radians
        self.x_init = WIDTH * amelioration_tower
        self.y_init = HEIGHT * amelioration_tower
        self.x = self.x_init
        self.y = self.y_init
        self.screen = SCREEN
        self.damage = 1000
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        # Calcule des vitesses x et y
        self.v_x = max(100,WIDTH*0.25)
        distance_x = self.x_end - self.x_init
        temps_arrive = distance_x / self.v_x
        self.v_y = (self.y_end-self.y_init-0.5*self.gravity*temps_arrive)/(math.sin(self.angle)*temps_arrive)

    def position(self, time):
        self.time = time  # Mettre à jour le temps
        temps_ecoule = (self.time - self.time_start) / 1000
        self.x = self.x_init + math.cos(self.angle) * temps_ecoule * self.v_x
        self.y = self.y_init+math.sin(self.angle)*temps_ecoule*self.v_y+0.5*self.gravity*temps_ecoule**2

        return self.x < 0 or self.x > self.width or self.y < 0 or self.y > self.height

def dead_fleche(enemys, Ensemble_fleche):
    for ennemy in enemys[:]:
        for fleche in Ensemble_fleche[:]:
            # Met à jour les coordonnées du rectangle de collision
            fleche.rect.x = fleche.x
            fleche.rect.y = fleche.y

            if fleche.rect.colliderect(ennemy.rect):
                Ensemble_fleche.remove(fleche)
                ennemy.hitbox(1000)
                if ennemy.est_mort():
                    enemys.remove(ennemy)
                break


def draw(time, SCREEN,Ensemble_fleche):
    # Gérer les flèches existantes
    for fleche in Ensemble_fleche:
        if not fleche.position(time):
            # Dessiner la flèche
            pygame.draw.rect(SCREEN, (0, 0, 255), (int(fleche.x), int(fleche.y), 10, 10))

        else:
            # Supprimer la flèche qui sort de l'écran
            Ensemble_fleche.remove(fleche)


def creation(WIDTH, HEIGHT, angle, SCREEN, mouse_pos, time, Ensemble_fleche, Update_arc):
    for i in range(Update_arc["salve"]):
        for l in range(len(Update_arc["dispersion"])):
            current_angle = math.radians(-Update_arc["dispersion"][l])  # Convertit chaque angle de dispersion en radians
            fleche = Fleche(WIDTH, HEIGHT, current_angle, mouse_pos, time + i*200, SCREEN)  # délai entre les fléches de la salve (0,2sec) grâce à i*200
            Ensemble_fleche.append(fleche)


def cadence(Ensemble_fleche, upgrade, mouse_pos, time, WIDTH, HEIGHT, SCREEN, Upgrade_arc):
    # Si la liste est vide
    if len(Ensemble_fleche) == 0:
        creation(WIDTH, HEIGHT, 0, SCREEN, mouse_pos, time, Ensemble_fleche, Upgrade_arc)
        return True

    # Vérifie le temps écoulé depuis la dernière flèche
    last_fleche = len(Ensemble_fleche) - 1  # Index de la dernière flèche
    if time - Ensemble_fleche[last_fleche].time_start >= (1 - Upgrade_arc["cadence"])*1000:
        creation(WIDTH, HEIGHT, 0, SCREEN, mouse_pos, time, Ensemble_fleche, Upgrade_arc)
    return False


