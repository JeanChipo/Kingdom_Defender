import math
import pygame
class Fleche:
    def __init__(self, WIDTH, HEIGHT, mouse_pos, time, SCREEN):
        self.time_start = time
        self.time = 0
        self.x_end = mouse_pos[0]
        self.y_end = mouse_pos[1]
        self.gravity = 300  # Augmenter pour un effet plus réaliste
        self.angle = math.radians(-45)  # Convertir directement en radians
        self.x_init = WIDTH // 8
        self.y_init = HEIGHT // 4
        self.x = self.x_init
        self.y = self.y_init
        self.screen = SCREEN
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.damage = 1000
        # Calcule de la distance entre le point de départ et le point d'arrivée
        distance_point_arrive = math.sqrt((self.x_end - self.x_init) ** 2 + (self.y_end - self.y_init) ** 2)

        # Calcul du temps d'arrivée basé sur la distance (arbitrairement divisé par 300 pour équilibrer)
        self.temps_arrive = max(0.1, distance_point_arrive / 300)

        # Calcul des vitesses initiales
        self.vx = (self.x_end - self.x_init) / self.temps_arrive
        self.vy = (self.y_end - self.y_init) / self.temps_arrive - 0.5 * self.gravity * self.temps_arrive

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

def cadence(Ensemble_fleche, upgrade, mouse_pos, time, WIDTH, HEIGHT, SCREEN):
    # Si la liste est vide
    if len(Ensemble_fleche) == 0:
        # Ajoute la première flèche
        Ensemble_fleche.append(Fleche(WIDTH, HEIGHT, mouse_pos, time, SCREEN))
        # Ajoute la deuxième flèche avec un délai de 200ms
        Ensemble_fleche.append(Fleche(WIDTH, HEIGHT, mouse_pos, time + 200, SCREEN))
        return True

    # Vérifie le temps écoulé depuis l'avant-dernière flèche (première flèche de la dernière salve)
    if len(Ensemble_fleche) >= 2:
        last_salve_time = Ensemble_fleche[-2].time_start
        if time - last_salve_time >= upgrade:
            # Ajoute une nouvelle salve de deux flèches
            Ensemble_fleche.append(Fleche(WIDTH, HEIGHT, mouse_pos, time, SCREEN))
            Ensemble_fleche.append(Fleche(WIDTH, HEIGHT, mouse_pos, time + 200, SCREEN))
            return True
    else:
        # Si on n'a qu'une seule flèche, on vérifie par rapport à celle-ci
        if time - Ensemble_fleche[-1].time_start >= upgrade:
            Ensemble_fleche.append(Fleche(WIDTH, HEIGHT, mouse_pos, time, SCREEN))
            Ensemble_fleche.append(Fleche(WIDTH, HEIGHT, mouse_pos, time + 200, SCREEN))
            return True

    return False


