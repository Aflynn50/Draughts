import pygame, sys, os
from pygame.locals import *
import Core

class Menu():

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.displaySurf = pygame.display.set_mode((400, 400))
        self.displaySurf.fill((100, 100, 100))
        self.FPS = 60
        self.FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption("Welcome to Draughts")
        self.button1 = pygame.Rect(0, 0, 400, 200)
        self.button2 = pygame.Rect(0, 200, 400, 200)
        self.my_font = pygame.font.SysFont("liberationmono", 80)
        self.mouse_pos = (0, 0)

        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    self.mouse_pos = event.pos
                    if self.button1.collidepoint(self.mouse_pos):
                        x = Core.Game()
                        x.run()
                elif self.button2.collidepoint(self.mouse_pos):
                    x = Core.Game()
                    x.replay(self.log_num_entry())

            self.draw()
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)

    def draw(self):
        pygame.draw.rect(self.displaySurf, (255, 255, 255), self.button1)
        pygame.draw.rect(self.displaySurf, (200, 200, 200), self.button2)
        self.displaySurf.blit(self.my_font.render("Play", 1, (0, 0, 0)), (100, 50))
        self.displaySurf.blit(self.my_font.render("Replay", 1, (0, 0, 0)), (55, 250))

    def log_num_entry(self):
        pygame.event.clear()
        num = ""
        boxColour = (255, 255, 255)
        while True:
            for event in pygame.event.get():  # Checks what keys have been pressed
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == pygame.K_RETURN and len(num) > 0:  # Checks if there is anything written in the box when they press enter
                        if os.path.isfile(os.path.join("Games/log" + str(num) + ".txt")):
                            return int(num)
                        else:
                            boxColour = (255, 150, 150)
                    elif event.key == pygame.K_BACKSPACE:
                        boxColour = (255, 255, 255)
                        num = num[:(len(num) - 1)]
                    elif len(num) < 4 and event.key >= 48 and event.key <= 57:
                        boxColour = (255, 255, 255)
                        num += chr(event.key).capitalize()
            self.displaySurf.fill((200, 200, 200))
            self.displaySurf.blit(self.my_font.render("Enter", 1, (0, 0, 0)), (90, 20))
            self.displaySurf.blit(self.my_font.render("log", 1, (0, 0, 0)), (130, 100))
            self.displaySurf.blit(self.my_font.render("number", 1, (0, 0, 0)), (65, 180))
            pygame.draw.rect(self.displaySurf, boxColour, (80, 280, self.my_font.size("AAAAA")[0], self.my_font.size("AAAAA")[1]))
            self.displaySurf.blit(self.my_font.render(num, 1, (0, 0, 0)), (85, 285))
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)





if __name__ == "__main__":
    menu = Menu()