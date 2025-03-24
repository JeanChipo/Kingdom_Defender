import pygame

pygame.init()
SCREEN_X, SCREEN_Y = 800, 600
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, size, health, speed, power):
        super().__init__()
        # parametre
        self.size = size
        self.health = health
        self.speed = speed
        self.power = power

        self.rect = pygame.Rect((SCREEN_X - self.size[0], SCREEN_Y - 100 - self.size[1]), self.size)

    def update(self):# deplacement de l'ennemi
        # condition stop du deplacement
        if self.rect.x > 50:
            self.rect.x -= self.speed

    def hitbox(self, canon):
        if self.rect.colliderect(canon):
            self.health -= 100

    def est_mort(self):
        return self.health <= 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


# creation enemy
enemy_moyen = Enemy((30, 50), 10000, 2, 5)
enemy_grand = Enemy((50, 70), 30000, 1, 10)
enemy_petit = Enemy((10, 30), 1000, 3, 3)

enemies = [enemy_moyen, enemy_grand, enemy_petit]

all_sprites = pygame.sprite.Group(enemies)


canon = pygame.Rect((50, SCREEN_Y - 110), (20, 20))

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()


    for enemy in enemies:
        enemy.hitbox(canon)
        if enemy.est_mort():
            all_sprites.remove(enemy)
            enemies.remove(enemy)

    screen.fill((255, 255, 255))

    for enemy in enemies:
        enemy.draw(screen)

    pygame.draw.rect(screen, (0, 255, 0), canon)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
