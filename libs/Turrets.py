from libs.models import*


class Turret_Gestion:
    def __init__(self):
        self.turrets = [Turret()]

    def add_turret(self):
        self.turrets.append(Turret())

    def update(self):
        for turret in self.turrets:
            turret.update()

    def draw(self, window, WIDTH):
        for turret in self.turrets:
            turret.draw(window, WIDTH)

    def run(self, window, WIDTH):
        self.update()
        self.draw(window, WIDTH)

class Turret:
    def __init__(self):
        self.x = 40
        self.y = 160
        self.name = "Basic"
        self.width = 50
        self.height = 25
        self.turret = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullet = []
        self.damage = 10
        self.upgrade = []
        self.level = 1
        self.fire_rate = 10
        self.time = 0

    def update(self):
        self.time += 1
        self.firing()
        for b in self.bullet:
            b.update()
        self.bullet = [b for b in self.bullet if b.x <= 800]  # 800 = screen width, TO REPLACE

    def firing(self):
        if self.time % self.fire_rate == 0:
            self.bullet.append(Bullet(self.x + self.width + 60, self.y + self.height + 120 // 2, self.damage))

    def draw(self, screen, dist):
        screen.blit(pygame.transform.rotate(turret_model, -40.0), (self.x, self.y))
        for b in self.bullet:
            b.draw(screen)

    def get_bullet(self):
        return [b.bullet for b in self.bullet]


class Bullet:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = 10
        self.width = 10
        self.height = 10
        self.bullet = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += self.speed
        self.bullet.move_ip(self.speed, 0)


    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.bullet)
