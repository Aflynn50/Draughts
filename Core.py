# Notes:
# Must capture is on
# Coordinates are x,y unless being used to access place on board where they are y,x
import copy
import pygame, sys
from pygame.locals import *
from pygame import gfxdraw


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
        pygame.display.set_caption("Draughts")

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
                    if self.selectedPiece:  # Checks if a piece is currently selected
                        if self.board.makeMove(self.selectedPiece, self.getMouseBox(event.pos)):  # Checks if where the user has clicked is a valid move for that piece and if it is makes that move
                            self.changeTurn(None)  # Swaps the turn
                            self.selectedPiece = None  # Deselects the piece
                            self.board.checkForKings()
                            winner = self.board.checkForWinner()
                            if winner:
                                self.win(winner)
                                return

                    if self.board.validSelection(self.getMouseBox(event.pos)):  # Checks if where they have clicked is a piece that can be selected, selects it if it is
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

    def win(self, colour):  # Colour is either "w" or "b"
        pygame.display.set_caption(colour + " wins")
        while True:
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    return
            self.board.draw(self.displaySurf, (0, 0), None)
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)





class Board:

    def __init__(self, board):
        if type(board) is not list:
            self.board = [["", "", "", "", "", "", "", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", ""],
                     ["", "", "", "", "", "b:k", "", "", "", ""],
                     ["", "", "", "", "w:m", "", "w:m", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", ""],
                     ["", "", "", "", "w:m", "", "w:m", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", ""]]

    def makeMove(self, selectedPiece, currentClickBox):  # Checks if the user has made a move and makes it, also returns whether a move has been made or not
        if self.board[selectedPiece[1]][selectedPiece[0]].split(":")[0] == PLAYERCOLOUR:
            moves = self.getMoves(selectedPiece)
            if moves:
                for move in moves:  # Each move here will be a list of the position the piece goes through to make the move
                    if move[-1] == currentClickBox:
                        self.move(move)  # Passes the list of moves to the move function
                        return True
        return False

    def move(self, moves):  # moves the piece through the list of moves and removes piece that have been captured
        if len(moves) > 1:
            start = moves[0]
            end = moves[-1]
            temp = str(self.board[start[1]][start[0]])
            self.board[start[1]][start[0]] = ""
            self.board[end[1]][end[0]] = temp

            if abs(start[0] - end[0]) > 1 or abs(start[1] - end[1]) > 1:  # Checks if the move jumps over another piece
                for i in range(len(moves) - 1):
                    pieceToRemove = [int((moves[i][0] + moves[i + 1][0])/2), int((moves[i][1] + moves[i + 1][1])/2)]
                    self.board[pieceToRemove[1]][pieceToRemove[0]] = ""



    def getMoves(self, pos):
        self.moves = []  # A list which contains lists of coordinates that the piece visits to make a the move (including start location)
        self.piece = self.board[pos[1]][pos[0]]
        if self.piece.split(":")[1] == "k":
            self.moveset = [[1, 1], [-1, -1], [1, -1], [-1, 1]]
        elif self.piece.split(":")[0] == "b":
            self.moveset = [[1, 1], [-1, 1]]
        elif self.piece.split(":")[0] == "w":
            self.moveset = [[-1, -1], [1, -1]]

        for i in self.moveset:  # Checks for a normal move
            try:
                if self.board[pos[1] + i[1]][pos[0] + i[0]] == "":
                    self.moves.append([[pos[0], pos[1]], [pos[0] + i[0], pos[1] + i[1]]])
            except IndexError:
                pass

        if self.piece.split(":")[0] == "w":
            opposite = "b"
        else:
            opposite = "w"

        self.moveRecersion([[pos[0], pos[1]]], opposite)

        return self.moves

    def moveRecersion(self, positions, opposite):  # Finds all the moves that involve capturing other pieces including ones that capture multiple pieces
        currentPos = positions[-1]
        for i in self.moveset:
            try:
                if self.board[currentPos[1] + (i[1] * 2)][currentPos[0] + (i[0] * 2)] == "" and self.board[currentPos[1] + i[1]][currentPos[0] + i[0]].split(":")[0] == opposite and [currentPos[0] + (i[0] * 2), currentPos[1] + (i[1] * 2)] not in positions:
                    #  Checks if move lands on blank square, checks it is capturing an enemy piece, checks the square the piece is moving to has not already been visited
                    self.moves.append(positions + [[currentPos[0] + (i[0] * 2), currentPos[1] + (i[1] * 2)]])  # adds the new chain of moves to the move list
                    positions.append([currentPos[0] + (i[0] * 2), currentPos[1] + (i[1] * 2)])
                    self.moveRecersion(positions, opposite)
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
                self.board[0][pieceidx] = "w:k"
            if self.board[-1][pieceidx].split(":")[0] == "b":
                self.board[-1][pieceidx] = "b:k"


    def validSelection(self, pos):
        if self.board[pos[1]][pos[0]].split(":")[0] == PLAYERCOLOUR:
            return True
        return False

    def draw(self, surface, mousePos, selectedPiece):  # Selected piece can be none, mousePos is used if no piece is selected and will highlight the square
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
                        pygame.gfxdraw.aacircle(surface, (int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2)), int(sqSize * 0.4), (0, 0, 0))
                        pygame.gfxdraw.filled_circle(surface, (int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2)), int(sqSize * 0.4), (0, 0, 0))

                        if x.split(":")[1] == "k":
                            pygame.gfxdraw.aacircle(surface, (int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2)), int(sqSize * 0.15), (255, 255, 255))
                            pygame.gfxdraw.filled_circle(surface, (int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2)), int(sqSize * 0.15), (255, 255, 255))

                    elif x.split(":")[0] == "w":
                        pygame.gfxdraw.aacircle(surface, (int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2)), int(sqSize * 0.4), (255, 255, 255))
                        pygame.gfxdraw.filled_circle(surface, (int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2)), int(sqSize * 0.4), (255, 255, 255))

                        if x.split(":")[1] == "k":
                            pygame.gfxdraw.aacircle(surface, (int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2)), int(sqSize * 0.15), (0, 0, 0))
                            pygame.gfxdraw.filled_circle(surface, (int(xnum * sqSize) + int(sqSize / 2)), (int(ynum * sqSize) + int(sqSize / 2)), int(sqSize * 0.15), (0, 0, 0))

                xnum += 1
            ynum += 1


        if selectedPiece:
            moves = self.getMoves(selectedPiece)
            print(moves)

            for move in moves:
                yellowBox = pygame.Surface((sqSize, sqSize), pygame.SRCALPHA)
                yellowBox.fill((70, 70, 255, 192))
                surface.blit(yellowBox, (move[-1][0] * sqSize, move[-1][1] * sqSize))

        elif self.board[mousePos[1]][mousePos[0]].split(":")[0] == PLAYERCOLOUR:
            moves = self.getMoves(mousePos)
            print(moves)

            for move in moves:
                yellowBox = pygame.Surface((sqSize, sqSize), pygame.SRCALPHA)
                yellowBox.fill((100, 100, 255, 128))
                surface.blit(yellowBox, (move[-1][0] * sqSize, move[-1][1] * sqSize))

game = Game()
