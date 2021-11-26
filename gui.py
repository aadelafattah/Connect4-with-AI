import pygame
import sys
from algorithm import decide, add_to_board, is_full, get_score_with_remove, print_tree

NUMBER_OF_MAKES = 4
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_ONE_PIECE = 1
PLAYER_TWO_PIECE = 2
PLAYER_ONE_REPLACEMENT = 3
PLAYER_TWO_REPLACEMENT = 4

DEPTH = 0
PLAYER_POINTS = 0
AI_POINTS = 0

PIXEL_UNIT = 100
BLUE = (50, 100, 230)
DARK_BLUE = (40, 80, 160)
GREY = (122, 123, 142)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
BRIGHT_RED = (225, 100, 100)
GREEN = (0, 225, 0)
BRIGHT_GREEN = (100, 225, 100)
LEN_PIC_PIX = 95

current_tree = None
recorded_score = 0
row_difference = (PIXEL_UNIT * ROW_COUNT - LEN_PIC_PIX *
                  ROW_COUNT) / (2 * ROW_COUNT)
column_difference = (PIXEL_UNIT * COLUMN_COUNT -
                     LEN_PIC_PIX * COLUMN_COUNT) / (2 * COLUMN_COUNT)

points = {  # Number of pieces of same player in a sequence --> its score
    0: 0,
    1: 0,
    2: 2,
    3: 5,
    4: 10000
}

board = [[0 for column in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]

# initiate pygame
pygame.init()

# initializing the window
window = pygame.display.set_mode(
    (COLUMN_COUNT * PIXEL_UNIT, ROW_COUNT * PIXEL_UNIT))

# Title and Icon
pygame.display.set_caption("Make Connect 4")
pygame.display.set_icon(pygame.image.load('assets/connect.png'))

# Balls
red_ball = pygame.image.load('assets/red.png')
yellow_ball = pygame.image.load('assets/yellow.png')


def draw_board(grid):
    # putting the images
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            coordinates = (column_difference + PIXEL_UNIT *
                           c, row_difference + PIXEL_UNIT * r)
            if (grid[r][c] == PLAYER_ONE_PIECE) or (grid[r][c] == PLAYER_ONE_REPLACEMENT):
                window.blit(red_ball, coordinates)
            elif (grid[r][c] == PLAYER_TWO_PIECE) or (grid[r][c] == PLAYER_TWO_REPLACEMENT):
                window.blit(yellow_ball, coordinates)
            else:
                pass
    # drawing the lines
    for i in range(COLUMN_COUNT + 1):
        pygame.draw.line(window, GREY, (PIXEL_UNIT * i, 0), (PIXEL_UNIT * i, PIXEL_UNIT * ROW_COUNT),
                         int(column_difference))

    for i in range(ROW_COUNT + 1):
        pygame.draw.line(window, GREY, (0, PIXEL_UNIT * i), (PIXEL_UNIT * COLUMN_COUNT, PIXEL_UNIT * i),
                         int(row_difference))


# player move
def player_move(column):
    # global recorded_score
    global PLAYER_POINTS
    if add_to_board(board, PLAYER_ONE_PIECE, ROW_COUNT, column):
        move_points = get_score_with_remove(board, PLAYER_ONE_PIECE, PLAYER_ONE_REPLACEMENT, ROW_COUNT, COLUMN_COUNT,
                                            NUMBER_OF_MAKES)
        if move_points > 0:
            PLAYER_POINTS += move_points
            return True
    return False


# Algorithm Move 1
def algorithm_move(with_pruning):
    global board
    global AI_POINTS
    global current_tree
    pieces = {
        "player1": PLAYER_ONE_PIECE,
        "player2": PLAYER_TWO_PIECE,
        "replacement1": PLAYER_ONE_REPLACEMENT,
        "replacement2": PLAYER_TWO_REPLACEMENT
    }
    # (new_board, algorithm_score) = min_max(board, with_pruning, DEPTH, True, float('-inf'), float('inf'), ROW_COUNT,
    #                                        COLUMN_COUNT, NUMBER_OF_MAKES, pieces)
    (new_board, algorithm_score, tree) = decide(board, with_pruning,
                                                DEPTH, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, pieces)
    current_tree = tree
    board = new_board
    move_points = get_score_with_remove(board, PLAYER_TWO_PIECE, PLAYER_TWO_REPLACEMENT, ROW_COUNT, COLUMN_COUNT,
                                        NUMBER_OF_MAKES)
    print_tree(tree, DEPTH)
    if move_points > 0:
        AI_POINTS += move_points
        return True
    return False


# Game Loop
pruning = True


def button(click, mouse, surface, x, y, width, height, color, bright_color):
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, bright_color, (x, y, width, height))
        if click[0]:
            return True
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))
        return False


def text_show(message, size, x, y):
    text = pygame.font.Font('freesansbold.ttf', size)
    TextSurf = text.render(message, True, BLACK)
    TextRect = TextSurf.get_rect()
    TextRect.center = (x, y)
    window.blit(TextSurf, TextRect)


def game_intro():
    global DEPTH
    intro = True
    temp = ''

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == '0':
                    temp = temp + '0'
                if event.unicode == '1':
                    temp = temp + '1'
                if event.unicode == '2':
                    temp = temp + '2'
                if event.unicode == '3':
                    temp = temp + '3'
                if event.unicode == '4':
                    temp = temp + '4'
                if event.unicode == '5':
                    temp = temp + '5'
                if event.unicode == '6':
                    temp = temp + '6'
                if event.unicode == '7':
                    temp = temp + '7'
                if event.unicode == '8':
                    temp = temp + '8'
                if event.unicode == '9':
                    temp = temp + '9'
                elif event.unicode == "d" or event.unicode == "D":
                    temp = temp[0:-1]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill(WHITE)
        if len(temp) == 0:
            DEPTH = 0
        else:
            DEPTH = int(temp)

        text_show(f"K = {DEPTH}", 25, window.get_width() /
                  2, window.get_height() / 4)
        text_show("Connect 4", 100, window.get_width() /
                  2, window.get_height() / 2)
        text_show(f"Use 'D' to delete ", 15, window.get_width() /
                  2, window.get_height() - 30)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if DEPTH != 0:
            if button(click, mouse, window, window.get_width() / 4 - 60, window.get_height() / 4 * 3 + 20, 220, 60, GREEN,
                      BRIGHT_GREEN):
                return True
            if button(click, mouse, window, window.get_width() / 3 * 2 - 60, window.get_height() / 4 * 3 + 20, 220, 60, RED,
                      BRIGHT_RED):
                return False

        text_show("with Alpha & Beta", 20, (window.get_width() / 4) + (100 / 2),
                  window.get_height() / 4 * 3 + (100 / 2))
        text_show("without Alpha & Beta", 20, (window.get_width() / 3 * 2) + (100 / 2),
                  window.get_height() / 4 * 3 + (100 / 2))

        pygame.display.update()


def game_loop(method):
    running = True
    # background colour
    window.fill(BLUE)
    player_turn = True
    while running:
        # Algorithm Move
        if not player_turn:
            player_turn = True
            if algorithm_move(method):
                print(f"score : player / AI = ({PLAYER_POINTS},{AI_POINTS})")

        # handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # print the tree
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    if not (current_tree is None):
                        if print_tree(current_tree):
                            print("TREE VIEWING EXPERIENCE IS DONE!!")
            # player move
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                column = x // 100
                if player_turn and board[0][column] == 0:
                    player_turn = False
                    if player_move(column):
                        print(
                            f"score : player / AI = ({PLAYER_POINTS},{AI_POINTS})")

        # draw the board
        draw_board(board)

        # update window
        pygame.display.update()

        if is_full(board):
            return


def game_end():
    end = True
    pygame.draw.rect(window, WHITE,
                     (window.get_width() / 5, window.get_height() / 5, window.get_width() / 5 * 3,
                      window.get_height() / 5 * 3))
    text_show(f"AI:{AI_POINTS}, Player:{PLAYER_POINTS}", 50,
              window.get_width() / 2, window.get_height() / 3)
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if button(click, mouse, window, window.get_width() / 7 * 2, window.get_height() / 6 * 3, 100, 100, GREEN,
                  BRIGHT_GREEN):
            return False
        if button(click, mouse, window, window.get_width() / 7 * 4, window.get_height() / 6 * 3, 100, 100, RED,
                  BRIGHT_RED):
            return True
        text_show("Again", 25, window.get_width() / 7 * 2 +
                  (100 / 2), window.get_height() / 6 * 3 + (100 / 2))
        text_show("Quit", 25, window.get_width() / 7 * 4 +
                  (100 / 2), window.get_height() / 6 * 3 + (100 / 2))
        pygame.display.flip()
        pygame.display.update()


def game_reset():
    global board, AI_POINTS, PLAYER_POINTS
    board = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
    AI_POINTS = 0
    PLAYER_POINTS = 0


if __name__ == '__main__':
    while True:
        pruning = game_intro()
        game_loop(pruning)
        if game_end():
            pygame.quit()
            sys.exit()
        else:
            game_reset()
