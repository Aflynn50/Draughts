# Notes:
# Must capture is on
# Coordinates are x,y unless being used to access place on board where they are y,x
import copy
import pygame, sys
from pygame.locals import *


PLAYERCOLOUR = "b"
SCREENSIZE = 400
if SCREENSIZE % 8 != 0:
    print("Invalid screen size")

class Game:
    def __init__(self):
        pygame.init()
        self.displaySurf = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))
        self.displaySurf.fill((100, 100, 100))
        self.board = Board("")
        self.FPS = 60
        self.FPSCLOCK = pygame.time.Clock()
        self.mousePos = [0, 0]
        self.selectedPiece = None

        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEMOTION:
                    self.mousePos = event.pos
                if event.type == MOUSEBUTTONUP:
                    if self.selectedPiece:
                        if self.board.makeMove(self.selectedPiece, self.getMouseBox(event.pos)):
                            self.changeTurn(None)  # Swaps the turn
                            self.selectedPiece = None
                    if self.board.validSelection(self.getMouseBox(event.pos)):
                        self.selectedPiece = self.getMouseBox(event.pos)
                    else:
                        self.selectedPiece = None

            mouseBoxPos = self.getMouseBox(self.mousePos)
            self.board.draw(self.displaySurf, mouseBoxPos, self.selectedPiece)
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)

    def getMouseBox(self, mousePos):
        return [int(mousePos[0]/(SCREENSIZE / 8)), int(mousePos[1]/(SCREENSIZE / 8))]

    def changeTurn(self, turn):  # Changes the turn to a requested colour or sawps it if no colour specified
        global PLAYERCOLOUR
        if turn == "w":
            PLAYERCOLOUR = "w"
        elif turn == "b":
            PLAYERCOLOUR = "b"
        else:
            if PLAYERCOLOUR == "w":
                PLAYERCOLOUR = "b"
            elif PLAYERCOLOUR == "b":
                PLAYERCOLOUR = "w"


class Board:

    def __init__(self, board):
        if type(board) is not list:
            self.board = [["", "b:m", "", "b:m", "", "b:m", "", "b:m", "", "b:m"],
                     ["b:m", "", "b:m", "", "b:m", "", "b:m", "", "b:m", ""],
                     ["", "b:m", "", "b:m", "", "b:m", "", "b:m", "", "b:m"],
                     ["", "", "", "", "", "", "", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", ""],
                     ["w:m", "", "w:m", "", "w:m", "", "w:m", "", "w:m", ""],
                     ["", "w:m", "", "w:m", "", "w:m", "", "w:m", "", "w:m"],
                     ["w:m", "", "w:m", "", "w:m", "", "w:m", "", "w:m", ""]]

    def makeMove(self, selectedPiece, currentClickBox):  # Checks if the user has made a move and makes it, also returns whether a move has been made or not
        if self.board[selectedPiece[1]][selectedPiece[0]].split(":")[0] == PLAYERCOLOUR:
            moves, captureMoves = self.getMoves(selectedPiece)
            if moves:
                for move in moves:
                    if move == currentClickBox:
                        self.move(selectedPiece, currentClickBox)
                        return True
            if captureMoves:
                for move in captureMoves:
                    if move[0] == currentClickBox:
                        self.move(selectedPiece, currentClickBox)
                        return True
        return False

    def getMoves(self, pos):
        moves = []  # Coordinates of the move x, y
        self.piece = self.board[pos[1]][pos[0]]
        captureMoves = []  # Each move in here is the move position and a list of pieces that are captured
        if self.piece.split(":")[1] == "k":
            self.moveset = [[1, 1], [-1, -1], [1, -1], [-1, 1]]
        elif self.piece.split(":")[0] == "b":
            self.moveset = [[1, 1], [-1, 1]]
        elif self.piece.split(":")[0] == "w":
            self.moveset = [[-1, -1], [1, -1]]

        for i in self.moveset:
            try:
                if self.board[pos[1] + i[1]][pos[0] + i[0]] == "":
                    moves.append([pos[0] + i[0], pos[1] + i[1]])
            except IndexError:
                pass

        capPos = (pos[0], pos[1])
        capList = []
        self.captureMoves = []
        self.captureRecursion(capList, capPos)
        return [moves, self.captureMoves]

    def captureRecursion(self, capList, capPos):
        if self.piece.split(":")[0] == "w":
            opposite = "b"
        else:
            opposite = "w"
        for i in self.moveset:
            try:
                if self.board[capPos[1] + (i[1] * 2)][capPos[0] + (i[0] * 2)] == "" and self.board[capPos[1] + i[1]][capPos[0] + i[0]].split(":")[0] == opposite and [capPos[0] + (i[0]), capPos[1] + (i[1])] not in capList:
                    #  Checks if move lands on blank square, checks it is capturing an enemy piece, checks the move it is making is not one that has already been checked
                    capList.append([capPos[0] + (i[0]), capPos[1] + (i[1])])
                    self.captureRecursion(capList, (capPos[0] + (i[0] * 2), capPos[1] + (i[1] * 2)))
                    self.captureMoves.append([[capPos[0] + (i[0] * 2), capPos[1] + (i[1] * 2)], capList])
            except IndexError:
                pass
        return

    def checkForWinner(self):
        blacks = 0
        whites = 0
        for row in self.board:
            for piece in row:
                if piece.split(":")[0] == "w":
                    whites += 1
                elif piece.split(":")[0] == "b":
                    blacks += 1
        if whites == 0:
            return "b"
        elif blacks == 0:
            return "w"
        else:
            return None

    def checkForKings(self):
        for pieceidx in range(len(self.board[0])):
            if self.board[0][pieceidx].split(":")[0] == "w":
                self.board


    def move(self, piece, pos):
        self.moves, self.captureMoves = self.getMoves(piece)
        if self.moves:
            if pos in self.moves:
                temp = str(self.board[piece[1]][piece[0]])
                self.board[piece[1]][piece[0]] = ""
                self.board[pos[1]][pos[0]] = temp
        if self.captureMoves:
            for move in self.captureMoves:
                if move[0] == pos:
                    temp = str(self.board[piece[1]][piece[0]])
                    self.board[piece[1]][piece[0]] = ""
                    self.board[pos[1]][pos[0]] = temp
                    for item in move[1]:
                        self.board[item[1]][item[0]] = ""

    def validSelection(self, pos):
        if self.board[pos[1]][pos[0]].split(":")[0] == PLAYERCOLOUR:
            return True
        return False

    def draw(self, surface, mousePos, selectedPiece):
        sqSize = SCREENSIZE / 8
        for row in range(8):
            if row % 2 == 0:
                pygame.draw.rect(surface, (200, 200, 200), (sqSize * 1, (row * sqSize), sqSize, sqSize))
                pygame.draw.rect(surface, (200, 200, 200), (sqSize * 3, (row * sqSize), sqSize, sqSize))
                pygame.draw.rect(surface, (200, 200, 200), (sqSize * 5, (row * sqSize), sqSize, sqSize))
                pygame.draw.rect(surface, (200, 200, 200), (sqSize * 7, (row * sqSize), sqSize, sqSize))
            else:
                pygame.draw.rect(surface, (200, 200, 200), (0, (row * sqSize), sqSize, sqSize))
                pygame.draw.rect(surface, (200, 200, 200), (sqSize * 2, (row * sqSize), sqSize, sqSize))
                pygame.draw.rect(surface, (200, 200, 200), (sqSize * 4, (row * sqSize), sqSize, sqSize))
                pygame.draw.rect(surface, (200, 200, 200), (sqSize * 6, (row * sqSize), sqSize, sqSize))

        ynum = 0
        for y in self.board:
            xnum = 0
            for x in y:
                if x != "":
                    if x.split(":")[0] == "b":
                        pygame.draw.circle(surface, (0, 0, 0), ((int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2))), int(sqSize * 0.4))
                    elif x.split(":")[0] == "w":
                        pygame.draw.circle(surface, (255, 255, 255), ((int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2))), int(sqSize * 0.4))
                xnum += 1
            ynum += 1

        moveOptions = []

        if selectedPiece:
            moves, captureMoves = self.getMoves(selectedPiece)
            if moves:
                for move in moves:
                    moveOptions.append(move)
            if captureMoves:
                for move in captureMoves:
                    moveOptions.append(move[0])

            for option in moveOptions:
                yellowBox = pygame.Surface((sqSize, sqSize), pygame.SRCALPHA)
                yellowBox.fill((70, 70, 255, 192))
                surface.blit(yellowBox, (option[0] * sqSize, option[1] * sqSize))

        elif self.board[mousePos[1]][mousePos[0]].split(":")[0] == PLAYERCOLOUR:
            moves, captureMoves = self.getMoves(mousePos)
            if moves:
                for move in moves:
                    moveOptions.append(move)
            if captureMoves:
                for move in captureMoves:
                    moveOptions.append(move[0])

            for option in moveOptions:
                yellowBox = pygame.Surface((sqSize, sqSize), pygame.SRCALPHA)
                yellowBox.fill((100, 100, 255, 128))
                surface.blit(yellowBox, (option[0] * sqSize, option[1] * sqSize))


game = Game()
