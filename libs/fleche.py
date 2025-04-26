import math
import pygame


class Fleche:
    def __init__(self, WIDTH, HEIGHT, angle, mouse_pos, time, SCREEN):
        self.time_start = time
        self.time = 0
        self.x_end = mouse_pos[0]
        self.y_end = mouse_pos[1]
        self.gravity = 300
        self.angle = angle  # angle en radians
        self.x_init = WIDTH // 8
        self.y_init = HEIGHT // 4
        self.x = self.x_init
        self.y = self.y_init
        self.screen = SCREEN
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.damage = 1000

        # Distance de base (sans angle)
        distance_point_arrive = math.sqrt((self.x_end - self.x_init) ** 2 + (self.y_end - self.y_init) ** 2)
        self.temps_arrive = max(0.1, distance_point_arrive / 300)

        # Calculer la direction de base
        direction_x = self.x_end - self.x_init
        direction_y = self.y_end - self.y_init

        # Normaliser le vecteur de direction
        longueur = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if longueur > 0:
            direction_x /= longueur
            direction_y /= longueur

        # Appliquer la rotation en fonction de l'angle
        vitesse = distance_point_arrive / self.temps_arrive
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        # Calculer les nouvelles composantes de vitesse avec l'angle
        self.vx = vitesse * (direction_x * cos_angle - direction_y * sin_angle)
        self.vy = vitesse * (direction_x * sin_angle + direction_y * cos_angle)
    def position(self, time):
        self.time = (time - self.time_start) / 1000  # Convertir le temps en secondes
        if self.time >= 0:
            self.x = self.x_init + self.vx * self.time
            self.y = self.y_init + self.vy * self.time + 0.5 * self.gravity * self.time ** 2
        self.rect.x = self.x
        self.rect.y = self.y
        return self.y >= self.screen.get_height() - 5  # Retourne si la flèche est hors de l'écran

def dead_fleche(enemys,Ensemble_fleche):
    for ennemy in enemys:  # On copie la liste pour éviter les conflits
        for fleche in Ensemble_fleche:
            if fleche.rect.colliderect(ennemy.rect):
                Ensemble_fleche.remove(fleche)
                ennemy.hitbox(1000)
                if ennemy.est_mort():
                    enemys.remove(ennemy)

def draw(SCREEN,time,Ensemble_fleche):
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




