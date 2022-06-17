from settings import *
import random
import button

"""It's a modify chrome dino game with a different levels. A game speed depends on level which user can choose."""
# todo: add collisions, break the code into modules, fix 'video system not initialized' error, add sound effects
# todo: add save top score, check code (delete unnecessary items), add documentation, add requirements.txt
# todo: delete button module


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
                self.y_velocity += 1.25

            if self.dino_rect.y > DINO_Y_START_POS:  # fixed dino clipping through the floor
                self.dino_rect.y = DINO_Y_START_POS
                self.y_velocity = 0
                self.jumping = False

        duck_offset = int(self.image.get_height() == 60)*36  # this is definitely a bad way to do this
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
    def __init__(self, image, image_type):
        self.image = image
        self.type = image_type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WIDTH

    def update(self, g_speed):
        # move obstacle cross the screen
        self.rect.x -= g_speed
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
        # random choice from 3 different positions
        self.rect.y = random.choice([260, 220, 300])
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
game_speed = 10


def display_text(character, pos_x, pos_y, txt):
    text = character.render(txt, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (pos_x, pos_y)
    screen.blit(text, text_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Chrome Dino!")
        self.running = True
        self.game_paused = False
        self.game_score = 0
        self.deaths = 0

    def score(self):
        global game_speed
        self.game_score += 0.25
        if self.game_score % 100 == 0:
            game_speed += 1

        # render text

        points = font.render("Points: " + "{:.0f}".format(self.game_score), True, (0, 0, 0))
        points_rect = points.get_rect()
        points_rect.center = (1000, 40)
        screen.blit(points, points_rect)

    def run(self, speed=10):
        global game_speed
        game_speed = speed
        while self.running:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_paused = True
                        self.main_menu()

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
                obstacle.update(game_speed)

            self.score()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()

    """ A method that represents the main menu of the game. The menu allows you to select the difficulty level of the 
    game (easy, hard) and in case of pausing, it allows you to resume the game."""
    def main_menu(self):
        while True:
            self.screen.fill(WHITE)
            if self.deaths == 0 and not self.game_paused:
                pygame.display.set_caption("Menu")
                display_text(big_menu_font, 550, 40, "MAIN MENU")
                display_text(menu_font, 550, 120, "press 'e' to easy mode")
                display_text(menu_font, 550, 200, "press 'h' to hard mode")
                display_text(menu_font, 550, 480, "press 'q' to quit")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            self.run()
                        if event.key == pygame.K_h:
                            self.run(20)
                        if event.key == pygame.K_q:
                            pygame.quit()

            elif self.deaths == 0 and self.game_paused:
                pygame.display.set_caption("Paused")

                # get current speed of game to unpause with the same speed
                current_speed = game_speed
                display_text(big_menu_font, 550, 40, "GAME PAUSED")
                display_text(menu_font, 550, 120, "press 'space' to resume the game")
                display_text(menu_font, 550, 480, "press 'q' to quit")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.run(current_speed)
                        if event.key == pygame.K_q:
                            pygame.quit()

            pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.main_menu()
