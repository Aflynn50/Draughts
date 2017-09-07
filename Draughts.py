import pygame, sys
from pygame.locals import *
import Core

class Menu():

    def __init__(self):
        pygame.init()
        self.displaySurf = pygame.display.set_mode((400, 400))
        self.displaySurf.fill((100, 100, 100))
        self.FPS = 60
        self.FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption("Draughts")
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)


if __name__ == "__main__":
    menu = Menu()