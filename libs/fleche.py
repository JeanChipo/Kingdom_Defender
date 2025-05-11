import math
import pygame
from libs.display import *
from libs.ui import TimedTextManager
from libs.turrets import *

""" Classe qui regroupe les informations d'une fléche tirée """
class Fleche:
    def __init__(self, middle_x, middle_y,RATIO_W, RATIO_H,vitesse_plus, mouse_pos, time, SCREEN):

        # Initilisation des variables

        # Attributs temporels
        self.time_start = time #Temps interne au jeu au moment de la création
        self.time = 0 #Temps écoulé depuis la création

        # Positions finales
        self.x_end = mouse_pos[0]
        self.y_end = mouse_pos[1]

        # Paramétre physique
        self.gravity = 300 #Equilibré pour le jeu (pas en proportion à la réalité/axe de progression

        # Positions initiales (ajustés par rapport aux améliorations de la tour)
        self.x_init = middle_x
        self.y_init = middle_y

        # Mise à jour des coordonnées de la fléche
        self.x = self.x_init
        self.y = self.y_init

        # Paramétre de rendu
        self.screen = SCREEN #(potentiellement effaçable pour une variable non local à une fléche)
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.damage = 1000

        # Partie calculatoire de la vitesse initiale

        # Calcule de la distance entre le point de départ et le point d'arrivée
        distance_point_arrive = math.sqrt(((self.x_end - self.x_init) / RATIO_W) ** 2 + ((self.y_end - self.y_init) / RATIO_H) ** 2)

        # Calcul du temps d'arrivée basé sur la distance (arbitrairement divisé par 300 pour équilibrer)
        self.temps_arrive = max(0.1, distance_point_arrive / 300)

        # Calcul des vitesses initiales
        self.vx = ((self.x_end - self.x_init) / self.temps_arrive) + vitesse_plus
        self.vy = (self.y_end - self.y_init) / self.temps_arrive - 0.5 * self.gravity * self.temps_arrive

    """ Calcule les nouvelles positions (coordonnées et hit box) de la fléche """
    def position(self, time):

        # Convertir le temps en secondes
        self.time = (time - self.time_start) / 1000

        # Calcule de la mise à jour des coordonnées
        if self.time >= 0:
            self.x = self.x_init + self.vx * self.time
            self.y = self.y_init + self.vy * self.time + 0.5 * self.gravity * self.time ** 2

        # Mise à jour des coordonnées de la hitbox de la fléche
        self.rect.x = self.x
        self.rect.y = self.y

        return self.y >= self.screen.get_height() - 5  # Retourne si la flèche est hors de l'écran
""" Calcule de la position inital de la flèche par rapport à la tour """
def initial_position(tower_level):
    middle_x = 50 * width_ratio() + 55 * height_ratio()
    middle_y = SCREEN.get_height() - tower_height_position(tower_level) * height_ratio() + 125 * height_ratio()
    return middle_x, middle_y

""" Vérifie les collisions avec les ennemies et qui met à jour leur statue si besoins """
def dead_fleche(enemys,Ensemble_fleche):

    # Parcourt la liste de chaque ennemie et de chaque fleche

    for ennemy in enemys:  # On copie la liste pour éviter les conflits
        for fleche in Ensemble_fleche:

            # Verifie les collisions
            if fleche.rect.colliderect(ennemy.rect):
                # Supprime la fléche si collision (axe amélioration, fléche perforante)
                Ensemble_fleche.remove(fleche)
                ennemy.hitbox(fleche.damage)
                #Verifie si l'ennemi est mort et réagie en conséquence
                if ennemy.est_mort():
                    if ennemy in enemys:
                        enemys.remove(ennemy)

old_x = 0
old_y = 0

""" Fonction qui permet l'affichage des fleches """
def draw(SCREEN,time,Ensemble_fleche):

    # Parcours les flèches existantes
    for fleche in Ensemble_fleche:

        if not fleche.position(time):
            # Dessiner les flèches de la liste
            global old_x
            global old_y
            temp_arrow = resize_fleche(arrow)
            arrow_rect = arrow.get_rect(center=((int(fleche.x), int(fleche.y))))
            if old_x==0:
                SCREEN.blit(temp_arrow,arrow_rect)
                old_x = fleche.x
                old_y = fleche.y
            else :
                opp = fleche.y - old_y+1
                adj = old_x+1 - fleche.x
                rotated_arrow = pygame.transform.rotate(temp_arrow, math.degrees(math.atan(opp / adj)))
                rotated_rect = rotated_arrow.get_rect(center=arrow_rect.center)
                SCREEN.blit((rotated_arrow), (rotated_rect))

        else:
            # Supprimer la flèche qui sort de l'écran
            Ensemble_fleche.remove(fleche)

""" Creation/initialisation des fleches"""
def creation(tower_level,RATIO_W, RATIO_H, SCREEN, mouse_pos, time, Ensemble_fleche, Upgrade_arc):
    middle_x, middle_y = initial_position(tower_level)
    # Crée le nombre de fléche automatiquement selon les améliorations
    for i in range(Upgrade_arc["salve"]):
        for l in range(len(Upgrade_arc["dispersion"])):
            # Prend en compte des améliorations pour faire varier les caractéristique des fléches (ici la vitesse horizontal inial)
            vitesse_plus = Upgrade_arc["dispersion"][l]
            # Délai entre les fléches de la salve (0,2sec) grâce à i*200
            fleche = Fleche(middle_x, middle_y,RATIO_W, RATIO_H,vitesse_plus, mouse_pos, time + i*200, SCREEN)
            # Ajoue de la fléche nouvellement crée dans un tableau
            Ensemble_fleche.append(fleche)

""" Gére le delai entre la création de chaque fléche (propre à l'amélioration cadence) """
def cadence(tower_level,Ensemble_fleche,RATIO_W, RATIO_H, mouse_pos, time, SCREEN, Upgrade_arc):

    # Si la liste est vide (cas particulier car sinon recherche d'une fléche précédente alors qu'elle n'existe pas)
    if len(Ensemble_fleche) == 0:
        creation(tower_level,RATIO_W, RATIO_H, SCREEN, mouse_pos, time, Ensemble_fleche, Upgrade_arc)
        return True

    # Vérifie le temps écoulé depuis la dernière flèche
    last_fleche = len(Ensemble_fleche) - 1  # Index de la dernière flèche
    if time - Ensemble_fleche[last_fleche].time_start >= (1 - Upgrade_arc["cadence"])*1000: # *1000 pour la conversion du des milliseconde en seconde
        creation(tower_level, RATIO_W, RATIO_H, SCREEN, mouse_pos, time, Ensemble_fleche, Upgrade_arc)
    return False

"""______________Fonctions qui gérent les améliorations des fléches______________"""

# Condition pour amélioration : économique et pas trop d'amélioration
# Schéma de d'amélioration : - Verification du nombre d'amélioration de la fléche puis l'économie actuel avec le prix
#                            - Si amélioration possible, amélioration de la compétence et soustraction de l'économie par le prix
#                            - Mise à jour du prix d'amélioration de la compétence
#                            - Renvoie si possible le signal qui rend impossible l'amélioration de la compétence
def upgrade_cadence(gold, Upgrade_arc, manager):
    if Upgrade_arc["cadence"] < 3 and gold >= 5000 + Upgrade_arc["cadence"] * 1000: # Permet d'avoir une préogressioon linéaire du coût des améliorations
        Upgrade_arc["cadence"] += 0.25
        gold -= 5000 + Upgrade_arc["cadence"] * 1000


        if Upgrade_arc["cadence"] < 3:
            Upgrade_arc["prices_upgrade"][0] = 5000 + Upgrade_arc["cadence"] * 1000
        else:
            Upgrade_arc["prices_upgrade"][0] = 1


    return int(gold), Upgrade_arc

def upgrade_salve(gold, Upgrade_arc, manager):
    if Upgrade_arc["salve"] < 3 and gold >= 5000 + Upgrade_arc["salve"] * 1000:
        gold -= 5000 + Upgrade_arc["salve"] * 1000
        Upgrade_arc["salve"] += 1


        if Upgrade_arc["salve"] < 3:
            Upgrade_arc["prices_upgrade"][1] = 5000 + Upgrade_arc["salve"] * 1000
        else:
            Upgrade_arc["prices_upgrade"][1] = 1


    return int(gold), Upgrade_arc

def upgrade_dispersion(gold, Upgrade_arc, manager):
    if len(Upgrade_arc["dispersion"]) < 7 and gold >= 5000 + len(Upgrade_arc["dispersion"]) * 1000:

        # Prise de la plus petite valeur et de la plus grande
        min_vitesse = min(Upgrade_arc["dispersion"])
        max_vitesse = max(Upgrade_arc["dispersion"])

        gold -= 5000 + len(Upgrade_arc["dispersion"]) * 1000


        # Ajout d'une valeur arbitraire au valeur extreme de la dispertion existante
        Upgrade_arc["dispersion"].extend([min_vitesse - 50, max_vitesse + 50])
        Upgrade_arc["dispersion"].sort()  # Trie la liste

        if len(Upgrade_arc["dispersion"]) < 7 :
            Upgrade_arc["prices_upgrade"][2] = 5000 + len(Upgrade_arc["dispersion"]) * 1000
        else:
            Upgrade_arc["prices_upgrade"][2] = 1

    return int(gold), Upgrade_arc
