from settings import *


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
        elif user_input[pygame.K_DOWN] and not self.ducking:
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
        pass

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

        surface.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    @property
    def grounded(self):
        """Checks if the dino is on the floor"""
        return self.dino_rect.y == DINO_Y_START_POS and not self.jumping


# instantiation of objects
dinosaur = Dinosaur()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Chrome Dino!")
        self.running = True

    def run(self):
        while self.running:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            user_input = pygame.key.get_pressed()
            dinosaur.draw(screen, user_input)
            dinosaur.get_event(user_input)

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
