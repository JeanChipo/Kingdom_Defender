from pygame.examples.moveit import HEIGHT
from libs.display import height_ratio
from libs.models import*
import math

class Turret_Gestion:
    def __init__(self):
        self.turrets = []
        self.nb_turret=-1
        self.pos = [(40,300),(40,260),(40,360)]
        self.add_turret()
        self.selected_turret = None


    def add_turret(self):
        self.nb_turret += 1
        if self.nb_turret >= 3:
            return
        self.turrets.append(Turret(self.pos[self.nb_turret]))

    def select_turret(self, mouse_pos):
        for turret in self.turrets:
            if turret.turret.collidepoint(mouse_pos):
                self.selected_turret = turret
                print(f"Tourelle sélectionnée : {turret.name}")
                return
        self.selected_turret = None

    def upgrade_turrets(self, path):
        if self.selected_turret is None:
            return
        self.selected_turret.upgrade(path)

    def change_priorities(self, priorities):
        if self.selected_turret is None:
            return
        self.selected_turret.priority = priorities

    def update(self, enemys, WIDTH, HEIGHT):
        for turret in self.turrets:
            turret.update(enemys, WIDTH, HEIGHT)

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
        self.name = "Unupgraded"
        self.width = 100
        self.height = 100
        self.turret = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullets = []
        self.damage = 1000
        self.upgrades = {"speed" : {1: {"name": "Standard", "damage": 500, "bullet_penetration": 1, "fire_rate": 10, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 120},
                                    2: {"name": "Rapide", "damage": 400, "bullet_penetration": 1, "fire_rate": 7, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 120},
                                    3: {"name": "Minigun", "damage": 300, "bullet_penetration": 2, "fire_rate": 4, "bullet_size_x": 8, "bullet_size_y": 8, "bullet_lifetime": 120},
                                    4: {"name": "Fusil Laser", "damage": 200, "bullet_penetration": 3, "fire_rate": 2, "bullet_size_x": 6, "bullet_size_y": 6, "bullet_lifetime": 120}},

                        "bullet" : {1: {"name": "Basic", "damage": 1000, "bullet_penetration": 1, "fire_rate": 10, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 120},
                                    2: {"name": "Gros Boulet", "damage": 1500, "bullet_penetration": 1, "fire_rate": 12, "bullet_size_x": 20, "bullet_size_y": 20, "bullet_lifetime": 120},
                                    3: {"name": "Mega Boulet", "damage": 2000, "bullet_penetration": 2, "fire_rate": 14, "bullet_size_x": 30, "bullet_size_y": 30, "bullet_lifetime": 120},
                                    4: {"name": "God Boulet", "damage": 3000, "bullet_penetration": 3, "fire_rate": 16, "bullet_size_x": 40,"bullet_size_y": 40, "bullet_lifetime": 120}},

                        "special" : {   1: {"name": "Explosif", "damage": 1200, "bullet_penetration": 1, "fire_rate": 10, "bullet_size_x": 15, "bullet_size_y": 15, "bullet_lifetime": 120, "explosive": True},
                                        2: {"name": "Perforant", "damage": 800, "bullet_penetration": 5, "fire_rate": 9, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 120},
                                        3: {"name": "Persistant", "damage": 700, "bullet_penetration": 1, "fire_rate": 10, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 400},
                                        4: {"name": "Ricochet", "damage": 900, "bullet_penetration": 2, "fire_rate": 5, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 500, "bounces": 3}}
                         }
        self.level = 0
        self.bullet_penetration = 1
        self.fire_rate = 10
        self.bullet_size_x = 10
        self.bullet_size_y = 10
        self.bullet_lifetime = 120
        self.priority = "petit"
        self.explosive = False
        self.bounces = 0
        self.path = None
        self.time = 0

    def update(self, enemys, WIDTH, HEIGHT):
        self.time += 1
        self.firing(self.get_first_enemy_pos(enemys, WIDTH), WIDTH)
        for elm in self.bullets:
            elm.update(WIDTH, HEIGHT)

    def select_type(self, enemys):
        for elm in enemys:
            if elm.name == self.priority: return elm
        return enemys[0]


    def get_first_enemy_pos(self, enemys, WIDTH):
        if not enemys:
            return (0, 0)
        ennemi = self.select_type(enemys)
        return ennemi.futur(60, WIDTH)

    def choose_path(self, path):
        if self.path is None:
            self.path = path
        return


    def upgrade(self, path):
        if self.level >= 4:
            return
        self.choose_path(path)
        self.level += 1
        self.name = self.upgrades[self.path][self.level]["name"]
        self.bullet_penetration = self.upgrades[self.path][self.level]["bullet_penetration"]
        self.fire_rate = self.upgrades[self.path][self.level]["fire_rate"]
        self.bullet_size_x = self.upgrades[self.path][self.level]["bullet_size_x"]
        self.bullet_size_y = self.upgrades[self.path][self.level]["bullet_size_y"]
        self.bullet_lifetime = self.upgrades[self.path][self.level]["bullet_lifetime"]
        self.damage = self.upgrades[self.path][self.level]["damage"]
        if "explosive" in self.upgrades[self.path][self.level]:
            self.explosive = self.upgrades[self.path][self.level]["explosive"]
        if "bounces" in self.upgrades[self.path][self.level]:
            self.bounces = self.upgrades[self.path][self.level]["bounces"]


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
                self.x + self.width/2,
                self.y + self.height/2,
                speedx, speedy,
                self.damage, self.bullet_penetration,
                self.bullet_size_x, self.bullet_size_y, self.bullet_lifetime,
                self.explosive, self.bounces
            ))

    def draw(self, screen, X, Y, enemys):
        x, y = self.get_first_enemy_pos(enemys, Y)
        if enemys:
            rotated_baliste= pygame.transform.rotate(baliste,math.degrees(math.atan(x/y)-135))
            screen.blit(pygame.transform.scale(rotated_baliste,(100*height_ratio(),100*height_ratio())),(self.x, self.y))
        for elm in self.bullets:
            elm.draw(screen)
        self.bullets = [elm for elm in self.bullets if (elm.x <= X and elm.y <= Y-300 and not elm.dead_bullet(enemys) and elm.time < elm.lifetime)]


class Bullet:
    def __init__(self, x, y, speedx, speedy, damage, penetration, size_x, size_y, lifetime, explosive, bounces):
        self.x = x
        self.y = y
        self.damage = damage
        self.speedx = speedx
        self.speedy = speedy
        self.penetration = penetration
        self.width = size_x
        self.height = size_y
        self.bullet = pygame.Rect(self.x, self.y, self.width, self.height)
        self.time = 0
        self.lifetime = lifetime
        self.explosive = explosive
        self.bounces = bounces

    def update(self, WIDTH, HEIGHT):
        self.time += 1
        self.x += self.speedx
        self.y += self.speedy
        self.bullet.x = int(self.x)
        self.bullet.y = int(self.y)
        screen_width, screen_height = WIDTH, HEIGHT
        if self.bounces > 0:
            if self.bullet.left <= 0 or self.bullet.right >= screen_width:
                self.speedx *= -1
                self.bounces -= 1
                if self.bullet.right >= screen_width:
                    self.bullet.right = screen_width - 10
            if self.bullet.top <= 0 or self.bullet.bottom >= screen_height -100:
                self.speedy *= -1
                self.bounces -= 1
                if self.bullet.bottom >= screen_height - 100:
                    self.bullet.bottom = screen_height - 110

    def dead_bullet(self, enemys):
        hits = 0
        for ennemy in enemys[:]:
            if self.bullet.colliderect(ennemy.rect):
                if self.explosive:
                    radius = 50
                    for target in enemys[:]:
                        dx = target.rect.centerx - self.bullet.centerx
                        dy = target.rect.centery - self.bullet.centery
                        if dx ** 2 + dy ** 2 <= radius ** 2:
                            target.hitbox(self.damage)
                            if target.est_mort():
                                enemys.remove(target)
                else:
                    ennemy.hitbox(self.damage)
                    if ennemy.est_mort():
                        enemys.remove(ennemy)
                self.penetration -= 1
                if self.penetration <= 0:
                    return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.bullet)
