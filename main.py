import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# creating game screen
screen = pygame.display.set_mode((800, 600))

# Title and icon in window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('shuttle.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('space.jpg')

# background sounds
# mixer.music.load('backgroundd.wav')
# mixer.music.play(-1)

# player
playerImg = pygame.image.load('player.png')
playerX = 360
playerY = 480
playerX_change = 0  # set to 0 so X value becomes 0 when key is released

# enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemy = 8
for i in range(num_of_enemy):

    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(80, 280))
    enemyX_change.append(0.5)
    enemyY_change.append(80)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 365
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"  # ready state means bullet cannot be seen  ||  fire state means bullet is moving in y axis towards enemy

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Game ver text
over_font = pygame.font.Font('freesansbold.ttf', 80)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (200, 200, 200))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (200, 200, 200))
    screen.blit(over_text, (150, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means drawing


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))

    if distance < 30:
        return True




# -------------------------------------------------------game running loop----------------------------------------------
running = True
while running:
    # screen color
    screen.fill((128, 128, 128))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # right or left keystroke pressed
        if event.type == pygame.KEYDOWN:
            # print("A keystroke is pressed!")
            if event.key == pygame.K_LEFT:
                # print("left key pressed!")
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                # print("right key pressed!")
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    shoot_sound = mixer.Sound('backgroundd.wav')
                    shoot_sound.play()
                    # print("bullet fired!")
                    bulletX = playerX + 15
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("keystroke is relesed!")
                playerX_change = 0

    # playerY -= 0.05
    playerX += playerX_change

    # enemy movement

    # player boundry
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # enemy boundry and movement
    for i in range(num_of_enemy):

        # Game Over
        if enemyY[i] > 450:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 0.3
        elif enemyX[i] > 736:
            # enemyX = 736
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -0.3

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            explosion_sound = mixer.Sound('explode.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(80, 280)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    player(playerX, playerY)
    # bullet(bulletX, bulletY)
    show_score(textX, textY)
    pygame.display.update()
