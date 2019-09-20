import pygame
from pygame.locals import *
from pygame.math import Vector2


class Bumper:
    def __init__(self, image, x=0, y=0, width=0, height=0, color=(0, 0, 0), velocity=Vector2(2, 2)):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (x, y)
        self.color = color
        self.vel = velocity
        self.surface = pygame.transform.scale(image, (width, height))

    def change_color(self, color):
        self.color = color

    def get_rect(self):
        return self.rect

    def set_rect_left(self, left):
        self.rect.left = left

    def set_rect_top(self, top):
        self.rect.top = top

    def get_velocity(self):
        return self.vel

    def set_velocity(self, velocity):
        self.vel = velocity
