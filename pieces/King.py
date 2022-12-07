import pygame
from .piece import Piece
from misc.constants import orthogonal_squares, diagonal_squares, pos_getter, king, rook, white_piece, black_piece


class King(Piece):
    def __init__(self, number, row, col):
        super().__init__(number, row, col)

    def find_moves(self, board):
        '''Find move for the piece'''
        moves = []
        for direction in orthogonal_squares + diagonal_squares:
            for i in range(1, 2):
                if self.position + direction*i < 0 or self.position + direction*i > 63:
                    break
                if abs(direction) == 1:
                    if direction*i + self.col < 0 or direction*i + self.col > 7:
                        break
                pos = self.position + direction*i
                move = pos_getter[pos]
                piece = board[move[0]][move[1]]
                if (direction == -7 or direction == 9) and move[1] < self.col:
                    break
                elif (direction == 7 or direction == -9) and move[1] > self.col:
                    break
                if piece != 0:
                    if piece.color != self.color:
                        moves.append(move)
                        break
                    else:
                        break
                else:
                    moves.append(move)

        return moves
