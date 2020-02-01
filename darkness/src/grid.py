import math
from collections import deque
from random import random

import pygame

from darkness.src.config import Config


def tab_copy(tab):
    return [row.copy() for row in tab]


class Grid:

    def __init__(self, display):
        self.display = display
        self.x_size = math.floor(Config['game']['width'] / Config['game']['cell_size'])
        self.y_size = math.floor(Config['game']['height'] / Config['game']['cell_size'])

        self.empty_power = []
        self.empty_dirs = [[0] * self.y_size for _ in range(self.x_size)]  # matrix filled with zeroes

        self.queue = deque()

        # state matrix init: x_size by y_size 2d matrix of 0s with border of -1s
        self.empty_power.append([-1] * self.y_size)
        tmp = [0] * self.y_size
        tmp[0] = -1
        tmp[self.y_size - 1] = -1
        for _ in range(self.x_size - 2):
            self.empty_power.append(tmp.copy())
        self.empty_power.append([-1] * self.y_size)

        # initial state
        for x in range(10, 30):
            for y in range(20, 24):
                self.empty_power[x][y] = -1

        self.power = tab_copy(self.empty_power)
        self.dirs = tab_copy(self.empty_dirs)

        self.power[5][5] = 1
        self.dirs[5][5] = 15

    def draw(self):
        for x in range(self.x_size):
            for y in range(self.y_size):
                val = self.power[x][y]
                pygame.draw.rect(
                    self.display,
                    Config['colors'][val] if val <= 0 else (val * 200, val * 200, val * 200),
                    [
                        x * Config['game']['cell_size'],
                        y * Config['game']['cell_size'],
                        Config['game']['cell_size'],
                        Config['game']['cell_size']
                    ]
                )

    def insert_source(self, x, y):
        x //= Config['game']['cell_size']
        y //= Config['game']['cell_size']
        self.queue.append((x, y))

    def loop(self):
        next_dirs = tab_copy(self.empty_dirs)
        next_power = tab_copy(self.empty_power)

        while self.queue:
            x, y = self.queue.popleft()
            if self.empty_dirs[x][y] != -1:
                self.dirs[x][y] = 15
                self.power[x][y] = 1

        # pprint(self.dirs)

        for x in range(1, self.x_size - 1):
            for y in range(1, self.y_size - 1):
                for _right, _down, _left, _up, _dx, _dy in (
                        (1, 2, 4, 8, 1, 0),  # 4 consecutive rotations
                        (2, 4, 8, 1, 0, 1),
                        (4, 8, 1, 2, -1, 0),
                        (8, 1, 2, 4, 0, -1)
                ):
                    if self.dirs[x][y] & _right:
                        distorted_power = (0.9 + random() * 0.1) * (self.power[x][y] - Config['game']['epsilon'])
                        # wall
                        if self.power[x + _dx][y + _dy] == -1:
                            next_dirs[x][y] |= _left
                            next_power[x][y] = max(next_power[x][y], distorted_power, 0)
                        else:
                            next_dirs[x + _dx][y + _dy] |= _right
                            next_power[x + _dx][y + _dy] = max(next_power[x + _dx][y + _dy], distorted_power, 0)
                        # pointed to the right explicitly
                        if not (self.dirs[x][y] ^ _right):
                            if self.power[x + _dy][y - _dx] == -1:
                                next_dirs[x][y] |= _down
                                next_power[x][y] = max(next_power[x][y], distorted_power, 0)
                            else:
                                next_dirs[x + _dy][y - _dx] |= _up
                                next_power[x + _dy][y - _dx] = max(next_power[x + _dy][y - _dx], distorted_power, 0)
                            if self.power[x - _dy][y + _dx] == -1:
                                next_dirs[x][y] |= _up
                                next_power[x][y] = max(next_power[x][y], distorted_power, 0)
                            else:
                                next_dirs[x - _dy][y + _dx] |= _down
                                next_power[x - _dy][y + _dx] = max(next_power[x - _dy][y + _dx], distorted_power, 0)

        # self.curr_n, next_n = next_n, self.curr_n
        # self.curr_d, next = next, self.curr_d
        # self.curr_n = next_n
        self.dirs = next_dirs
        self.power = next_power
