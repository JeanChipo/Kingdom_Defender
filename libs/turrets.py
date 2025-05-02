from libs.display import height_ratio
from libs.models import*
import math
import pygame.transform


class Turret_Gestion:
    def __init__(self):
        self.turrets = []
        self.nb_turret=-1
        self.pos = [(40,300),(40,260),(40,360)]
        self.add_turret()


    def add_turret(self):
        self.nb_turret += 1
        if self.nb_turret >= 3:
            return
        self.turrets.append(Turret(self.pos[self.nb_turret]))

    def upgrade_turrets(self):
        for turret in self.turrets:
            turret.upgrade()


    def update(self, enemys, WIDTH):
        for turret in self.turrets:
            turret.update(enemys, WIDTH)

    def draw(self, window, WIDTH, HEIGHT,enemys):
        for turret in self.turrets:
            turret.draw(window, WIDTH, HEIGHT,enemys)

    def run(self, window, WIDTH):
        self.update()
        self.draw(window, WIDTH)

    def update_positions(self, WIDTH, HEIGHT):
        for turret in self.turrets:
            turret.x = turret.x_stable * WIDTH / 800
            turret.y = turret.y_stable * HEIGHT / 600
            turret.turret = pygame.Rect(turret.x, turret.y, turret.width, turret.height)


class Turret:
    def __init__(self, pos):
        self.x, self.y = pos
        self.x_stable, self.y_stable = pos[0], pos[1]
        self.name = "Basic"
        self.width = 50
        self.height = 25
        self.turret = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullets = []
        self.damage = 1000
        self.upgrades = {1 : {"name" : "Basic", "damage" : 1000, "bullet_penetration" : 1, "fire_rate" : 10, "bullet_size_x" : 10, "bullet_size_y" : 10},
                        2 : {"name" : "Canon", "damage" : 5000, "bullet_penetration" : 1, "fire_rate" : 15, "bullet_size_x" : 20, "bullet_size_y" : 20},
                        3 : {"name" : "Lance", "damage" : 5000, "bullet_penetration" : 1, "fire_rate" : 10, "bullet_size_x" : 10, "bullet_size_y" : 10},
                        4 : {"name" : "Minigun", "damage" : 100, "bullet_penetration" : 100, "fire_rate" : 1, "bullet_size_x" : 10, "bullet_size_y" : 10}}
        self.level = 1
        self.bullet_penetration = 1
        self.fire_rate = 10
        self.bullet_size_x = 10
        self.bullet_size_y = 10
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
        return ennemi.futur(60, WIDTH)  # 60 frames = 1 seconde si 60 FPS

    def upgrade(self):
        self.level += 1 if self.level < 4 else 0
        self.name = self.upgrades[self.level]["name"]
        self.damage = self.upgrades[self.level]["damage"]
        self.fire_rate = self.upgrades[self.level]["fire_rate"]
        self.bullet_penetration = self.upgrades[self.level]["bullet_penetration"]
        self.bullet_size_x = self.upgrades[self.level]["bullet_size_x"]
        self.bullet_size_y = self.upgrades[self.level]["bullet_size_y"]


    def get_bullet(self):
        return [elm.bullet for elm in self.bullets]

    def firing(self, pos, WIDTH):
        if pos == (0,0): return
        X, Y = pos
        if self.time % self.fire_rate == 0:
            dir_x = X - self.x
            dir_y = Y - self.y
            time_to_target = 1.0  # secondes
            fps = 60
            frames = time_to_target * fps
            speedx = dir_x / frames
            speedy = dir_y / frames
            self.bullets.append(Bullet(
                self.x + self.width,
                self.y + self.height*2,
                speedx, speedy,
                self.damage, self.bullet_penetration,
                self.bullet_size_x, self.bullet_size_y
            ))

    def draw(self, screen, X, Y, enemys):
        x, y = self.get_first_enemy_pos(enemys, Y)
        if enemys:
            rotated_baliste= pygame.transform.rotate(baliste,math.degrees(math.atan(x/y)-135))
            screen.blit(pygame.transform.scale(rotated_baliste,(100*height_ratio(),100*height_ratio())),(self.x, self.y))
        for elm in self.bullets:
            elm.draw(screen)
        self.bullets = [elm for elm in self.bullets if (elm.x <= X and elm.y <= Y-300 and not elm.dead_bullet(enemys))]


class Bullet:
    def __init__(self, x, y, speedx, speedy, damage, penetration, size_x, size_y):
        self.x = x
        self.y = y
        self.damage = damage
        self.speedx = speedx
        self.speedy = speedy
        self.penetration = penetration
        self.width = size_x
        self.height = size_y
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
