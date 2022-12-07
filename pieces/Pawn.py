import pygame
from .piece import Piece
from misc.constants import white_piece, black_piece, pawn
from misc.miscellaneous import normalize_moves


class Pawn(Piece):
    def __init__(self, number, row, col):
        super().__init__(number, row, col)
        self.en_passant = False

    def find_moves(self, board):
        '''Find move for the piece'''
        moves = []
        if board[self.row + self.color][self.col] == 0:
            moves.append((self.row + self.color, self.col))

        if board[self.row + self.color][self.col] == 0:
            # If pawn is on start square
            if (self.row == 6) and self.color == white_piece:
                if board[self.row + 2*self.color][self.col] == 0:
                    moves.append((self.row + self.color*2, self.col))
            elif (self.row == 1) and self.color == black_piece:
                if board[self.row + 2*self.color][self.col] == 0:
                    moves.append((self.row + self.color*2, self.col))

        # Capturing diagonaly
        if self.col == 0:
            piece = board[self.row + self.color][self.col + 1]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((self.row + self.color, self.col + 1))
        elif self.col == 7:
            piece = board[self.row + self.color][self.col - 1]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((self.row + self.color, self.col - 1))
        else:
            piece1 = board[self.row + self.color][self.col + 1]
            piece2 = board[self.row + self.color][self.col - 1]
            if piece1 != 0:
                if piece1.color != self.color:
                    moves.append((self.row + self.color, self.col + 1))
            if piece2 != 0:
                if piece2.color != self.color:
                    moves.append((self.row + self.color, self.col - 1))

        # Find en passant moves
        if self.col < 7:
            enp_piece1 = board[self.row][self.col + 1]
            if enp_piece1 != 0:
                if enp_piece1.color != self.color and enp_piece1.type == pawn:
                    if enp_piece1.en_passant == True:
                        moves.append((self.row + self.color, self.col + 1))

        if self.col > 0:
            enp_piece2 = board[self.row][self.col - 1]
            if enp_piece2 != 0:
                if enp_piece2.color != self.color and enp_piece2.type == pawn:
                    if enp_piece2.en_passant == True:
                        moves.append((self.row + self.color, self.col - 1))

        return moves
