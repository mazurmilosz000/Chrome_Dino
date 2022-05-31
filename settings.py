import pygame
import os

WINDOW_SIZE = WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode(WINDOW_SIZE)
FPS = 60

WHITE = (255, 255, 255)

# position of dinosaur (position is not changeable)
X_POS = 80
Y_POS = 310

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