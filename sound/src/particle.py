from random import random, randint

import numpy as np
import pygame as pg

from src.config import Config


# todo colors
# colors = [(255, 255, 0), (0, 255, 255), (255, 0, 255)]


class Particle:
    def __init__(self):
        self.x = random() * Config.box.width
        self.y = random() * Config.box.height
        self.vx = (random() - 0.5) * 2 * Config.particle.v_max
        self.vy = (random() - 0.5) * 2 * Config.particle.v_max


def bounce_walls(x, y, vx, vy):
    # bounce off walls
    if x < 0:
        x = -x
        vx = -vx
    elif x > Config.game.width:
        x = 2 * Config.game.width - x
        vx = -vx
    if y < 0:
        y = -y
        vy = -vy
    elif y > Config.game.height:
        y = 2 * Config.game.height - y
        vy = -vy

    return x, y, vx, vy


class Particles:

    def __init__(self, display, n):
        self.display = display
        self.x = np.random.sample(n) * Config.box.width
        self.y = np.random.sample(n) * Config.box.height
        self.vx = 2 * (np.random.sample(n) - 0.5) * Config.particle.v_max
        self.vy = 2 * (np.random.sample(n) - 0.5) * Config.particle.v_max

    def draw(self):
        for x, y in zip(self.x, self.y):
            pg.draw.circle(self.display,
                           Config.particle.color,
                           (int(x), int(y)),
                           Config.particle.r)

    def bounce_walls(self):

        for pos, vel, high in [(self.x, self.vx, Config.box.width),
                               (self.y, self.vy, Config.box.height)]:
            where = pos < 0
            np.copyto(vel, -vel, where=where)
            np.copyto(pos, -pos, where=where)
            where = pos > high
            np.copyto(vel, -vel, where=where)
            np.copyto(pos, 2 * high - pos, where=where)

    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

        self.bounce_walls()

        # todo bounce each other
