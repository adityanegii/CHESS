from misc.constants import *
from pieces.Pawn import Pawn
from pieces.Knight import Knight
from pieces.Bishop import Bishop
from pieces.Rook import Rook
from pieces.Queen import Queen
from pieces.King import King
from misc.miscellaneous import get_key


def fen_to_board(fen_notation, board):
    '''Function to transform standard fen string into board representation'''
    row = 0
    col = 0

    for char in fen_notation:
        if char == '/':
            row += 1
            col = 0
        elif char.isnumeric() == True:
            col += int(char)
        elif char.isalpha() == True:
            if char.isupper():
                if char == 'P':
                    temp = Pawn(symbol2num.get(char.lower())
                                * white_piece, row, col)
                if char == 'K':
                    temp = King(symbol2num.get(char.lower())
                                * white_piece, row, col)
                if char == 'N':
                    temp = Knight(symbol2num.get(char.lower())
                                  * white_piece, row, col)
                if char == 'B':
                    temp = Bishop(symbol2num.get(char.lower())
                                  * white_piece, row, col)
                if char == 'Q':
                    temp = Queen(symbol2num.get(char.lower())
                                 * white_piece, row, col)
                if char == 'R':
                    temp = Rook(symbol2num.get(char.lower())
                                * white_piece, row, col)
                board[row][col] = temp
            else:
                if char == 'p':
                    temp = Pawn(symbol2num.get(char.lower())
                                * black_piece, row, col)
                if char == 'k':
                    temp = King(symbol2num.get(char.lower())
                                * black_piece, row, col)
                if char == 'n':
                    temp = Knight(symbol2num.get(char.lower())
                                  * black_piece, row, col)
                if char == 'b':
                    temp = Bishop(symbol2num.get(char.lower())
                                  * black_piece, row, col)
                if char == 'q':
                    temp = Queen(symbol2num.get(char.lower())
                                 * black_piece, row, col)
                if char == 'r':
                    temp = Rook(symbol2num.get(char.lower())
                                * black_piece, row, col)
                board[row][col] = temp

            col += 1


def board_to_fen(board):
    fen_string = ''

    for row in board:
        counter = 0
        for piece in row:
            if piece == 0:
                counter += 1
            else:
                if counter != 0:
                    fen_string += str(counter)
                    counter = 0
                if piece.color == white_piece:
                    fen_string += get_key(symbol2num, piece.type).upper()
                else:
                    fen_string += get_key(symbol2num, piece.type)
        if counter != 0:
            fen_string += str(counter) + "/"
        else:
            fen_string += "/"

    return fen_string[:-1] + '\n'
