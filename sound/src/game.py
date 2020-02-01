from random import random, randint

import pygame as pg

from src.config import Config
from src.particle import Particles


class Game:
    def __init__(self, display):
        self.display = display
        self.mouse_pos = (0, 0)
        self.particles = Particles(display, Config.simulation.num_particles)

    def loop(self):
        clock = pg.time.Clock()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEMOTION:
                    if pg.mouse.get_pressed()[0]:
                        self.mouse_pos = pg.mouse.get_pos()

            # self.grid.loop()
            self.particles.update()

            # self.grid.draw()
            # self.display.fill(pg.Color(0, 0, 0))
            self.particles.draw()

            pg.display.update()
            clock.tick(Config['game']['fps'])
