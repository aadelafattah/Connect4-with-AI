import sys
import pygame
from pygame.locals import *
import math

Turn = True

RED = (190, 50, 55)
YELLOW = (245, 210, 80)
BLUE = (50, 90, 220)
DARK_BLUE = (40, 80, 160)
GREY = (211, 211, 211)

UNIT = 100
ROW_COUNT = 6
COLUMN_COUNT = 7
size = (UNIT * COLUMN_COUNT, UNIT * ROW_COUNT)
board = [[0 for r in range(ROW_COUNT)] for c in range(COLUMN_COUNT)]

pygame.init()
window = pygame.display.set_mode(size)
pygame.display.set_caption('Connect 4')
running = True


def draw_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(window, BLUE, (c * UNIT, r * UNIT, UNIT, UNIT))
            pygame.draw.rect(window, DARK_BLUE, (c * UNIT, r * UNIT, UNIT, UNIT), 10, 100)
            if board[c][r] == 1:
                pygame.draw.circle(window, RED, (c * UNIT + UNIT / 2, r * UNIT + UNIT / 2), UNIT * 0.42)
            elif board[c][r] == -1:
                pygame.draw.circle(window, YELLOW, (c * UNIT + UNIT / 2, r * UNIT + UNIT / 2), UNIT * 0.42)
            else:
                pygame.draw.circle(window, GREY, (c * UNIT + UNIT / 2, r * UNIT + UNIT / 2), UNIT * 0.42)


def find_place():
    column = math.floor(pygame.mouse.get_pos()[0] / 100)
    row = math.floor(pygame.mouse.get_pos()[1] / 100)
    while board[column][row] != 0 and row >= 0:
        row = row - 1
    return column, row


while running:
    draw_board()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            place = find_place()
            if place[1] >= 0:
                if Turn:
                    board[place[0]][place[1]] = 1
                else:
                    board[place[0]][place[1]] = -1
                Turn = not Turn
        if event.type == QUIT:
            running = not running
            sys.exit()
    pygame.display.update()
