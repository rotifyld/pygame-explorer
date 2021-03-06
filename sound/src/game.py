from datetime import datetime
from random import random, randint

import numpy as np
import pygame as pg

from src.config import Config
from src.particle import Particles


class Game:
    def __init__(self, display):
        self.display = display
        self.mouse_pos = (0, 0)
        self.particles = Particles(display, Config.simulation.num_particles)

        if Config.debug.benchmark:
            self.benchmark = []

    def update(self):
        self.particles.update()

    def draw(self):
        # draw black background
        self.display.fill((0, 0, 0))
        # self.display.line()

        self.particles.draw()

        pg.display.update()

    def loop(self):
        clock = pg.time.Clock()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEMOTION:
                    if pg.mouse.get_pressed()[0]:
                        self.mouse_pos = pg.mouse.get_pos()

            zero_t = datetime.now()
            self.update()
            update_t = datetime.now()
            self.draw()
            draw_t = datetime.now()
            if Config.debug.benchmark:
                if len(self.benchmark) == Config.debug.print_every:
                    print("update takes {0:.3f}% of time".format(10 * np.mean(self.benchmark)))
                    self.benchmark = []
                self.benchmark.append((update_t - zero_t) / (draw_t - zero_t))

            clock.tick(Config.game.fps)
