import pygame

from src.Config import Config
from src.Grid import Grid


class Game:
    def __init__(self, display):
        self.display = display
        self.grid = Grid(display)

    def loop(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        self.grid.insert_source(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


                # print(event)

            self.grid.loop()
            self.grid.draw()

            pygame.display.update()
            clock.tick(Config['game']['fps'])
