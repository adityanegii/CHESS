import pygame

# BOARD DIMESIONS
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# COLORS
LIGHT_SQUARES = (199, 167, 137)
DARK_SQUARES = (148, 113, 81)
DARK_SQUARES_MOVE = (200, 200, 36)
LIGHT_SQUARES_MOVE = (255, 225, 0)
BLUE = (0, 0, 175)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# DEPTH for move search
DEPTH = 4
INF = float('inf')

# Piece numbers
pawn = 1
knight = 2
bishop = 3
rook = 4
queen = 5
king = 6

promotion_list = [knight, bishop, rook, queen]

# Piece color
white_piece = -1
black_piece = 1

# Dictionary of association for FEN
symbol2num = {'p': 1, 'n': 2, 'b': 3, 'r': 4, 'q': 5, 'k': 6}

# White pieces
W_PAWN = pygame.transform.scale(pygame.image.load(
    'misc/assets/w_pawn.png'), (100, 100))
W_ROOK = pygame.transform.scale(pygame.image.load(
    'misc/assets/w_rook.png'), (100, 100))
W_QUEEN = pygame.transform.scale(pygame.image.load(
    'misc/assets/w_queen.png'), (100, 100))
W_KING = pygame.transform.scale(pygame.image.load(
    'misc/assets/w_king.png'), (100, 100))
W_BISHOP = pygame.transform.scale(pygame.image.load(
    'misc/assets/w_bishop.png'), (100, 100))
W_KNIGHT = pygame.transform.scale(pygame.image.load(
    'misc/assets/w_knight.png'), (100, 100))

W_IMGS = [W_PAWN, W_KNIGHT, W_BISHOP, W_ROOK, W_QUEEN, W_KING]

# Black pieces
B_PAWN = pygame.transform.scale(pygame.image.load(
    'misc/assets/b_pawn.png'), (100, 100))
B_ROOK = pygame.transform.scale(pygame.image.load(
    'misc/assets/b_rook.png'), (100, 100))
B_QUEEN = pygame.transform.scale(pygame.image.load(
    'misc/assets/b_queen.png'), (100, 100))
B_KING = pygame.transform.scale(pygame.image.load(
    'misc/assets/b_king.png'), (100, 100))
B_BISHOP = pygame.transform.scale(pygame.image.load(
    'misc/assets/b_bishop.png'), (100, 100))
B_KNIGHT = pygame.transform.scale(pygame.image.load(
    'misc/assets/b_knight.png'), (100, 100))

B_IMGS = [B_PAWN, B_KNIGHT, B_BISHOP, B_ROOK, B_QUEEN, B_KING]

orthogonal_squares = [-8, 1, 8, -1]
diagonal_squares = [-9, -7, 9, 7]
k_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

pos_getter = []
for row in range(ROWS):
    for col in range(COLS):
        pos_getter.append((row, col))

colToLetter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
