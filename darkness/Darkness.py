import pygame

from src.Config import Config
from src.Game import Game


def main():
    display = pygame.display.set_mode((Config['game']['width'], Config['game']['height']))
    pygame.display.set_caption('Darkness')

    game = Game(display)
    game.loop()


if __name__ == '__main__':
    main()
