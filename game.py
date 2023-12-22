import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE

WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
PLAYER_COLOR = (0, 0, 255)
AI_COLOR = (255, 0, 0)

board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")

def draw_board():
    screen.fill(WHITE)
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

def draw_player(row, col):
    pygame.draw.line(screen, PLAYER_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                     ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, PLAYER_COLOR, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE),
                     (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)

def draw_ai(row, col):
    pygame.draw.circle(screen, AI_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                       SQUARE_SIZE // 2 - 5, LINE_WIDTH)

def check_win(player):
    for i in range(BOARD_SIZE):
        if all(board[i][j] == player for j in range(BOARD_SIZE)) or all(board[j][i] == player for j in range(BOARD_SIZE)):
            return True
    if all(board[i][i] == player for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
        return True
    return False

def check_draw():
    return all(board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

def get_available_moves():
    return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == ' ']

def minimax(depth, is_maximizing):
    if check_win('O'):
        return 10 - depth
    elif check_win('X'):
        return depth - 10
    elif check_draw():
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for move in get_available_moves():
            board[move[0]][move[1]] = 'O'
            eval = minimax(depth + 1, False)
            board[move[0]][move[1]] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves():
            board[move[0]][move[1]] = 'X'
            eval = minimax(depth + 1, True)
            board[move[0]][move[1]] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move():
    best_eval = float('-inf')
    best_move = None
    for move in get_available_moves():
        board[move[0]][move[1]] = 'O'
        eval = minimax(0, False)
        board[move[0]][move[1]] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                row = event.pos[1] // SQUARE_SIZE
                col = event.pos[0] // SQUARE_SIZE
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    if check_win('X'):
                        print("Вы победили!")
                        pygame.quit()
                        sys.exit()
                    if check_draw():
                        print("Ничья!")
                        pygame.quit()
                        sys.exit()

                    ai_move = get_best_move()
                    board[ai_move[0]][ai_move[1]] = 'O'
                    if check_win('O'):
                        print("Вы проиграли!")
                        pygame.quit()
                        sys.exit()
                    if check_draw():
                        print("Ничья!")
                        pygame.quit()
                        sys.exit()

    draw_board()

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                draw_player(row, col)
            elif board[row][col] == 'O':
                draw_ai(row, col)

    pygame.display.flip()
