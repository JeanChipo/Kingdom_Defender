import math
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
        return self.y >= self.screen.get_height() - 5  # Retourne si la flèche est hors de l'écran