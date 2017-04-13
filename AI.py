

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


    def movePiece(self, piece, move):
        pieceType = self.board[piece[1]][piece[0]].split(":")
        if self.board[piece[1]][piece[0]] != "":
            if pieceType[1] == "k":
                if self.board[][]

            elif pieceType[1] == "m":
                if pieceType[0] == "b":
                    if self.board[]

                elif pieceType[0] == "w":
                    pass

    def getMoves(self, pos):
        moves = []
        piece = self.board[pos[1]][pos[0]]
        capture = []
        if piece != "":
            return "That is not a valid piece"
        elif piece.split(":")[1] == "k":
            try:
                if self.board[pos[1] + 1][pos[0] - 1] == "":
                    moves.append([pos[0] - 1, pos[1] + 1])
                else:
                    if self.board[pos[1] + 2][pos[0] - 2] == "" and self.board[pos[1] + 1][pos[0] - 1].split(":")[0] != piece.split(":")[0]:
                        moves.append([pos[0] - 2, pos[1] + 2])
                        capture.append([pos[0] - 1, pos[1] + 1])
            except IndexError:
                pass
            try:
                if self.board[pos[1] + 1][pos[0] + 1] == "":
                    moves.append([pos[0] - 1, pos[1] + 1])
                else:
                    if self.board[pos[1] + 2][pos[0] + 2] == "" and self.board[pos[1] + 1][pos[0] + 1].split(":")[0] != piece.split(":")[0]:
                        moves.append([pos[0] + 2, pos[1] + 2])
                        capture = True
            except IndexError:
                pass
            try:
                if self.board[pos[1] - 1][pos[0] - 1] == "":
                    moves.append([pos[0] - 1, pos[1] - 1])
                else:
                    if self.board[pos[1] - 2][pos[0] - 2] == "" and self.board[pos[1] - 1][pos[0] - 1].split(":")[0] != piece.split(":")[0]:
                        moves.append([pos[0] - 2, pos[1] - 2])
                        capture = True
            except IndexError:
                pass
            try:
                if self.board[pos[1] - 1][pos[0] + 1] == "":
                    moves.append([pos[0] + 1, pos[1] - 1])
                else:
                    if self.board[pos[1] - 2][pos[0] + 2] == "" and self.board[pos[1] - 1][pos[0] + 1].split(":")[0] != piece.split(":")[0]:
                        moves.append([pos[0] + 2, pos[1] - 2])
                        capture = True
            except IndexError:
                pass



        elif piece.split(":")[1] == "m":
            if piece.split(":")[0] == "b":
                try:
                    if self.board[pos[1] + 1][pos[0] - 1] == "":
                        moves.append([pos[0] - 1, pos[1] + 1])
                    else:
                        if self.board[pos[1] + 2][pos[0] - 2] == "" and self.board[pos[1] + 1][pos[0] - 1].split(":")[0] != piece.split(":")[0]:
                            moves.append([pos[0] - 2, pos[1] + 2])
                            capture = True
                except IndexError:
                    pass
                try:
                    if self.board[pos[1] + 1][pos[0] + 1] == "":
                        moves.append([pos[0] - 1, pos[1] + 1])
                    else:
                        if self.board[pos[1] + 2][pos[0] + 2] == "" and self.board[pos[1] + 1][pos[0] + 1].split(":")[0] != piece.split(":")[0]:
                            moves.append([pos[0] + 2, pos[1] + 2])
                            capture = True
                except IndexError:
                    pass

            elif piece.split(":")[0] == "w":
                try:
                    if self.board[pos[1] - 1][pos[0] - 1] == "":
                        moves.append([pos[0] - 1, pos[1] - 1])
                    else:
                        if self.board[pos[1] - 2][pos[0] - 2] == "" and self.board[pos[1] - 1][pos[0] - 1].split(":")[0] != piece.split(":")[0]:
                            moves.append([pos[0] - 2, pos[1] - 2])
                            capture = True
                except IndexError:
                    pass
                try:
                    if self.board[pos[1] - 1][pos[0] + 1] == "":
                        moves.append([pos[0] + 1, pos[1] - 1])
                    else:
                        if self.board[pos[1] - 2][pos[0] + 2] == "" and self.board[pos[1] - 1][pos[0] + 1].split(":")[0] != piece.split(":")[0]:
                            moves.append([pos[0] + 2, pos[1] - 2])
                            capture = True
                except IndexError:
                    pass


        def take(pos):


        if 0 <= move_pos[0] <= 7 and 0 <= move_pos[1] <= 7:
            pass


for i in [[1, 1], [-1, -1], [1, -1], [-1, 1]]:
    try:
        if self.board[pos[1] + i][pos[0] + 1] == "":
            moves.append([pos[0] - 1, pos[1] + 1])
    except IndexError:
        pass