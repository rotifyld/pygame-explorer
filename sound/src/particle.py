from random import random, randint

import pygame as pg

from src.config import Config

colors = [(255, 255, 0), (0, 255, 255), (255, 0, 255),
          (0, 0, 255), (0, 255, 0), (255, 0, 0)]


class Particle:
    def __init__(self):
        self.x = random() * Config.box.width
        self.y = random() * Config.box.height
        self.vx = (random() - 0.5) * 2 * Config.particle.v_max
        self.vy = (random() - 0.5) * 2 * Config.particle.v_max
        self.colors = [colors[randint(0, len(colors) - 1)], (0, 0, 0)]


class Particles:

    def __init__(self, display, n):
        self.display = display
        self.particles = [Particle() for _ in range(n)]

    def draw(self):
        for p in self.particles:
            pg.draw.circle(self.display,
                           p.colors[0],
                           (int(p.x), int(p.y)),
                           Config.particle.r)

    def update(self):
        for p in self.particles:

            n_x = p.x + p.vx
            n_y = p.y + p.vy

            if n_x < 0:
                n_x = -n_x
                p.vx = -p.vx
            elif n_x > Config.game.width:
                n_x = 2 * Config.game.width - n_x
                p.vx = -p.vx

            if n_y < 0:
                n_y = -n_y
                p.vy = -p.vy
            elif n_y > Config.game.height:
                n_y = 2 * Config.game.height - n_y
                p.vy = -p.vy

            p.x = n_x
            p.y = n_y
