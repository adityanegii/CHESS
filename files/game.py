import pygame
from misc.constants import*
from misc.miscellaneous import *
from misc.Node import Node
from .board import Board
from .FEN import board_to_fen
from collections import deque
from pieces import Pawn, Knight, Bishop, Rook, Queen
from .MoveGenerator import MoveGenerator


class Game:
    def __init__(self, fen, win):
        self.board = Board(fen)
        self.turn = self.board.turn
        self.num_of_moves = 0
        self.win = win

        self.history = deque()
        # The move that was just made so it can be drawn on the board
        self.p_move = None
        self.check = self.find_danger(self.turn)

        self.whitePieces = self.get_pieces(white_piece)
        self.blackPieces = self.get_pieces(black_piece)

        # List of all possible moves ((originX, originY), (destX, destY))
        self.move_list = []

        # To keep track of castling
        self.blackQueenSideCastle = self.board.blackQueenSideCastle
        self.whiteQueenSideCastle = self.board.whiteQueenSideCastle
        self.blackKingSideCastle = self.board.blackKingSideCastle
        self.whiteKingSideCastle = self.board.whiteKingSideCastle

        self.blackThreatMap = []    # Squares black attacks
        self.whiteThreatMap = []    # Squares white attacks

        self.checkers = []
        
        self.blackThreatMap = []
        self.whiteThreatMap = []

        self.updateThreatMap()

        self.generate_all_moves()

        self.winner = None
        self.find_winner()

    def initializeThreatMap1(self):
        '''Initialize the threat maps for both black and white'''
        self.blackThreatMap = []
        self.whiteThreatMap = []
        for row in range(ROWS):
            tmpB = []
            tmpW = []
            for col in range(COLS):
                tmpB.append(0)
                tmpW.append(0)
            self.blackThreatMap.append(tmpB)
            self.whiteThreatMap.append(tmpW)

    def initializeThreatMap(self):
        '''Initialize the threat maps for both black and white'''
        if self.turn == white_piece:
            self.blackThreatMap = [0 for i in range(ROWS*COLS)]
        else:
            self.whiteThreatMap = [0 for i in range(ROWS*COLS)]

    def updateThreatMap(self):

        self.initializeThreatMap()

        if self.turn == black_piece:
            tMap = self.whiteThreatMap
            pieces = self.whitePieces
        else:
            tMap = self.blackThreatMap
            pieces = self.blackPieces
        
        checkers = []

        for piece in pieces:
            row, col = piece.row, piece.col
            pos = piece.position
            if piece.type == pawn:
                if col > 0:
                    if piece.color == white_piece:
                        tMap[pos-9] = 1
                        dest = self.get_piece_from_pos(pos-9)
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                checkers.append(piece)
                    else:
                        tMap[pos+7] = 1
                        dest = self.get_piece_from_pos(pos+7)
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                checkers.append(piece)
                if col < 7:
                    if piece.color == white_piece:
                        tMap[pos-7] = 1
                        dest = self.get_piece_from_pos(pos-7)
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                checkers.append(piece)
                    else:
                        tMap[pos+9] = 1
                        dest = self.get_piece_from_pos(pos+9)
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                checkers.append(piece)

            if piece.type == knight:
                t_moves = k_moves
                for move in t_moves:
                    x, y = move
                    x += row
                    y += col
                    n_pos = 8*x+y
                    if x >= 0 and y >= 0 and x <= 7 and y <= 7:
                        tMap[n_pos] = 1
                        dest = self.get_piece_from_pos(n_pos)
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                checkers.append(piece)
            if piece.type == king:
                if col > 0:
                    tMap[pos-1] = 1
                    if row > 0:
                        tMap[pos-9] = 1
                        tMap[pos-8] = 1
                    if row < 7:
                        tMap[pos+7] = 1
                        tMap[pos+8] = 1
                if col < 7:
                    tMap[pos+1] = 1
                    if row > 0:
                        tMap[pos-7] = 1
                        tMap[pos-8] = 1
                    if row < 7:
                        tMap[pos+9] = 1
                        tMap[pos+8] = 1
            if piece.type == bishop or piece.type == queen:
                start_rem = pos % 8
                for direction in diagonal_squares:
                    pot_pin = None
                    king_found = False
                    for i in range(1, 8):
                        n_pos = pos + i*direction
                        if n_pos not in range(0, 64):
                            break
                        if (n_pos) % 8 > start_rem and (direction == -9 or direction == 7):
                            break
                        if (n_pos) % 8 < start_rem and (direction == -7 or direction == 9):
                            break
                        dest = self.get_piece_from_pos(n_pos)
                        if dest != 0:
                            if pot_pin:
                                if dest.type == king and dest.color == self.turn:
                                    pot_pin.pinned = True
                                    break
                                else:
                                    break
                            else:
                                if king_found:
                                    if dest.color == self.turn:
                                        break
                                    else:
                                        tMap[n_pos] = 1
                                        break
                                tMap[n_pos] = 1
                                if dest.type == king and dest.color == self.turn:
                                    checkers.append(piece)
                                    king_found = True
                                elif dest.color == self.turn:
                                    if pot_pin:
                                        break
                                    else:
                                        pot_pin = dest
                                else:
                                    break
                        else:
                            if pot_pin is None:
                                tMap[n_pos] = 1
            if piece.type == rook or piece.type == queen:
                start_rem = pos % 8
                for direction in orthogonal_squares:
                    pot_pin = None
                    king_found = False
                    for i in range(1, 8):
                        n_pos = pos + i*direction
                        if n_pos not in range(0, 64):
                            break
                        if (n_pos) % 8 > start_rem and direction == -1:
                            break
                        if (n_pos) % 8 < start_rem and direction == 1:
                            break
                        dest = self.get_piece_from_pos(n_pos)
                        if dest != 0:
                            if pot_pin:
                                if dest.type == king and dest.color == self.turn:
                                    pot_pin.pinned = True
                                    break
                                else:
                                    break
                            else:
                                if king_found:
                                    if dest.color == self.turn:
                                        break
                                    else:
                                        tMap[n_pos] = 1
                                        break
                                tMap[n_pos] = 1
                                if dest.type == king and dest.color == self.turn:
                                    checkers.append(piece)
                                    king_found = True
                                elif dest.color == self.turn:
                                    if pot_pin:
                                        break
                                    else:
                                        pot_pin = dest
                                else:
                                    break
                        else:
                            if pot_pin is None:
                                tMap[n_pos] = 1
        
        self.check = 0
        if len(checkers) > 0:
            self.check = self.turn
        self.checkers = checkers

    def updateThreatMap1(self):
        '''Method to update the threat map with the proper values, get the checkers, determine whether there is a check, and find pinned pieces'''
        self.initializeThreatMap()
        checkers = []
        check = 0
        if self.turn == black_piece:
            for piece in self.whitePieces:
                r, c = piece.row, piece.col
                if piece.type == pawn:
                    if c-1 < 0:
                        self.whiteThreatMap[r+piece.color][c+1] = 1
                        dest = self.get_piece((r+piece.color, c+1))
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                check = self.turn
                                checkers.append(piece)
                    elif c+1 > 7:
                        self.whiteThreatMap[r+piece.color][c-1] = 1
                        dest = self.get_piece((r+piece.color, c-1))
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                check = self.turn
                                checkers.append(piece)
                    else:
                        self.whiteThreatMap[r+piece.color][c+1] = 1
                        self.whiteThreatMap[r+piece.color][c-1] = 1
                        dest1 = self.get_piece((r+piece.color, c+1))
                        if dest1 != 0:
                            if dest1.type == king and dest1.color == self.turn:
                                check = self.turn
                                checkers.append(piece)
                        dest2 = self.get_piece((r+piece.color, c-1))
                        if dest2 != 0:
                            if dest2.type == king and dest2.color == self.turn:
                                check = self.turn
                                checkers.append(piece)
                if piece.type == knight:
                    moves = [(r+2, c+1), (r+2, c-1),
                             (r-2, c+1), (r-2, c-1),
                             (r+1, c+2), (r-1, c+2),
                             (r+1, c-2), (r-1, c-2)]
                    for move in moves:
                        x, y = move
                        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
                            self.whiteThreatMap[x][y] = 1
                            dest = self.get_piece((x, y))
                            if dest != 0:
                                if dest.type == king and dest.color == self.turn:
                                    check = self.turn
                                    checkers.append(piece)
                if piece.type == bishop or piece.type == queen:
                    for direction in diagonal_squares:
                        pot_pin = None
                        king_found = False
                        for i in range(1, 8):
                            if piece.position + direction*i < 0 or piece.position + direction*i > 63:
                                break
                            pos = piece.position + direction*i
                            move = pos_getter[pos]
                            if (direction == -7 or direction == 9) and move[1] < c:
                                break
                            elif (direction == 7 or direction == -9) and move[1] > c:
                                break
                            dest = self.get_piece(move)
                            if dest != 0:
                                if king_found:
                                    break
                                if pot_pin:
                                    if dest.type == king and dest.color == self.turn:
                                        pot_pin.pinned = True
                                        break
                                    else:
                                        break
                                else:
                                    self.whiteThreatMap[move[0]][move[1]] = 1
                                    if dest.type == king and dest.color == self.turn:
                                        check = self.turn
                                        checkers.append(piece)
                                        king_found = True
                                    elif dest.color == self.turn:
                                        if pot_pin:
                                            break
                                        else:
                                            pot_pin = dest
                                    else:
                                        break
                            else:
                                if pot_pin is None:
                                    self.whiteThreatMap[move[0]][move[1]] = 1
                if piece.type == rook or piece.type == queen:
                    for direction in orthogonal_squares:
                        pot_pin = None
                        king_found = False
                        for i in range(1, 8):
                            if abs(direction) == 1:
                                if direction*i + piece.col < 0 or direction*i + piece.col > 7:
                                    break
                            if piece.position + direction*i < 0 or piece.position + direction*i > 63:
                                break
                            pos = piece.position + direction*i
                            move = pos_getter[pos]
                            dest = self.get_piece(move)
                            if dest != 0:
                                if king_found:
                                    break
                                if pot_pin:
                                    if dest.type == king and dest.color == self.turn:
                                        pot_pin.pinned = True
                                        break
                                    else:
                                        break
                                else:
                                    self.whiteThreatMap[move[0]][move[1]] = 1
                                    if dest.type == king and dest.color == self.turn:
                                        check = self.turn
                                        checkers.append(piece)
                                        king_found = True
                                    elif dest.color == self.turn:
                                        if pot_pin:
                                            break
                                        else:
                                            pot_pin = dest
                                    else:
                                        break
                            else:
                                if pot_pin is None:
                                    self.whiteThreatMap[move[0]][move[1]] = 1
                elif piece.type == king:
                    for direction in orthogonal_squares + diagonal_squares:
                        for i in range(1, 2):
                            if piece.position + direction*i < 0 or piece.position + direction*i > 63:
                                break
                            if abs(direction) == 1:
                                if direction*i + piece.col < 0 or direction*i + piece.col > 7:
                                    break
                            pos = piece.position + direction*i
                            move = pos_getter[pos]
                            dest = self.get_piece(move)
                            if (direction == -7 or direction == 9) and move[1] < piece.col:
                                break
                            elif (direction == 7 or direction == -9) and move[1] > piece.col:
                                break
                            if dest != 0:
                                self.whiteThreatMap[move[0]][move[1]] = 1
                                if dest.type == king and dest.color == self.turn:
                                    check = self.turn
                                    checkers.append(piece)
                                    break
                                else:
                                    break
                            else:
                                self.whiteThreatMap[move[0]][move[1]] = 1
        else:
            for piece in self.blackPieces:
                r, c = piece.row, piece.col
                if piece.type == pawn:
                    if c-1 < 0:
                        self.blackThreatMap[r+piece.color][c+1] = 1
                        dest = self.get_piece((r+piece.color, c+1))
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                check == self.turn
                                checkers.append(piece)
                    elif c+1 > 7:
                        self.blackThreatMap[r+piece.color][c-1] = 1
                        dest = self.get_piece((r+piece.color, c-1))
                        if dest != 0:
                            if dest.type == king and dest.color == self.turn:
                                check = self.turn
                                checkers.append(piece)
                    else:
                        self.blackThreatMap[r+piece.color][c+1] = 1
                        self.blackThreatMap[r+piece.color][c-1] = 1
                        dest1 = self.get_piece((r+piece.color, c+1))
                        if dest1 != 0:
                            if dest1.type == king and dest1.color == self.turn:
                                check = self.turn
                                checkers.append(piece)
                        dest2 = self.get_piece((r+piece.color, c-1))
                        if dest2 != 0:
                            if dest2.type == king and dest2.color == self.turn:
                                check = self.turn
                                checkers.append(piece)
                if piece.type == knight:
                    moves = [(r+2, c+1), (r+2, c-1),
                             (r-2, c+1), (r-2, c-1),
                             (r+1, c+2), (r-1, c+2),
                             (r+1, c-2), (r-1, c-2)]
                    for move in moves:
                        x, y = move
                        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
                            self.blackThreatMap[x][y] = 1
                            dest = self.get_piece((x, y))
                            if dest != 0:
                                if dest.type == king and dest.color == self.turn:
                                    check = self.turn
                                    checkers.append(piece)
                if piece.type == bishop or piece.type == queen:
                    for direction in diagonal_squares:
                        pot_pin = None
                        king_found = False
                        for i in range(1, 8):
                            if piece.position + direction*i < 0 or piece.position + direction*i > 63:
                                break
                            pos = piece.position + direction*i
                            move = pos_getter[pos]
                            if (direction == -7 or direction == 9) and move[1] < c:
                                break
                            elif (direction == 7 or direction == -9) and move[1] > c:
                                break
                            dest = self.get_piece(move)
                            if dest != 0:
                                if king_found:
                                    break
                                if pot_pin:
                                    if dest.type == king and dest.color == self.turn:
                                        pot_pin.pinned = True
                                        break
                                    else:
                                        break
                                else:
                                    self.blackThreatMap[move[0]][move[1]] = 1
                                    if dest.type == king and dest.color == self.turn:
                                        check = self.turn
                                        checkers.append(piece)
                                        king_found = True
                                    elif dest.color == self.turn:
                                        if pot_pin:
                                            break
                                        else:
                                            pot_pin = dest
                                    else:
                                        break
                            else:
                                if pot_pin is None:
                                    self.blackThreatMap[move[0]][move[1]] = 1
                if piece.type == rook or piece.type == queen:
                    for direction in orthogonal_squares:
                        pot_pin = None
                        king_found = False
                        for i in range(1, 8):
                            if abs(direction) == 1:
                                if direction*i + piece.col < 0 or direction*i + piece.col > 7:
                                    break
                            if piece.position + direction*i < 0 or piece.position + direction*i > 63:
                                break
                            pos = piece.position + direction*i
                            move = pos_getter[pos]
                            dest = self.get_piece(move)
                            if dest != 0:
                                if king_found:
                                    break
                                if pot_pin:
                                    if dest.type == king and dest.color == self.turn:
                                        pot_pin.pinned = True
                                        break
                                    else:
                                        break
                                else:
                                    self.blackThreatMap[move[0]][move[1]] = 1
                                    if dest.type == king and dest.color == self.turn:
                                        check = self.turn
                                        checkers.append(piece)
                                        king_found = False
                                    elif dest.color == self.turn:
                                        if pot_pin:
                                            break
                                        else:
                                            pot_pin = dest
                                    else:
                                        break
                            else:
                                if pot_pin is None:
                                    self.blackThreatMap[move[0]][move[1]] = 1
                if piece.type == king:
                    for direction in orthogonal_squares + diagonal_squares:
                        for i in range(1, 2):
                            if piece.position + direction*i < 0 or piece.position + direction*i > 63:
                                break
                            if abs(direction) == 1:
                                if direction*i + piece.col < 0 or direction*i + piece.col > 7:
                                    break
                            pos = piece.position + direction*i
                            move = pos_getter[pos]
                            dest = self.get_piece(move)
                            if (direction == -7 or direction == 9) and move[1] < piece.col:
                                break
                            elif (direction == 7 or direction == -9) and move[1] > piece.col:
                                break
                            if dest != 0:
                                self.blackThreatMap[move[0]][move[1]] = 1
                                if dest.type == king and dest.color == self.turn:
                                    check = self.turn
                                    checkers.append(piece)
                                    break
                                else:
                                    break
                            else:
                                self.blackThreatMap[move[0]][move[1]] = 1
        
        self.checkers = checkers
        self.check = check

    def draw(self):
        '''Method to draw board, call draw method of Board object'''
        self.board.draw_squares(self.win)
        if self.p_move != None:
            origin, dest = self.p_move
            oR, oC = origin
            destR, destC = dest

            if (oR + oC) % 2 == 0:
                pygame.draw.rect(
                    self.win, LIGHT_SQUARES_MOVE, (oC*SQUARE_SIZE, oR*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(
                    self.win, DARK_SQUARES_MOVE, (oC*SQUARE_SIZE, oR*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if (destR + destC) % 2 == 0:
                pygame.draw.rect(
                    self.win, LIGHT_SQUARES_MOVE, (destC*SQUARE_SIZE, destR*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(
                    self.win, DARK_SQUARES_MOVE, (destC*SQUARE_SIZE, destR*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = self.get_piece(dest)
            if piece != 0:
                piece.draw(self.win)

        if self.check != 0:
            kL = None
            if self.check == black_piece:
                kL = self.get_black_king_location()
            elif self.check == white_piece:
                kL = self.get_white_king_location()
            pygame.draw.circle(self.win, RED, (kL[1] * SQUARE_SIZE + 50, kL[0]  * SQUARE_SIZE + 50), 50, width=5)

    def draw_moves(self, pos):
        '''Method to draw moves, call draw_moves method of Board object'''
        if pos != None:
            piece = self.get_piece(pos)
            if piece != 0 and piece.pinned == False:
                if (pos[0] + pos[1]) % 2 == 0:
                    pygame.draw.rect(
                        self.win, LIGHT_SQUARES_MOVE, (pos[1]*SQUARE_SIZE, pos[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(
                        self.win, DARK_SQUARES_MOVE, (pos[1]*SQUARE_SIZE, pos[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece.draw(self.win)
                for move in self.move_list:
                    origin = move.get_origin()
                    dest = move.get_dest()
                    if pos == origin:
                        row, col = dest
                        if self.get_piece((row, col)) != 0:
                            pygame.draw.circle(
                                self.win, BLUE, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50), 50, width=5)
                        else:
                            pygame.draw.circle(
                                self.win, BLUE, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50), 15)

    def draw_promotion_screen(self, dest):
        '''Method that brings up the options when promoting a pawn and returns the piece that was selected to be promoted to'''
        pygame.draw.rect(self.win, GREY, (200, 325, 400, 150), False)
        x = 200
        y = 350
        if self.turn == black_piece:
            for image in W_IMGS[1:-1]:
                self.win.blit(image, (x, y))
                x += 100
        else:
            for image in B_IMGS[1:-1]:
                self.win.blit(image, (x, y))
                x += 100
        pygame.display.update()
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    x, y = mouse_pos
                    if y > 325 and y < 475:
                        selected_piece = (x-200)//100
                        choosing = False

        selected_piece += 2
        row, col = dest
        if selected_piece == 2:
            new_piece = Knight.Knight(-self.turn*selected_piece, row, col)
        elif selected_piece == 3:
            new_piece = Bishop.Bishop(-self.turn*selected_piece, row, col)
        elif selected_piece == 4:
            new_piece = Rook.Rook(-self.turn*selected_piece, row, col)
        elif selected_piece == 5:
            new_piece = Queen.Queen(-self.turn*selected_piece, row, col)

        return new_piece
    
    def draw_squares(self):
        self.board.draw_squares(self.win)
                
    def move(self, origin, dest, AI=True, generate=False, move=None):
        '''Method to move from origin to dest'''
        if move:
            origin = move.get_origin()
            dest = move.get_dest()
        else:
            for mv in self.move_list:
                if mv.get_origin() == origin and mv.get_dest() == dest:
                    move = mv
                    break 
        if move:
            o_piece = self.get_piece(origin)
            self.move_nmw(move) 
            if move.get_promotion():
                self.promote(move, o_piece, AI)
            self.updateThreatMap()
            if generate:
                if self.check != 0:
                    self.generate_all_moves()
                    self.find_winner()
            else:
                self.generate_all_moves()
                self.find_winner()
                self.reset_pins()
    
    def promote(self, move, o_piece, AI):
        """Method to make a promoting move. If AI is False, it is a human move so options will pop up to choose
        which piece to promote to. Otherwise, it will promote to the 'designated' piece according to the move."""
        color = -self.turn
        row, col = move.get_dest()
        if AI:
            code = move.get_promotion()
            if code == knight:
                new_piece = Knight.Knight(code*color, row, col)
            elif code == bishop:
                new_piece = Bishop.Bishop(code*color, row, col)
            elif code == rook:
                new_piece = Rook.Rook(code*color, row, col)
            elif code == queen:
                new_piece = Queen.Queen(code*color, row, col)
            if color == white_piece:
                index = self.whitePieces.index(o_piece)
                self.whitePieces[index] = new_piece
            else:
                index = self.blackPieces.index(o_piece)
                self.blackPieces[index] = new_piece
            self.board.board[row][col] = new_piece
        else:
            new_piece = self.draw_promotion_screen((row, col))
            if color == white_piece:
                index = self.whitePieces.index(o_piece)
                self.whitePieces[index] = new_piece
            else:
                index = self.blackPieces.index(o_piece)
                self.blackPieces[index] = new_piece
            self.board.board[row][col] = new_piece

    def move_nmw(self, move):
        origin = move.get_origin()
        dest = move.get_dest()
        x1, y1 = origin
        x2, y2 = dest

        o_piece = self.get_piece(origin)        # Piece to be moved

        # Piece/square where the o_piece will be moved
        d_piece = self.get_piece(dest)
        p_piece = self.get_p_piece()            # Piece moved last turn
        enPassantPiece = 0

        # Keep track if last move allows en passant capture
        enPassant = False
        if p_piece != None:
            if p_piece != 0:
                if p_piece.type == pawn:
                    if p_piece.en_passant == True:
                        enPassant = True

        # Check if it is an en passant move
        if move.get_enpassant():
            en_piece = self.get_piece((x1, y2))
            enPassantPiece = en_piece
            if en_piece.color == white_piece:
                self.whitePieces.remove(en_piece)
            else:
                self.blackPieces.remove(en_piece)

        # Check for promotion
        if move.get_promotion():
            promotion = True  
        else:
            promotion = False

        newNode = Node((origin, dest), self.p_move, self.move_list,
                       enPassantPiece, enPassant, self.check, d_piece, p_piece, self.blackQueenSideCastle, self.blackKingSideCastle, self.whiteQueenSideCastle, self.whiteKingSideCastle,
                       self.whiteThreatMap, self.blackThreatMap, promotion, self.winner)

        if o_piece.type == king:
            if o_piece.color == white_piece:
                self.whiteKingSideCastle = False
                self.whiteQueenSideCastle = False
            else:
                self.blackKingSideCastle = False
                self.blackQueenSideCastle = False

        if o_piece.type == rook:
            if x1 == 7:
                if y1 == 7:
                    self.whiteKingSideCastle = False
                elif y1 == 0:
                    self.whiteQueenSideCastle = False
            elif x1 == 0:
                if y1 == 7:
                    self.blackKingSideCastle = False
                elif y1 == 0:
                    self.blackQueenSideCastle = False

        # Remove captured pieces from piece list
        if d_piece != 0:
            if d_piece.color == white_piece:
                self.whitePieces.remove(d_piece)
            else:
                self.blackPieces.remove(d_piece)

        self.history.append(newNode)
        self.board.move(origin, dest)
        self.p_move = (origin, dest)
        self.num_of_moves += 1

        self.change_turn()

    def unmove(self):
        '''Method to undo a move'''
        if self.num_of_moves > 0:
            node = self.history.pop()
            self.turn = -self.turn
            origin, dest = node.getMove()
            cap_piece = node.getCapPiece()
            enPassant = node.getEnPassant()
            enPassantPiece = node.getEnPassantPiece()
            p_piece = node.getP_piece()

            promotion = node.getPromotion()

            self.blackKingSideCastle = node.getBlackKingSideCastle()
            self.blackQueenSideCastle = node.getBlackQueenSideCastle()
            self.whiteKingSideCastle = node.getWhiteKingSideCastle()
            self.whiteQueenSideCastle = node.getWhiteQueenSideCastle()

            self.whiteThreatMap = node.getWhiteThreatMap()
            self.blackThreatMap = node.getBlackThreatMap()
            
            self.check = node.getCheck()
            self.winner = node.getWinner()
            
            self.p_move = node.getP_move()
            self.move_list = node.getMoveList()
            if self.move_list == 0:
                self.move_list = []
            self.num_of_moves -= 1
            self.board.unmove(origin, dest, cap_piece,
                              enPassantPiece, enPassant, p_piece)

            # Add captured piece back to List
            if cap_piece != 0:
                if cap_piece.color == white_piece:
                    self.whitePieces.append(cap_piece)
                else:
                    self.blackPieces.append(cap_piece)

            # If en passant capture was made
            if enPassantPiece != 0:
                if enPassantPiece.color == white_piece:
                    self.whitePieces.append(enPassantPiece)
                else:
                    self.blackPieces.append(enPassantPiece)

            if promotion:
                promoted_p = self.get_piece(origin)
                reverse = Pawn.Pawn(self.turn, origin[0], origin[1])
                if self.turn == white_piece:
                    index = self.whitePieces.index(promoted_p)
                    self.whitePieces[index] = reverse
                else:
                    index = self.blackPieces.index(promoted_p)
                    self.blackPieces[index] = reverse
                self.board.board[origin[0]][origin[1]] = reverse

            self.reset_pins()

    def change_turn(self):
        '''Method to change turn'''
        self.turn = -self.turn

    def find_danger(self, color):
        '''This functions looks at the 4 diagonals and 4 orthogonals
        from the king of color 'color' piece and looks for potential danger (checks, pinned pieces)'''

        board = self.board

        # Intermediate  variables
        potential_pin = None
        check = 0

        # Get location of king of color 'color'
        if color == white_piece:
            if self.board.whiteKingLocation != None:
                x, y = self.board.whiteKingLocation
            else:
                return check * color
        else:
            if self.board.blackKingLocation != None:
                x, y = self.board.blackKingLocation
            else:
                return check * color

        # Board positions
        current_king_pos = x*8 + y

        orthogonal_squares = [-8, 1, 8, -1]
        diagonal_squares = [-9, -7, 9, 7]

        checkers = []

        # Find edge of board from king position in 8 directions
        for direction in orthogonal_squares:
            potential_pin = None
            for i in range(1, 8):
                if abs(direction) == 1:
                    if direction*i + y < 0 or direction*i + y > 7:
                        break
                if current_king_pos + direction*i < 0 or current_king_pos + direction*i > 63:
                    break
                pos = current_king_pos + direction*i
                move = pos_getter[pos]
                piece = board.get_piece(move)
                if piece != 0:
                    if i == 1 and piece.type == king:
                        check = 1
                        checkers.append(piece)
                    elif (piece.type == queen or piece.type == rook) and piece.color != color:
                        if potential_pin == None:
                            check = 1
                            checkers.append(piece)
                        else:
                            potential_pin.pinned = True
                            potential_pin = None
                        break
                    else:
                        if potential_pin == None:
                            potential_pin = piece
                        else:
                            potential_pin = None
                            break

        for direction in diagonal_squares:
            potential_pin = None
            for i in range(1, 8):
                if current_king_pos + direction*i < 0 or current_king_pos + direction*i > 63:
                    break
                pos = current_king_pos + direction*i
                move = pos_getter[pos]
                if (direction == -7 or direction == 9) and move[1] < y:
                    break
                elif (direction == 7 or direction == -9) and move[1] > y:
                    break
                piece = board.get_piece(move)
                if piece != 0:
                    if i == 1 and piece.type == king:
                        check = 1
                        checkers.append(piece)
                    elif (piece.type == queen or piece.type == bishop) and piece.color != color:
                        if potential_pin == None:
                            check = 1
                            checkers.append(piece)
                        else:
                            potential_pin.pinned = True
                            potential_pin = None
                        break
                    else:
                        if potential_pin == None:
                            potential_pin = piece
                        else:
                            potential_pin = None
                            break

        # Check danger from knights
        pot_moves = [(x+2, y+1), (x+2, y-1),
                     (x-2, y+1), (x-2, y-1),
                     (x+1, y+2), (x-1, y+2),
                     (x+1, y-2), (x-1, y-2)]

        for move in pot_moves:
            try:
                piece = self.get_piece(move)
                if (piece.type == knight) and (piece.color != color) and move[0] in range(0, ROWS) and move[1] in range(0, COLS):
                    check = 1
                    checkers.append(piece)
            except:
                continue

        # Check danger from pawns
        try:
            piece = self.get_piece((x + color, y + 1))
            if piece.type == pawn and piece.color != color:
                check = 1
                checkers.append(piece)
        except:
            pass
        try:
            if y-1 > 0:
                piece = self.get_piece((x + color, y - 1))
                if piece.type == pawn and piece.color != color:
                    check = 1
                    checkers.append(piece)
        except:
            pass

        self.checkers = checkers
        return check * color

    def generate_all_moves(self):
        self.move_list = MoveGenerator(self)

    def find_winner(self):
        '''Find if the match has ended'''
        if self.move_list == [] and self.check == self.turn:
            self.winner = -self.turn
        elif self.move_list == []:
            self.winner = 0

    def get_piece(self, pos):
        '''Get piece on position pos'''
        if pos[0] < 0 or pos[1] < 0 or pos[0] > 7 or pos[1] > 7:
            return 0
        return self.board.get_piece(pos)

    def get_piece_from_pos(self, pos):
        if -1 < pos < 64:
            col = pos % 8
            row = pos // 8
            return self.get_piece((row, col))
        else:
            return None

    def get_pieces(self, color):
        '''Get all pieces of color color'''
        return self.board.get_pieces(color)

    def reset_pins(self):
        '''Reset piece pinned attribute'''
        self.board.reset_pins(self.whitePieces+self.blackPieces)

    def get_p_piece(self):
        '''Get previous piece'''
        return self.board.p_piece

    def get_white_king_location(self):
        return self.board.whiteKingLocation

    def get_black_king_location(self):
        return self.board.blackKingLocation

    def __repr__(self):
        '''Method to print the game (board, king locations, and if there is a check'''
        result = ""
        result += repr(self.board) + "\n"
        result += "White King location: "
        if self.board.whiteKingLocation == None:
            result += "Not available\n"
        else:
            result += str(self.board.whiteKingLocation) + "\n"
        result += "Black King location: "
        if self.board.blackKingLocation == None:
            result += "Not available\n"
        else:
            result += str(self.board.blackKingLocation) + "\n"

        if self.check == white_piece:
            result += "White in check\n"
        elif self.check == black_piece:
            result += "Black in check\n"
        else:
            result += "No check\n"

        if self.turn == white_piece:
            result += "White to play"
        else:
            result += "Black to play"
        return result

    def to_str(self):
        '''Method to print the game (board, king locations, and if there is a check'''
        result = ""
        result += repr(self.board)
        result += "White King location: "
        if self.board.whiteKingLocation == None:
            result += "Not available\n"
        else:
            result += str(self.board.whiteKingLocation) + "\n"
        result += "Black King location: "
        if self.board.blackKingLocation == None:
            result += "Not available\n"
        else:
            result += str(self.board.blackKingLocation) + "\n"

        if self.check == white_piece:
            result += "White in check\n"
        elif self.check == black_piece:
            result += "Black in check\n"
        else:
            result += "No check\n"

        if self.turn == white_piece:
            result += "White to play"
        else:
            result += "Black to play"
        return result +"\n"
 
