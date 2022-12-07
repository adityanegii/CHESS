import pygame
from .constants import *


def get_key(dict, value):
    for key, val in dict.items():
        if val == value:
            return key


def normalize_moves(moves, piece, board):
    '''Find out of board moves'''
    legal_moves = []
    for move in moves:
        x, y = move
        if x in range(8) and y in range(8):
            if board[x][y] != 0:
                if board[x][y].color != piece.color:
                    legal_moves.append(move)
            else:
                legal_moves.append(move)

    return legal_moves


def knight_moves(piece, board):
    '''Function to get moves for knights'''
    r, c = piece.row, piece.col
    t_moves = k_moves
    moves = []
    for move in t_moves:
        moves.append((r+move[0], c+move[1]))

    return normalize_moves(moves, piece, board)


def do_en_passant(board, move):
    '''Function checks if an en passant capture was made and removes the capture pawn from the board'''
    origin, dest = move
    originR, originC = origin
    destR, destC = dest
    if abs(destR-originR) == abs(destC-originC):
        pot_piece = board.get_piece((originR, destC))
        cap_piece = board.get_piece((originR, originC))

        if pot_piece != 0:
            if pot_piece.type == pawn and pot_piece.color != cap_piece.color:
                if pot_piece.en_passant == True:
                    board.board[originR][destC] = 0

def check_for_en_passant(board, move):
    """Function checks whether a move is en passant"""
    origin, dest = move
    originR, originC = origin
    destR, destC = dest
    if abs(destR-originR) == abs(destC-originC):
        pot_piece = board.get_piece((originR, destC))
        cap_piece = board.get_piece((originR, originC))

        if pot_piece != 0:
            if pot_piece.type == pawn and pot_piece.color != cap_piece.color:
                if pot_piece.en_passant == True:
                    return True

def rowColToStdPositions(pos):
    row, col = pos
    x = str(8-row)
    y = colToLetter.get(col)
    return y+x


def stdPositionsToRowCol(pos):
    col = ord(pos[0]) - 97
    row = 8 - int(pos[1])
    return (row, col)
