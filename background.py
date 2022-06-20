from settings import *

""" A class that represents background in my game"""


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