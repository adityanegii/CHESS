import pygame
from .piece import Piece
from misc.constants import diagonal_squares, pos_getter


class Bishop(Piece):
    def __init__(self, number, row, col):
        super().__init__(number, row, col)

    def find_moves(self, board):
        '''Find move for the piece'''
        moves = []
        for direction in diagonal_squares:
            for i in range(1, 8):
                if self.position + direction*i < 0 or self.position + direction*i > 63:
                    break
                pos = self.position + direction*i
                move = pos_getter[pos]
                if (direction == -7 or direction == 9) and move[1] < self.col:
                    break
                elif (direction == 7 or direction == -9) and move[1] > self.col:
                    break
                piece = board[move[0]][move[1]]
                if piece != 0:
                    if piece.color != self.color:
                        moves.append(move)
                        break
                    else:
                        break
                else:
                    moves.append(move)

        return moves
