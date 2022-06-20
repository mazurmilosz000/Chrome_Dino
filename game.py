from settings import *
import random
import sys
from background import Background
from dinosaur import Dinosaur

"""It's a modify chrome dino game with a different levels. A game speed depends on level which user can choose."""


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

# game speed
game_speed = 10


# a function that displays text on the screen
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
        self.running = True
        self.game_paused = False
        self.game_score = 0
        self.deaths = 0

    def score(self):
        global game_speed
        if game_speed > 0:
            self.game_score += 0.25
            if self.game_score % 100 == 0:
                POINT_SOUND.play()
                game_speed += 1

        # render text
        points = font.render("Points: " + "{:.0f}".format(self.game_score), True, (0, 0, 0))
        points_rect = points.get_rect()
        points_rect.center = (1000, 40)
        screen.blit(points, points_rect)

    def run(self, speed=10):
        pygame.display.set_caption("Chrome Dino!")
        global game_speed
        game_speed = speed
        while self.running:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
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
                # detect collisions with obstacles
                if dinosaur.dino_rect.colliderect(obstacle.rect):
                    # play sound when dino dies
                    DIE_SOUND.play()
                    game_speed = 0
                    self.deaths += 1
                    dinosaur.image = DINO_DEAD
                    self.main_menu()

            self.score()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    """ A method that represents the main menu of the game. The menu allows you to select the difficulty level of the 
    game (easy, hard) and in case of pausing, it allows you to resume the game."""
    def main_menu(self):
        while True:

            if self.deaths == 0 and not self.game_paused:
                self.screen.fill(WHITE)
                pygame.display.set_caption("Menu")
                display_text(big_menu_font, 550, 40, "MAIN MENU")
                display_text(menu_font, 550, 120, "press 'e' to easy mode")
                display_text(menu_font, 550, 200, "press 'h' to hard mode")
                screen.blit(DINO_RUNNING[0], (500, 280))
                display_text(menu_font, 550, 480, "press 'q' to quit")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            pygame.display.set_caption("Chrome Dino Game")
                            self.run()
                        if event.key == pygame.K_h:
                            pygame.display.set_caption("Chrome Dino Game")
                            self.run(20)
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

            elif self.deaths == 0 and self.game_paused:
                self.screen.fill(WHITE)
                pygame.display.set_caption("Paused")

                # get current speed of game to unpause with the same speed
                current_speed = game_speed
                display_text(big_menu_font, 550, 40, "GAME PAUSED")
                display_text(menu_font, 550, 120, "press 'space' to resume the game")
                screen.blit(DINO_RUNNING[0], (500, 250))
                display_text(menu_font, 550, 480, "press 'q' to quit")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.run(current_speed)
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

            elif self.deaths > 0:
                self.game_paused = False
                pygame.display.set_caption("Game Over")
                game_score = int(self.game_score)
                display_text(big_menu_font, 550, 40, "GAME OVER")
                display_text(menu_font, 550, 120, f"score: {game_score}")

                # read (and save) high score in 'score.txt' file
                with open("score.txt", "r+") as f:
                    high_score = int(f.read())
                    if high_score < game_score:
                        f.seek(0)
                        f.write(f'{game_score}')
                        high_score = game_score

                    # display high score in game over menu
                    display_text(menu_font, 550, 200, f"high score: {high_score}")
                    f.close()

                display_text(menu_font, 550, 280, "press 'r' to restart")
                display_text(menu_font, 550, 480, "press 'q' to quit")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_r:
                            # restart game
                            global obstacles
                            self.deaths = 0
                            self.game_score = 0
                            # set the dino to the starting position
                            dinosaur.dino_rect.x = DINO_X_POS
                            dinosaur.dino_rect.y = DINO_Y_START_POS
                            dinosaur.y_velocity = 0
                            # set new random obstacles
                            obstacles = []
                            self.main_menu()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.main_menu()
