from settings import *
import random
import button

"""It's a modify chrome dino game with a different levels. A game speed depends on level which user can choose."""
# todo: add collisions, create and add start menu with different difficulties levels


class Background:
    def __init__(self, x, y):
        self.width = WIDTH
        self.height = HEIGHT
        self.image = BG
        self.x = x
        self.y = y
        self.draw()

    def update(self, speed):
        self.x -= speed
        if self.x <= -WIDTH:
            self.x = WIDTH

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.run_img = DINO_RUNNING
        self.jump_img = DINO_JUMPING
        self.duck_img = DINO_DUCKING

        self.running = True
        self.jumping = False
        self.ducking = False

        # step index for animation
        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = DINO_X_POS
        self.dino_rect.y = DINO_Y_START_POS
        self.y_velocity = 0
        self.level = None
        self.lives = 3

    def get_event(self, user_input):
        if self.running:
            self.run()
        if self.ducking:
            self.duck()

        if self.step_index >= DINO_ANIM_SPEED*2:
            self.step_index = 0

        if user_input[pygame.K_UP] and not self.jumping:
            self.running = False
            self.jumping = True
            self.ducking = False
            self.jump()
        elif user_input[pygame.K_DOWN] and not self.ducking and not self.jumping:
            self.running = False
            self.jumping = False
            self.ducking = True
        elif not (self.jumping or user_input[pygame.K_DOWN]):
            self.running = True
            self.jumping = False
            self.ducking = False

    def run(self):
        self.image = self.run_img[self.step_index // DINO_ANIM_SPEED]
        self.step_index += 1

    def jump(self):
        self.y_velocity = -DINO_JUMP_HEIGHT

    def duck(self):
        self.image = self.duck_img[self.step_index // DINO_ANIM_SPEED]
        self.step_index += 2
        self.dino_rect.y = DINO_Y_DUCK_POS

    def draw(self, surface, user_input):

        # move the dino downwards every frame
        self.dino_rect.y += self.y_velocity
        if not self.grounded:
            self.y_velocity += DINO_GRAVITY_AMOUNT

            # in the real game, holding down in midair moves the dino downwards faster
            if user_input[pygame.K_DOWN]:
                self.y_velocity += 1

            if self.dino_rect.y > DINO_Y_START_POS:  # fix dino clipping through the floor
                self.dino_rect.y = DINO_Y_START_POS
                self.y_velocity = 0
                self.jumping = False

        duck_offset = int(self.image.get_height() == 60)*36  # this is definitly a bad way to do this
        surface.blit(self.image, (self.dino_rect.x, self.dino_rect.y+duck_offset))

    @property
    def grounded(self):
        """Checks if the dino is on the floor"""
        return self.dino_rect.y == DINO_Y_START_POS and not self.jumping


class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(0, WIDTH)
        self.y = random.randint(50, 150)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed - 6
        if self.x < -self.width:
            self.x = WIDTH+random.randint(0, 100)
            self.y = random.randint(50, 150)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WIDTH

    def update(self):
        # move obstacle cross the screen
        self.rect.x -= game_speed
        # remove obstacles when they are off the screen
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, surface):
        surface.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacles):
    def __init__(self, image):
        # display only 1 bird on the screen
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 260
        self.step_index = 0

    def draw(self, surface):
        # value 36 to slow down the bird animation
        if self.step_index >= 36:
            self.step_index = 0
        surface.blit(self.image[self.step_index//20], self.rect)
        self.step_index += 1


# instantiation of objects
background = [Background(X_POS_BG, Y_POS_BG), Background(X_POS_BG + WIDTH, Y_POS_BG)]
dinosaur = Dinosaur()
clouds = [Cloud(), Cloud(), Cloud(), Cloud()]
obstacles = []

# instantiation of buttons
resume_button = button.Button(304, 125, RESUME_IMAGE, 1)


# game speed
game_speed = 14
x_pos_bg = 0
y_pos_bg = 380


class Game:
    def __init__(self):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Chrome Dino!")
        self.running = True
        self.game_paused = False

    def run(self):
        while self.running:
            self.screen.fill(WHITE)
            # check if game is paused
            if self.game_paused:
                # resume_button.draw(screen)
                print('paused')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_paused = True
                        # self.running = False

            for bg in background:
                bg.update(game_speed)
                bg.draw()

            user_input = pygame.key.get_pressed()
            for cloud in clouds:
                cloud.draw(screen)
                cloud.update()
            dinosaur.draw(screen, user_input)
            dinosaur.get_event(user_input)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD_FLYING))

            for obstacle in obstacles:
                obstacle.draw(screen)
                obstacle.update()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
