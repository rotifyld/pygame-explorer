from random import random, randint

import numpy as np
import pygame as pg

from src.config import Config

colors = [(255, 255, 0), (0, 255, 255), (255, 0, 255)]


def init_fonts(n):
    font = pg.font.Font(pg.font.get_default_font(), Config.debug.label_size)

    # now print the text
    return [font.render(str(i), False, (255, 255, 255)) for i in range(n)]


# based on https://github.com/yoyoberenguer/Elastic-Collision
def equal_mass_elastic_collision(pos1, pos2, v1, v2):
    norm = np.linalg.norm(pos1 - pos2) ** 2
    dv = np.dot(v1 - v2, pos1 - pos2) * (pos1 - pos2) / norm

    u1 = v1 - dv
    u2 = v2 + dv
    return u1, u2


class Particles:

    def __init__(self, display, n):
        self.display = display
        self.x = Config.box.x_low + np.random.sample(n) * (Config.box.x_high - Config.box.x_low)
        self.nx = self.x
        self.y = Config.box.y_low + np.random.sample(n) * (Config.box.y_high - Config.box.y_low)
        self.ny = self.y
        self.vx = 2 * (np.random.sample(n) - 0.5) * Config.particle.v_max
        self.vy = 2 * (np.random.sample(n) - 0.5) * Config.particle.v_max
        self.colors = [colors[randint(0, len(colors) - 1)] for _ in range(n)]

        self.p_collision = np.zeros((1, 2))

        if Config.debug.collisions:
            self.num_collisions = []

        if Config.debug.labels:
            self.labels = init_fonts(n)

    def draw(self):
        for x, y, color in zip(self.x, self.y, self.colors):
            pg.draw.circle(self.display,
                           color,
                           (int(x), int(y)),
                           Config.particle.r)

        if Config.debug.labels:
            r = Config.particle.r
            for label, x, y in zip(self.labels, self.x, self.y):
                self.display.blit(label, dest=(x + r, y - r))

    def bounce_walls(self):

        for pos, vel, low, high in [(self.nx, self.vx, Config.box.x_low, Config.box.x_high),
                                    (self.ny, self.vy, Config.box.y_low, Config.box.y_high)]:
            where = pos < low
            np.copyto(vel, -vel, where=where)
            np.copyto(pos, 2 * low - pos, where=where)
            where = pos > high
            np.copyto(vel, -vel, where=where)
            np.copyto(pos, 2 * high - pos, where=where)

    def bounce_each_other(self):

        if Config.debug.collisions:
            if len(self.num_collisions) < Config.debug.print_every:
                self.num_collisions.append(0)
            else:
                print('Avg. {0:.0f} collisions per step'.format(np.mean(self.num_collisions)))
                self.num_collisions = [0]

        dist_x = np.abs(np.subtract.outer(self.nx, self.nx))
        dist_y = np.abs(np.subtract.outer(self.ny, self.ny))
        appx_dist = dist_x + dist_y

        potential_collisions = np.dstack(np.where((0 < appx_dist) * (appx_dist < (3 * Config.particle.r))))

        if potential_collisions[0].size > 0:
            collided = set()
            for (m, n) in potential_collisions[0]:
                if len(collided.intersection((m, n))) == 0:
                    collided.add(m)
                    collided.add(n)

                    pos1 = np.array([self.nx[m], self.ny[m]])
                    pos2 = np.array([self.nx[n], self.ny[n]])

                    exact_distance = np.linalg.norm(pos1 - pos2)

                    if exact_distance < 2 * Config.particle.r:
                        if Config.debug.collisions:
                            self.num_collisions[-1] += 1
                        v1 = np.array([self.vx[m], self.vy[m]])
                        v2 = np.array([self.vx[n], self.vy[n]])

                        u1, u2 = equal_mass_elastic_collision(pos1, pos2, v1, v2)

                        # save results
                        self.vx[m] = u1[0]
                        self.vy[m] = u1[1]
                        self.vx[n] = u2[0]
                        self.vy[n] = u2[1]
                        self.nx = self.x + self.vx
                        self.ny = self.y + self.vy

        if Config.debug.labels:
            is_new_collision = self.p_collision.data != potential_collisions.data
            self.p_collision = potential_collisions

    def update(self):
        self.nx = self.x + self.vx
        self.ny = self.y + self.vy

        self.bounce_each_other()

        self.bounce_walls()

        self.x = self.nx
        self.y = self.ny
