from random import random, randint

import numpy as np
import pygame as pg

from src.config import Config

# todo colors
colors = [(255, 255, 0), (0, 255, 255), (255, 0, 255)]


class Particles:

    def __init__(self, display, n):
        self.display = display
        self.x = np.random.sample(n) * Config.box.width
        self.y = np.random.sample(n) * Config.box.height
        self.z = np.random.sample(n) * 100
        self.vx = 2 * (np.random.sample(n) - 0.5) * Config.particle.v_max
        self.vy = 2 * (np.random.sample(n) - 0.5) * Config.particle.v_max
        self.vz = 2 * (np.random.sample(n) - 0.5) * Config.particle.v_max
        # self.colors = [colors[randint(0, len(colors) - 1)] for _ in range(n)]

    def draw(self):
        for x, y, z in zip(self.x, self.y, self.z):
            color = (255 - (2 * z), 0, 55 + (2 * z))

            pg.draw.circle(self.display,
                           color,
                           (int(x), int(y)),
                           Config.particle.r)

    def bounce_walls(self):

        for pos, vel, high in [(self.x, self.vx, Config.box.width),
                               (self.y, self.vy, Config.box.height),
                               (self.z, self.vz, 100)]:
            where = pos < 0
            np.copyto(vel, -vel, where=where)
            np.copyto(pos, -pos, where=where)
            where = pos > high
            np.copyto(vel, -vel, where=where)
            np.copyto(pos, 2 * high - pos, where=where)

    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.z = self.z + self.vz

        self.bounce_walls()

        # todo bounce each other
