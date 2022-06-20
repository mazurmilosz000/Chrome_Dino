import pygame
import os
from pygame import mixer


WINDOW_SIZE = WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode(WINDOW_SIZE)
FPS = 60

WHITE = (255, 255, 255)

# background attributes
X_POS_BG = 0
Y_POS_BG = 380

# dinosaur attributes
DINO_X_POS = 80
DINO_Y_START_POS = 310
DINO_Y_DUCK_POS = 530
DINO_ANIM_SPEED = 9
DINO_JUMP_HEIGHT = 15
DINO_GRAVITY_AMOUNT = 0.7

# fonts
pygame.init()

# regular font to display score
font = pygame.font.SysFont('Comic Sans MS', 20)

# fonts to display menu
menu_font = pygame.font.SysFont('Arial Black', 20)

big_menu_font = pygame.font.SysFont('Arial Black', 30)

# images
# a variable that represents background
BACKGROUND = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# a list that represents dino running
DINO_RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

# a variable that represents dino jumping
DINO_JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

# a list that represents dino ducking
DINO_DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

# a list that represents bird flying
BIRD_FLYING = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
               pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

# a list that represents large cactus
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

# a list that represents small cactus
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

DINO_DEAD = pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png"))

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# Sound effects
DIE_SOUND = mixer.Sound(os.path.join("sounds", "die.wav"))

JUMP_SOUND = mixer.Sound(os.path.join("sounds", "jump.wav"))

POINT_SOUND = mixer.Sound(os.path.join("sounds", "point.wav"))

