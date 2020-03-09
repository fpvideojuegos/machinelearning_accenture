import math
import random

#librerías importadas de pygame
import pygame
from pygame import mixer

# Inicializa pygame
pygame.init()
#creamos la escena
screen = pygame.display.set_mode((800, 600))
reloj = pygame.time.Clock()

# Esto es el fondo
background = pygame.image.load('backgroundd.png')

# Música de fondo
mixer.music.load("backgroundd.mp3")
mixer.music.play(-1)

#imagenes
pygame.display.set_caption("Apashe Tomca")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Cargamos la imagen del jugador y definimos las coordenadas en las que aparece
playerImg = pygame.image.load('nave2.png')
playerX = 370
playerY = 480
playerX_change = 0

#Nave huidiza
player2Img = pygame.image.load('ufo.png')
player2X = 370
player2Y = 50
player2X_change = 0


# Array de enemigos. Ponemos 6, pero podemos poner los que queramos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

#bucle para generar los enemigos
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy2.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bala

# Ready - Aparece la bala
# Fire - Ahora la bala se mueve

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Puntuación. La seteamos a 0 (obviamente) y le ponemos una fuente bonita

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))
    
def player2(x, y):
    screen.blit(player2Img, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 15))

#colisiones enemigos y bala
def isCollision(enemyX, enemyY, bulletX, bulletY):
    #raiz cuadrada y potencias
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

#Bucle que ejecuta el juego
running = True
while running:

    screen.fill((0, 0, 0))
    
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#Movimiento naves - EVENTOS DE TECLADO -. El ufo se mueve siempre en la dirección opuesta a la nave
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -8
                player2X_change = 7
            if event.key == pygame.K_RIGHT:
                playerX_change = 8
                player2X_change = -7
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    player2X += player2X_change
    if player2X <= 0:
        player2X = 0
    elif player2X >= 736:
        player2X = 736

    # Movimiento enemigos
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 800
            game_over_text()
            pygame.quit()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Colisión de balas con enemigos
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            
        # colisiones de la nave reina
        collision2 = isCollision(player2X, player2Y, bulletX, bulletY)
        if collision2:
            explosionSound = mixer.Sound("ovniScream.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            player2X = random.randint(0, 736)
            player2Y = random.randint(50, 150)
            
    

        enemy(enemyX[i], enemyY[i], i)

    # Movimiento balas
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    player2(player2X, player2Y)
    show_score(textX, testY)
    pygame.display.update()
    reloj.tick(60)
