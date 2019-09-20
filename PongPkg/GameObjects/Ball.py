import pygame
import random
from pygame.locals import *
from pygame.math import Vector2


class Ball:

    def __init__(self, image, diameter, speed, x=0, y=0):
        self.origImage = image
        self.origDiam = diameter
        self.origSpeed = speed
        self.origPos = (x, y)
        self.initialize()
        # self.velocity = vel

    def initialize(self):
        self.position = self.origPos
        self.rect = pygame.Rect(self.origPos, (self.origDiam, self.origDiam))
        self.rect.center = self.position
        self.surface = pygame.transform.scale(self.origImage, (self.origDiam, self.origDiam))
        self.diameter = self.origDiam
        self.vel = random.choice([Vector2(-self.origSpeed, -self.origSpeed), Vector2(self.origSpeed, -self.origSpeed),
             Vector2(-self.origSpeed, self.origSpeed), Vector2(self.origSpeed, self.origSpeed)])

    def update_pos(self):
        print('velocity: ' + str(self.vel))
        self.position += self.vel
        self.rect.center = self.position

    def set_vel(self, velocity):
        self.vel = velocity

    def get_pos(self):
        return self.position

    def reset(self):
        self.initialize()

    def reverse_vel_y(self):
        newvel = (self.vel[0], -self.vel[1])
        print('setting velocity: ' + str(newvel))
        self.set_vel(newvel)

    def reverse_vel_x(self):
        newvel = (-self.vel[0], self.vel[1])
        print('setting velocity: ' + str(newvel))
        self.set_vel(newvel)
