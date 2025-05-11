import math

from libs.display import *
from libs.enemy import Enemy
from libs.models import *
from libs.ui import TimedTextManager



class Turret_Gestion:
    def __init__(self, gain_gold):
        """module permettant de gerer les tourrelles en court d'activité"""
        self.turrets = []
        self.nb_turret=-1
        self.pos = [(20*width_ratio()+22*height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+165*height_ratio()),(20*width_ratio()+22*height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+100*height_ratio()),(20*width_ratio()+22*height_ratio(),SCREEN.get_height() - tower_height_position(tower_level) * height_ratio()+35*height_ratio())]
        self.gain_gold = gain_gold
        self.add_turret()
        self.selected_turret = None

    def add_turret(self):
        """ajoute une tourelle"""
        self.nb_turret += 1
        if self.nb_turret >= 3: #empêche plus de 3 tourelle
            return
        self.turrets.append(Turret(self.pos[self.nb_turret], self.gain_gold))

    def select_turret(self, mouse_pos: (float, float), manager: TimedTextManager):
        """selectionne une tourelle en cliquant dessus"""
        for turret in self.turrets:
            if turret.turret.collidepoint(mouse_pos): # vérification de hitbox
                self.selected_turret = turret
                manager.show_text(f"Selected Turret : {self.selected_turret.name}", 2)
                return
        self.selected_turret = None #aucune tourelle selectioné

    def upgrade_turrets(self, path: str, gold: int, manager: TimedTextManager):
        """améliore la tourelle selectioné"""
        if self.selected_turret is None: #si pas de tourelle choisi
            manager.show_text(f"No Turret Selected", 2)
            return
        self.selected_turret.upgrade(path, gold, manager)

    def change_priorities(self, priorities: str):
        """"change l'option de ciblage de la tourelle"""
        if self.selected_turret is None: #si pas de tourelle choisi
            return
        self.selected_turret.priority = priorities

    def update(self, enemys: list[Enemy], WIDTH: int, HEIGHT: int):
        """met a jours les tourelles"""
        for turret in self.turrets:
            turret.update(enemys, WIDTH, HEIGHT)

    def draw(self, window: pygame.Surface, WIDTH: int, HEIGHT: int, enemys: list[Enemy]):
        """affiche les tourelles"""
        for turret in self.turrets:
            turret.draw(window, WIDTH, HEIGHT,enemys)

    def update_positions(self, WIDTH: int, HEIGHT : int):
        """permet de repositioner les tourelles en cas de repositionnement"""
        for turret in self.turrets:
            turret.x = 20*width_ratio()+22*height_ratio()
            turret.y = turret.y_stable * HEIGHT / 600
            turret.turret = pygame.Rect(turret.x, turret.y, turret.width, turret.height)

    def get_next_price(self, path: str) -> int:
        """donne le prix du prochain niveau de la tourelle selectionnée"""
        if self.selected_turret is None: # si pas de tourelle choisi
            return 0
        else:
            if self.selected_turret.path is None:
                return self.selected_turret.upgrades[path][1]["price"]
            elif path != self.selected_turret.path:
                return 1
            else:
                if self.selected_turret.level < 4: # level inférieur a 4
                    return self.selected_turret.upgrades[path][self.selected_turret.level + 1]["price"]
                else: # jusqu'a infini
                    return self.selected_turret.upgrades[path][1]["price"] * (2 ** self.selected_turret.level)


class Turret:
    def __init__(self, pos: tuple[float, float], gain_gold):
        """gere un tourelle"""
        self.x, self.y = pos
        self.gain_gold = gain_gold
        self.x_stable, self.y_stable = pos[0], pos[1]
        self.name = "Unupgraded"
        self.width = 100*height_ratio()
        self.height = 100*height_ratio()
        self.turret = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullets = []
        self.damage = 1000
        self.upgrades = {"speed" : {1: {"name": "Standard", "damage": 1000, "bullet_penetration": 1, "fire_rate": 10, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 120, "price" : 5000},
                                    2: {"name": "Rapide", "damage": 1000, "bullet_penetration": 1, "fire_rate": 7, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 120, "price" : 10000},
                                    3: {"name": "Minigun", "damage": 300, "bullet_penetration": 2, "fire_rate": 4, "bullet_size_x": 8, "bullet_size_y": 8, "bullet_lifetime": 120, "price" : 20000},
                                    4: {"name": "Fusil Laser", "damage": 200, "bullet_penetration": 3, "fire_rate": 2, "bullet_size_x": 6, "bullet_size_y": 6, "bullet_lifetime": 120, "price" : 40000}},

                        "bullet" : {1: {"name": "Basic", "damage": 1000, "bullet_penetration": 1, "fire_rate": 10, "bullet_size_x": 25, "bullet_size_y": 10, "bullet_lifetime": 120, "price" : 5000},
                                    2: {"name": "Gros Boulet", "damage": 1500, "bullet_penetration": 1, "fire_rate": 12, "bullet_size_x": 25, "bullet_size_y": 20, "bullet_lifetime": 120, "price" : 10000},
                                    3: {"name": "Mega Boulet", "damage": 2000, "bullet_penetration": 2, "fire_rate": 14, "bullet_size_x": 30, "bullet_size_y": 30, "bullet_lifetime": 120, "price" : 20000},
                                    4: {"name": "God Boulet", "damage": 3000, "bullet_penetration": 3, "fire_rate": 16, "bullet_size_x": 40,"bullet_size_y": 40, "bullet_lifetime": 120, "price" : 40000}},

                        "special" : {   1: {"name": "Explosif", "damage": 1200, "bullet_penetration": 1, "fire_rate": 10, "bullet_size_x": 15, "bullet_size_y": 15, "bullet_lifetime": 120, "explosive": True, "price" : 5000},
                                        2: {"name": "Perforant", "damage": 800, "bullet_penetration": 5, "fire_rate": 9, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 120, "price" : 10000},
                                        3: {"name": "Persistant", "damage": 700, "bullet_penetration": 1, "fire_rate": 10, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 400, "price" : 20000},
                                        4: {"name": "Ricochet", "damage": 900, "bullet_penetration": 2, "fire_rate": 5, "bullet_size_x": 10, "bullet_size_y": 10, "bullet_lifetime": 500, "bounces": 3, "price" : 40000}}
                        }
        self.level = 0
        self.bullet_penetration = 1
        self.fire_rate = 25
        self.bullet_size_x = 10
        self.bullet_size_y = 10
        self.bullet_lifetime = 180
        self.priority = "petit"
        self.explosive = False
        self.bounces = 0
        self.path = None
        self.time = 0

    def update(self, enemys: list[Enemy], WIDTH: int, HEIGHT: int):
        """met a jours la tourelle"""
        self.time += 1
        self.firing(self.get_first_enemy_pos(enemys, WIDTH), WIDTH)
        for elm in self.bullets:
            elm.update(WIDTH, HEIGHT)

    def select_type(self, enemys: list[Enemy]) -> Enemy:
        """permet de selectionner le premier du type choisi"""
        for elm in enemys: #renvoie le premier ennemi du type choisi
            if elm.name == self.priority: return elm
        return enemys[0] #renvoie le premier ennemi

    def get_first_enemy_pos(self, enemys: list[Enemy], WIDTH: int) -> tuple[float, float]:
        """recupere la position de l'ennemi choisi"""
        if not enemys: #renvoie (0,0) si pas d'ennemi
            return (0, 0)
        ennemi = self.select_type(enemys)
        return ennemi.futur(60, WIDTH)

    def choose_path(self, path: str):
        """choisi un path a la tourelle"""
        if self.path is None:
            self.path = path
        return

    def upgrade(self, path: str, gold, manager: TimedTextManager):
        """permet d'améliorer la tourelle"""
        self.choose_path(path)
        if self.level < 4: # level inférieur a 4
            if self.upgrades[self.path][self.level + 1]["price"] > gold: #vérification or
                manager.show_text(f"Not enough Money", 2)
                return
            self.gain_gold(-self.upgrades[self.path][self.level + 1]["price"])
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
        elif self.path == "speed":
            if self.upgrades[self.path][1]["price"] * (2 ** self.level - 1) > gold:
                manager.show_text(f"Not enough Money", 2)
                return
            self.gain_gold(-(self.upgrades[self.path][1]["price"] * (2 ** self.level - 1)))
            self.level += 1
            self.bullet_penetration *= 2
            self.fire_rate /= 2
            self.damage *= 2
        elif self.path == "bullet":
            if self.upgrades[self.path][1]["price"] * (2 ** self.level - 1) > gold:
                manager.show_text(f"Not enough Money", 2)
                return
            self.gain_gold(-(self.upgrades[self.path][1]["price"] * (2 ** self.level - 1)))
            self.level += 1
            self.bullet_penetration *= 2
            self.damage *= 2
            self.bullet_size_x += 10
            self.bullet_size_y += 10
        elif self.path == "special":
            if self.upgrades[self.path][1]["price"] * (2 ** self.level - 1) > gold:
                manager.show_text(f"Not enough Money", 2)
                return
            self.gain_gold(-(self.upgrades[self.path][1]["price"] * (2 ** self.level - 1)))
            self.level += 1
            self.damage *= 2
            self.bullet_lifetime *= 2
            self.bullet_size_x *= 2



    def get_bullet(self):
        """renvoie la liste des bullets actuel"""
        return [elm.bullet for elm in self.bullets]

    def firing(self, pos: tuple[float, float], WIDTH: float):
        """permet a la tourelle de tirer"""
        if pos == (0,0): return # ne tire pas si pas d'ennemi
        X, Y = pos
        if self.time % self.fire_rate == 0: # verification de quand tirer
            dir_x = X - (self.x + self.width/2) #distance en X a parcourir
            dir_y = Y - (self.y + self.height/2) #distance en Y a parcourir
            if dir_y < 50 and dir_x < 50:
                time_to_target = 0.5
            else:
                time_to_target = 1.0
            fps = 60
            frames = time_to_target * fps
            speedx = dir_x / frames #vitesse de la balle
            speedy = dir_y / frames #vitesse de la balle
            self.bullets.append(Bullet(
                self.x  + 45*height_ratio(),
                self.y  + 50*height_ratio(),
                speedx, speedy,
                self.damage, self.bullet_penetration,
                self.bullet_size_x, self.bullet_size_y, self.bullet_lifetime,
                self.explosive, self.bounces,
                self.gain_gold
            ))

    def draw(self, screen: pygame.Surface, X: float, Y: float, enemys: list[Enemy]):
        """affiche la tourelle"""
        x, y = self.get_first_enemy_pos(enemys, self.width)
        baliste_rect = baliste.get_rect(center=(self.x, self.y))
        if enemys:
            rotated_baliste= pygame.transform.rotate(baliste,math.degrees(math.atan(x/y)-135))
            screen.blit(pygame.transform.scale(rotated_baliste,(100*height_ratio(screen),100*height_ratio(screen))),(self.x, self.y))
            """resized_baliste = pygame.transform.scale(baliste, (100 * height_ratio(screen), 100 * height_ratio(screen)))
            rotated_baliste = pygame.transform.rotate(resized_baliste, math.degrees(math.atan(x / y) - 135))
            rotated_rect = rotated_baliste.get_rect(center=baliste_rect.center)

            screen.blit((rotated_baliste),(rotated_rect))"""
            #à remplacer quand get_first_enemy_pos sera fix
            
        for elm in self.bullets:
            elm.draw(screen)
        self.bullets = [elm for elm in self.bullets if (elm.x <= X and elm.y <= Y-300 and not elm.dead_bullet(enemys) and elm.time < elm.lifetime)]

        x, y = self.get_first_enemy_pos(enemys, self.width)
        opp = self.y+70 - y
        adj = x - self.x+90
        minigun_rect = minigun.get_rect(center=(self.x+70 * height_ratio(), self.y+65 * height_ratio()))
        if enemys:
            resized_minigun = pygame.transform.scale(minigun, (81 * height_ratio(), 41 * height_ratio()))
            rotated_minigun = pygame.transform.rotate(resized_minigun,math.degrees(math.atan(opp / adj)))
            rotated_rect = rotated_minigun.get_rect(center=minigun_rect.center)

            screen.blit((rotated_minigun),(rotated_rect))
            #à remplacer quand get_first_enemy_pos sera fix



class Bullet:
    def __init__(self, x: float, y: float, speedx: float, speedy: float, damage: int, penetration: int,
                 size_x: int, size_y: int, lifetime: int, explosive: bool, bounces: int, gain_gold):
        """gére les boulets"""
        self.x = x
        self.y = y
        self.gain_gold = gain_gold
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

    def update(self, WIDTH: int, HEIGHT: int):
        """met a jours la tourelle"""
        self.time += 1
        self.x += self.speedx
        self.y += self.speedy
        self.bullet.x = int(self.x)
        self.bullet.y = int(self.y)
        screen_width, screen_height = WIDTH, HEIGHT
        if self.bounces > 0: # vérification des rebonds
            if self.bullet.bottom >= screen_height -100:
                self.speedy *= -1
                self.bounces -= 1
                if self.bullet.bottom >= screen_height - 100:
                    self.bullet.bottom = screen_height - 110

    def dead_bullet(self, enemys: list[Enemy]) -> bool:
        """gérent les collisions boulets ennemis"""
        hits = 0
        for ennemy in enemys[:]:
            if self.bullet.colliderect(ennemy.rect):
                if self.explosive: # module "explosif"
                    radius = 100
                    for target in enemys[:]:
                        dx = target.rect.centerx - self.bullet.centerx
                        dy = target.rect.centery - self.bullet.centery
                        if dx ** 2 + dy ** 2 <= radius ** 2:
                            target.hitbox(self.damage)
                            if target.est_mort():
                                enemys.remove(target)
                                self.gain_gold(ennemy.money())
                else:
                    ennemy.hitbox(self.damage)
                    if ennemy.est_mort():
                        enemys.remove(ennemy)
                        self.gain_gold(ennemy.money())
                self.penetration -= 1
                if self.penetration <= 0:
                    return True
        return False

    def draw(self, screen: pygame.Surface):
        """affiche les boulets"""
        #pygame.draw.rect(screen, (255,0,0), self.bullet)
        screen.blit(resize_cannonball(resized_cannonball),(self.x,self.y))

