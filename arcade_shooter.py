import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
ENEMY_SPEED = 3
ENEMY_SHOOT_COOLDOWN = 1  # Enemy shooting cooldown in seconds
BULLET_SPEED = 8
SHOOT_COOLDOWN = 0.2
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Shooter")

# Load images
player_img = pygame.image.load(r"C:\Users\wjrtsf\Desktop\test\player.png")
enemy_img = pygame.image.load(r"C:\Users\wjrtsf\Desktop\test\enemy.png")
bullet_img = pygame.image.load(r"C:\Users\wjrtsf\Desktop\test\bullet.png")

# Initialize player
player_x = WIDTH // 2
player_y = HEIGHT - 50

# Lists to store enemies and bullets
enemies = []
enemy_bullets = []
bullets = []

# Function to calculate angle between two points
def calculate_angle(x1, y1, x2, y2):
    angle = math.atan2(y2 - y1, x2 - x1)
    return angle

# Game loop
running = True
game_over = False
last_shot_time = 0
last_enemy_shot_time = 0  # Track the time of the last enemy shot
score = 0  # Initialize score
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

while running:
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_x = WIDTH // 2
                    player_y = HEIGHT - 50
                    enemies.clear()
                    bullets.clear()
                    enemy_bullets.clear()
                    score = 0  # Reset score
                    ENEMY_SPEED = 3  # Reset enemy speed
                    ENEMY_SHOOT_COOLDOWN = 0.2  # Reset enemy shooting cooldown
                    game_over = False

        screen.fill((0, 0, 0))
        text = font.render("Game Over - Press 'R' to Restart", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        score_text = font.render("Score: " + str(score), True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(score_text, score_rect)

        pygame.display.update()
        clock.tick(60)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_y += PLAYER_SPEED

    # Check if player touches the borders
    if player_x < 0 or player_x > WIDTH or player_y < 0 or player_y > HEIGHT:
        game_over = True

    # Shoot if enough time has passed since the last shot
    current_time = time.time()
    if keys[pygame.K_SPACE] and current_time - last_shot_time > SHOOT_COOLDOWN:
        bullets.append([player_x + 16, player_y])
        last_shot_time = current_time

    # Move bullets
    bullets_to_remove = []
    for bullet in bullets:
        bullet[1] -= BULLET_SPEED
        if bullet[1] < 0:
            bullets_to_remove.append(bullet)

    # Spawn enemies more frequently
    if random.randint(1, 50) < 2:
        enemies.append([random.randint(0, WIDTH - 32), 0])

    # Move enemies and handle collisions
    enemies_to_remove = []
    bullets_to_remove = []

    for enemy in enemies:
        enemy[1] += ENEMY_SPEED

        # Check collision with player
        if (
            player_x < enemy[0] + 32
            and player_x + 32 > enemy[0]
            and player_y < enemy[1] + 32
            and player_y + 32 > enemy[1]
        ):
            game_over = True

        # Enemy shooting logic
        current_time = time.time()
        if current_time - last_enemy_shot_time > ENEMY_SHOOT_COOLDOWN:
            enemy_bullets.append([enemy[0] + 16, enemy[1] + 32])
            last_enemy_shot_time = current_time

        for bullet in bullets:
            if (
                bullet[0] > enemy[0]
                and bullet[0] < enemy[0] + 32
                and bullet[1] > enemy[1]
                and bullet[1] < enemy[1] + 32
            ):
                bullets_to_remove.append(bullet)
                enemies_to_remove.append(enemy)
                score += 1  # Increase score when enemy is hit

        if enemy[1] > HEIGHT:
            enemies_to_remove.append(enemy)

    # Move enemy bullets
    enemy_bullets_to_remove = []
    for bullet in enemy_bullets:
        bullet[1] += BULLET_SPEED
        if bullet[1] > HEIGHT:
            enemy_bullets_to_remove.append(bullet)

        # Check collision with player
        if (
            player_x < bullet[0] + 8
            and player_x + 32 > bullet[0]
            and player_y < bullet[1] + 8
            and player_y + 32 > bullet[1]
        ):
            game_over = True

    # Remove collided bullets and enemies
    for bullet in bullets_to_remove:
        bullets.remove(bullet)
    for enemy in enemies_to_remove:
        if enemy in enemies:
            enemies.remove(enemy)
    for bullet in enemy_bullets_to_remove:
        enemy_bullets.remove(bullet)

    # Clear the screen
    screen.fill((0, 0, 0))

    if not game_over:
        # Draw player
        screen.blit(player_img, (player_x, player_y))

        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))

        # Draw bullets
        for bullet in bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))

        # Draw enemy bullets
        for bullet in enemy_bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))

        # Draw borders
        pygame.draw.rect(screen, RED, (0, 0, WIDTH, 10))  # Top border
        pygame.draw.rect(screen, RED, (0, HEIGHT - 10, WIDTH, 10))  # Bottom border
        pygame.draw.rect(screen, RED, (0, 0, 10, HEIGHT))  # Left border
        pygame.draw.rect(screen, RED, (WIDTH - 10, 0, 10, HEIGHT))  # Right border

        # Draw score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        # Increase difficulty based on score
        if score >= 5:
            ENEMY_SPEED = 4
            ENEMY_SHOOT_COOLDOWN = 0.2
        if score >= 10:
            ENEMY_SPEED = 5
            ENEMY_SHOOT_COOLDOWN = 0.15
        if score >= 15:
            ENEMY_SPEED = 7
            ENEMY_SHOOT_COOLDOWN = 0.1
            PLAYER_SPEED = 6
        # more opption if wanted

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
