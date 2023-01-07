import pygame
from misc.constants import*
from .FEN import fen_to_board
from misc.miscellaneous import *


class Board:
    '''Class representing a checkers board'''

    def __init__(self, fen):
        '''Initialising the board'''
        self.board = []

        strings = fen.split(' ')
        board_fen = strings[0]
        turn = strings[1]
        castle = strings[2]
        enpassant = strings[3]
        # halfmoves = strings[4]
        # fullmoves = strings[5]

        # Keep track of king locations
        self.whiteKingLocation = None
        self.blackKingLocation = None

        self.blackQueenSideCastle = False
        self.whiteQueenSideCastle = False
        self.blackKingSideCastle = False
        self.whiteKingSideCastle = False

        for char in castle:
            if char == "K":
                self.whiteKingSideCastle = True
            elif char == "k":
                self.blackKingSideCastle = True
            elif char == "Q":
                self.whiteQueenSideCastle = True
            elif char == "q":
                self.blackQueenSideCastle = True

        self.p_piece = 0

        if turn == "w":
            self.turn = white_piece
        elif turn == "b":
            self.turn = black_piece

        for row in range(ROWS):
            temp = [0]*8
            self.board.append(temp)

        fen_to_board(board_fen, self.board)

        self.update_king_position()

        if enpassant != "-":
            pos = stdPositionsToRowCol(enpassant)
            piece = self.get_piece(pos)
            if piece.type == pawn:
                piece.enPassant = True

    def draw_squares(self, win):
        '''Draw the squares of the board'''
        win.fill(DARK_SQUARES)
        for row in range(ROWS):
            for col in range(COLS):
                if row % 2 == col % 2:
                    pygame.draw.rect(
                        win, LIGHT_SQUARES, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        self.draw(win)

    def draw(self, win):
        '''Method to draw the pieces of the board'''
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def move(self, startPos, endPos):
        '''Move a piece of the board, and update the king position, possible castles, en passant captures'''
        x1, y1 = startPos
        x2, y2 = endPos
        piece = self.get_piece((startPos))

        # Update king position
        if piece.type == king:
            if piece.color == white_piece:
                self.whiteKingLocation = endPos
            else:
                self.blackKingLocation = endPos

        # Check if it is a castling move
        if piece.type == king:
            if abs(y2-y1) == 2:
                if y2-y1 > 0:
                    self.board[x2][7].move((x2, 5))
                    self.board[x2][7], self.board[x2][5] = self.board[x2][5], self.board[x2][7]
                else:
                    self.board[x2][0].move((x2, 3))
                    self.board[x2][0], self.board[x2][3] = self.board[x2][3], self.board[x2][0]

        # Check for en passant
        if piece.type == pawn:
            if abs(x2-x1) == 2:
                piece.en_passant = True
            elif abs(x1-x2) == abs(y2-y1):
                do_en_passant(self, (startPos, endPos))

        if self.p_piece != 0:
            if self.p_piece != 0:
                if self.p_piece.type == pawn:
                    self.p_piece.en_passant = False

        if piece.type == king or piece.type == rook:
            piece.castle = False
        self.p_piece = piece
        piece.move(endPos)
        self.board[x1][y1], self.board[x2][y2] = 0, self.board[x1][y1]

    def unmove(self, origin, dest, cap_piece, enPassantPiece, enPassant, p_piece):
        x1, y1 = origin
        x2, y2 = dest
        o_piece = self.get_piece(dest)
        o_piece.move(origin)
        if o_piece.type == king:
            if o_piece.color == white_piece:
                self.whiteKingLocation = origin
            else:
                self.blackKingLocation = origin

        # Check for castle move
        if o_piece.type == king and abs(y2-y1) == 2:
            if y2 == 2:
                tp = self.get_piece((x2, 3))
                tp.move((x2, 0))
                self.board[x2][0], self.board[x2][3] = self.board[x2][3], self.board[x2][0]
                o_piece.castle = True
                tp.castle = True
            elif y2 == 6:
                tp = self.get_piece((x2, 5))
                tp.move((x2, 7))
                self.board[x2][7], self.board[x2][5] = self.board[x2][5], self.board[x2][7]
                o_piece.castle = True
                tp.castle = True

        # Replace "eaten" piece
        if cap_piece != 0:
            cap_piece.move(dest)

        if enPassantPiece != 0:
            enPassantPiece.move((x1, y2))
            enPassantPiece.en_passant = True
            self.board[x1][y2] = enPassantPiece

        self.p_piece = p_piece

        # Reset en passant for last piece
        if enPassant == True:
            self.p_piece.en_passant = True
        else:
            if o_piece.type == pawn:
                o_piece.en_passant = False

        self.board[x1][y1], self.board[x2][y2] = o_piece, cap_piece

    def get_pieces(self, color):
        '''Return array of pieces of color color'''
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    if piece.color == color:
                        pieces.append(piece)

        return pieces

    def update_king_position(self):
        '''Looks for kings on the board to update their respective positions'''
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece((row, col))
                if piece != 0:
                    if piece.type == king:
                        if piece.color == white_piece:
                            self.whiteKingLocation = (row, col)
                        else:
                            self.blackKingLocation = (row, col)

    def reset_pins(self, pieces):
        for piece in pieces:
            piece.pinned = False

    def get_piece(self, pos):
        '''Get piece on board[row][col]'''
        if pos[0] < 0 or pos[1] < 0 or pos[0] > 7 or pos[1] > 7:
            return None
        return self.board[pos[0]][pos[1]]
    
    def __repr__(self) -> str:
        "Method to print out the board"
        board = ''
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0:
                    temp = self.board[row][col].__repr__()
                    board += temp
                    board += ' '
                else:
                    board += str(self.board[row][col])
                    board += ' '
            board += '\n'

        return board + "\n"
