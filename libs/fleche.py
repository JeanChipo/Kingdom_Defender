import math
import pygame



class Fleche:
    def __init__(self, WIDTH, HEIGHT,RATIO_W, RATIO_H,vitesse_plus, mouse_pos, time, SCREEN):
        self.time_start = time
        self.time = 0
        self.x_end = mouse_pos[0]
        self.y_end = mouse_pos[1]
        self.gravity = 300
        self.x_init = WIDTH // 8
        self.y_init = HEIGHT // 4
        self.x = self.x_init
        self.y = self.y_init
        self.screen = SCREEN
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.damage = 1000

        # Calcule de la distance entre le point de départ et le point d'arrivée
        distance_point_arrive = math.sqrt(((self.x_end - self.x_init) / RATIO_W) ** 2 + ((self.y_end - self.y_init) / RATIO_H) ** 2)

        # Calcul du temps d'arrivée basé sur la distance (arbitrairement divisé par 300 pour équilibrer)
        self.temps_arrive = max(0.1, distance_point_arrive / 300)

        # Calcul des vitesses initiales
        self.vx = ((self.x_end - self.x_init) / self.temps_arrive) + vitesse_plus
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
                    if ennemy in enemys:
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


def creation(WIDTH, HEIGHT,RATIO_W, RATIO_H, SCREEN, mouse_pos, time, Ensemble_fleche, Upgrade_arc):
    for i in range(Upgrade_arc["salve"]):
        for l in range(len(Upgrade_arc["dispersion"])):
            vitesse_plus = Upgrade_arc["dispersion"][l]  # Convertit ch aque angle de dispersion en radians
            fleche = Fleche(WIDTH, HEIGHT,RATIO_W, RATIO_H,vitesse_plus, mouse_pos, time + i*200, SCREEN)  # délai entre les fléches de la salve (0,2sec) grâce à i*200
            Ensemble_fleche.append(fleche)

def cadence(Ensemble_fleche,RATIO_W, RATIO_H, upgrade, mouse_pos, time, WIDTH, HEIGHT, SCREEN, Upgrade_arc):
    # Si la liste est vide
    if len(Ensemble_fleche) == 0:
        creation(WIDTH, HEIGHT,RATIO_W, RATIO_H, SCREEN, mouse_pos, time, Ensemble_fleche, Upgrade_arc)
        return True

    # Vérifie le temps écoulé depuis la dernière flèche
    last_fleche = len(Ensemble_fleche) - 1  # Index de la dernière flèche
    if time - Ensemble_fleche[last_fleche].time_start >= (1 - Upgrade_arc["cadence"])*1000:
        creation(WIDTH, HEIGHT, RATIO_W, RATIO_H, SCREEN, mouse_pos, time, Ensemble_fleche, Upgrade_arc)
    return False

def upgrade_cadence(gold, Upgrade_arc, manager):
    if Upgrade_arc["cadence"] <=3 and gold >= 100 +Upgrade_arc["cadence"]*100: # Permet d'avoir une préogressioon linéaire du coût des améliorations
        Upgrade_arc["cadence"] += 0.5
        gold -= 100 + Upgrade_arc["cadence"] * 100
        print(Upgrade_arc["cadence"])
    else:
        manager.show_text("error pas assez d'argent ou trop de palier monté", 2)
    return gold, Upgrade_arc

def upgrade_salve(gold, Upgrade_arc, manager):
    if Upgrade_arc["salve"] <=3 and gold >= 100 +Upgrade_arc["salve"]*100:
        Upgrade_arc["salve"] += 1
        gold -= 100 + Upgrade_arc["salve"] * 100
    else:
        manager.show_text("error pas assez d'argent ou trop de palier monté", 2)
    return gold, Upgrade_arc

def upgrade_dispersion(gold, Upgrade_arc, manager):
    if len(Upgrade_arc["dispersion"]) <= 9 and gold >= 100 + len(
            Upgrade_arc["dispersion"]) * 100:
        min_vitesse = min(Upgrade_arc["dispersion"])
        max_vitesse = max(Upgrade_arc["dispersion"])
        Upgrade_arc["dispersion"].extend([min_vitesse - 15, max_vitesse + 15])  # Ajoute deux nouveaux angles
        Upgrade_arc["dispersion"].sort()  # Trie la liste
        gold -= 100 + len(Upgrade_arc["dispersion"]) * 100
        print(Upgrade_arc["dispersion"])
    else:
        manager.show_text("error pas assez d'argent ou trop de palier monté", 2)
    return gold, Upgrade_arc
