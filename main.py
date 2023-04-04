import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption('Space Invasion')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background.jpg')

# Add music
mixer.music.load('Background music.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Player variables
img_player = pygame.image.load('rocket.png')
player_x = 368
player_y = 500
player_x_change = 0

# Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 8

for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.5)
    enemy_y_change.append(50)

# Laser variables
img_laser = pygame.image.load('laser.png')
laser_x = 0
laser_y = 500
laser_x_change = 0
laser_y_change = 3
laser_visibility = False

# Score
score = 0
font = pygame.font.Font('Fastest.ttf', 32)
text_x = 10
text_y = 10

# Game over text
final_font = pygame.font.Font('Fastest.ttf', 50)


def final_text():
    my_final_font = final_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(my_final_font, (180, 200))


# Show score function
def show_score(x, y):
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (x, y))


# Player function
def player(x, y):
    screen.blit(img_player, (x, y))


# Enemy function
def enemy(x, y, ene):
    screen.blit(img_enemy[ene], (x, y))


# Laser shot function
def laser_shot(x, y):
    global laser_visibility
    laser_visibility = True
    screen.blit(img_laser, (x + 16, y + 10))


# Collision detection function
def is_collision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
executes = True
while executes:

    # Background
    screen.blit(background, (0, 0))

    # Event iteration
    for event in pygame.event.get():

        # Quit event
        if event.type == pygame.QUIT:
            executes = False

        # Keydown event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                laser_sound = mixer.Sound('laser.mp3')
                laser_sound.play()
                if not laser_visibility:
                    laser_x = player_x
                    laser_shot(laser_x, laser_y)
        # Keyup event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Modify player location
    player_x += player_x_change

    # Keep player within the borders
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Modify enemy location
    for e in range(number_of_enemies):

        # Game over
        if enemy_y[e] > 500:
            for k in range(number_of_enemies):
                enemy_y[k] = 1000
            final_text()
            break

        enemy_x[e] += enemy_x_change[e]

    # Keep enemy within the borders
        if enemy_x[e] <= 0:
            enemy_x_change[e] = 1
            enemy_y[e] += enemy_y_change[e]
        elif enemy_x[e] >= 736:
            enemy_x_change[e] = -1
            enemy_y[e] += enemy_y_change[e]

        # Collision
        collision = is_collision(enemy_x[e], enemy_y[e], laser_x, laser_y)
        if collision:
            collision_sound = mixer.Sound('hit.mp3')
            collision_sound.play()
            laser_y = 500
            laser_visibility = False
            score += 1
            enemy_x[e] = random.randint(0, 736)
            enemy_y[e] = random.randint(50, 200)

        enemy(enemy_x[e], enemy_y[e], e)
    # Laser motion
    if laser_y <= -32:
        laser_y = 500
        laser_visibility = False

    if laser_visibility:
        laser_shot(laser_x, laser_y)
        laser_y -= laser_y_change

    player(player_x, player_y)

    show_score(text_x, text_y)

    # Update
    pygame.display.update()
