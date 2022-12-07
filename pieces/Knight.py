import pygame
from .piece import Piece
from misc.miscellaneous import knight_moves, normalize_moves


class Knight(Piece):
    def __init__(self, number, row, col):
        super().__init__(number, row, col)

    def find_moves(self, board):
        '''Find move for the piece'''
        return knight_moves(self, board)
