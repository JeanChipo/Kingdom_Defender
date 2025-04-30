from libs.models import*


class Turret_Gestion:
    def __init__(self):
        self.turrets = [Turret()]

    def add_turret(self):
        self.turrets.append(Turret())

    def update(self, enemys, WIDTH):
        for turret in self.turrets:
            turret.update(enemys, WIDTH)

    def draw(self, window, WIDTH, HEIGHT,enemys):
        for turret in self.turrets:
            turret.draw(window, WIDTH, HEIGHT,enemys)

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
        self.bullets = []
        self.damage = 1000
        self.upgrades = {1 : {"name" : "Basic", "damage" : 1000, "bullet_penetration" : 1, "fire_rate" : 10},
                        2 : {"name" : "Canon", "damage" : 5000, "bullet_penetration" : 1, "fire_rate" : 15},
                        3 : {"name" : "Lance", "damage" : 5000, "bullet_penetration" : 1, "fire_rate" : 10},
                        4 : {"name" : "Laser", "damage" : 100, "bullet_penetration" : 100, "fire_rate" : 1}}
        self.level = 1
        self.bullet_penetration = 1
        self.fire_rate = 10
        self.time = 0

    def update(self, enemys, WIDTH):
        self.time += 1
        self.firing(self.get_first_enemy_pos(enemys, WIDTH), WIDTH)
        for elm in self.bullets:
            elm.update()

    def get_first_enemy_pos(self, enemys, WIDTH):
        if not enemys:
            return (0, 0)

        ennemi = enemys[0]

        # Si l'ennemi est à l'arrêt (il ne va plus bouger), on vise sa position actuelle
        if ennemi.rect.x <= WIDTH / 10:
            print("on tire la !")
            return -ennemi.rect.x, ennemi.rect.y
        dx = ennemi.rect.x - self.x
        dy = ennemi.rect.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        vitesse_bullet = 10
        t = distance / vitesse_bullet
        ratio_future = max(ennemi.ratio - ennemi.speed * t, 0)
        future_x = (WIDTH * ratio_future) / 10000
        return future_x, ennemi.rect.y

    def upgrade(self):
        self.level += 1 if self.level < 4 else 0
        self.name = self.upgrades[self.level]["name"]
        self.damage = self.upgrades[self.level]["damage"]
        self.fire_rate = self.upgrades[self.level]["fire_rate"]
        self.bullet_penetration = self.upgrades[self.level]["bullet_penetration"]


    def get_bullet(self):
        return [elm.bullet for elm in self.bullets]

    def firing(self, pos, WIDTH):
        X, Y = pos
        if self.time % self.fire_rate == 0:
            dir_x = X - self.x
            dir_y = Y - self.y
            print(dir_x)
            magnitude = (dir_x ** 2 + dir_y ** 2) ** 0.5 or 1
            bullet_speed = 7
            speedx = bullet_speed * dir_x / magnitude
            speedy = bullet_speed * dir_y / magnitude
            self.bullets.append(Bullet(
                self.x + self.width + 80,
                self.y + self.height + 120 // 2,
                speedx, speedy,
                self.damage, self.bullet_penetration
            ))

    def draw(self, screen, X, Y, enemys):
        screen.blit(pygame.transform.rotate(turret_model,-40.0), (self.x, self.y))
        for elm in self.bullets:
            elm.draw(screen)
        self.bullets = [elm for elm in self.bullets if (elm.x <= X and elm.y <= Y-300 and not elm.dead_bullet(enemys))]


class Bullet:
    def __init__(self, x, y, speedx, speedy, damage, penetration):
        self.x = x
        self.y = y
        self.damage = damage
        self.speedx = speedx
        self.speedy = speedy
        self.penetration = penetration
        self.width = 10
        self.height = 10
        self.bullet = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += self.speedx
        self.y += self.speedy
        self.bullet.x = int(self.x)
        self.bullet.y = int(self.y)

    def dead_bullet(self, enemys):
        hits = 0
        for ennemy in enemys[:]:  # On copie la liste pour éviter les conflits
            if self.bullet.colliderect(ennemy.rect):
                ennemy.hitbox(self.damage)
                hits += 1
                if ennemy.est_mort():
                    enemys.remove(ennemy)
                self.penetration -= 1
                if self.penetration <= 0:
                    return True  # La balle est morte
        return False  # La balle continue

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.bullet)
