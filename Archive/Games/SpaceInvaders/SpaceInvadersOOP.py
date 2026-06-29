import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders OOP")

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Load player image and scale it
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))  # Scale down the image to 50x50

# Load background image
bg_img = pygame.image.load("background.png").convert()

# Define Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color, is_laser=False):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7 * direction
        self.is_laser = is_laser
        if self.is_laser:
            self.image = pygame.Surface((4, HEIGHT))  # Make the laser taller
            self.image.fill(RED)  # Laser color

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.speed = 5
        self.score = 0
        self.health = 3
        self.is_double_shot = False
        self.is_laser = False
        self.last_shot_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 300:  # Delay between shots
            self.last_shot_time = current_time
            if self.is_double_shot:
                left_bullet = Bullet(self.rect.centerx - 10, self.rect.top, -1, GREEN)
                right_bullet = Bullet(self.rect.centerx + 10, self.rect.top, -1, GREEN)
                player_bullets.add(left_bullet, right_bullet)
            elif self.is_laser:
                laser = Bullet(self.rect.centerx, self.rect.top, -1, RED, is_laser=True)
                player_bullets.add(laser)
            else:
                bullet = Bullet(self.rect.centerx, self.rect.top, -1, GREEN)
                player_bullets.add(bullet)

# Define Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))  # Green rectangle for aliens
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.move_down = False
        self.shoot_timer = random.randint(100, 300)  # Increase time between alien shots

    def update(self):
        self.rect.x += self.direction * 2
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += 10

        # Alien shooting logic with cooldown
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = random.randint(100, 300)  # Reset shoot cooldown

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 1, WHITE)
        alien_bullets.add(bullet)

# Define Bunker class
class Bunker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface((60, 40))
        self.original_image.fill(GREEN)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 5

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
        else:
            alpha = max(50, int((self.health / 5) * 255))
            self.image.set_alpha(alpha)

# Define Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH // 2, 50))
        self.speed = 3
        self.health = 10
        self.shoot_timer = 0
        self.direction = 1

    def update(self):
        # Boss moves erratically
        self.rect.x += self.direction * self.speed
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += 10  # Move down once it hits the wall

        # Boss shooting logic
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = 100  # Boss shoots less often

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 1, WHITE)
        alien_bullets.add(bullet)

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN if type == "double_shot" else RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.type = type
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Sprite groups
player = Player()
player_group = pygame.sprite.Group(player)
aliens = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()
bunkers = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Spawn aliens
def spawn_aliens():
    for row in range(4):
        for col in range(10):
            alien = Alien(80 + col * 60, 50 + row * 50)
            aliens.add(alien)

# Spawn bunkers
def spawn_bunkers():
    for i in range(4):
        bunker = Bunker(100 + i * 170, HEIGHT - 100)
        bunkers.add(bunker)

# Draw score
def draw_text(surf, text, x, y):
    rendered = font.render(text, True, WHITE)
    surf.blit(rendered, (x, y))

# Game loop
level = 1
running = True
spawn_aliens()
spawn_bunkers()

while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Draw background
    screen.blit(bg_img, (0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update sprites
    player_group.update()
    aliens.update()
    player_bullets.update()
    alien_bullets.update()
    powerups.update()

    # Check for collisions
    for bullet in pygame.sprite.groupcollide(player_bullets, aliens, True, True).keys():
        player.score += 10
        # Maybe drop a power-up
        if random.random() < 0.2:  # 20% chance to drop a power-up
            powerup_type = "double_shot" if random.random() < 0.5 else "laser"
            powerup = PowerUp(bullet.rect.centerx, bullet.rect.centery, powerup_type)
            powerups.add(powerup)

    # Player power-up collisions
    for powerup in pygame.sprite.spritecollide(player, powerups, True):
        if powerup.type == "double_shot":
            player.is_double_shot = True
        elif powerup.type == "laser":
            player.is_laser = True

    # Collisions with bunkers and alien bullets
    pygame.sprite.groupcollide(player_bullets, bunkers, True, False)
    pygame.sprite.groupcollide(alien_bullets, bunkers, True, False)

    # Collisions with player and alien bullets
    if pygame.sprite.spritecollide(player, alien_bullets, True):
        player.health -= 1

    # Boss spawn and behavior
    if len(aliens) == 0:
        if level == 1:
            boss = Boss()
            player_group.add(boss)
            level += 1
        spawn_aliens()  # Spawn new level aliens

    # Draw everything
    player_group.draw(screen)
    aliens.draw(screen)
    player_bullets.draw(screen)
    alien_bullets.draw(screen)
    bunkers.draw(screen)
    powerups.draw(screen)

    draw_text(screen, f"Score: {player.score}  Health: {player.health}", 10, 10)

    # End game if health reaches 0
    if player.health <= 0:
        running = False

    pygame.display.flip()

pygame.quit()
