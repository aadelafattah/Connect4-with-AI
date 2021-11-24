import pygame
from algorithm import decide, get_score, add_to_board, print_board, is_full

NUMBER_OF_MAKES = 4
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_ONE_PIECE = 1
PLAYER_TWO_PIECE = 2
SCORE_FOR_WIN = 950
DEPTH = 6
PLAYER_SCORE=0
AI_SCORE=0

PIXEL_UNIT = 100
BLUE = (50, 100, 230)
DARK_BLUE = (40, 80, 160)
GREY = (122, 123, 142)
LEN_PIC_PIX = 95

recorded_score = 0
row_difference = (PIXEL_UNIT * ROW_COUNT - LEN_PIC_PIX * ROW_COUNT) / (2 * ROW_COUNT)
column_difference = (PIXEL_UNIT * COLUMN_COUNT - LEN_PIC_PIX * COLUMN_COUNT) / (2 * COLUMN_COUNT)

points = {  # Number of pieces of same player in a sequence --> its score
    0: 0,
    1: 0,
    2: 2,
    3: 5,
    4: 1000
}

board = [[0 for column in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]

# initiate pygame
pygame.init()

# initializing the window
window = pygame.display.set_mode((COLUMN_COUNT * PIXEL_UNIT, ROW_COUNT * PIXEL_UNIT))

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
            coordinates = (column_difference + PIXEL_UNIT * c, row_difference + PIXEL_UNIT * r)
            if grid[r][c] == PLAYER_ONE_PIECE:
                window.blit(red_ball, coordinates)
            elif grid[r][c] == PLAYER_TWO_PIECE:
                window.blit(yellow_ball, coordinates)
            else:
                pass
    # drawing the lines
    for i in range(COLUMN_COUNT+1):
        pygame.draw.line(window, GREY, (PIXEL_UNIT * i, 0), (PIXEL_UNIT * i, PIXEL_UNIT * ROW_COUNT),
                         int(column_difference))

    for i in range(ROW_COUNT+1):
        pygame.draw.line(window, GREY, (0, PIXEL_UNIT * i), (PIXEL_UNIT * COLUMN_COUNT,PIXEL_UNIT * i),
                         int(row_difference))


# player move
def player_move(column):
    global recorded_score
    if add_to_board(board, PLAYER_ONE_PIECE, ROW_COUNT, column):
        score = get_score(board, 1, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, points) - get_score(board, 2,
                                                                                                  ROW_COUNT,
                                                                                                  COLUMN_COUNT,
                                                                                                  NUMBER_OF_MAKES,
                                                                                                  points)
        recorded_score = score
        print(f"Player score: {recorded_score}")
        if recorded_score >= SCORE_FOR_WIN:
            print(f"Congrats Player, Your Score = {recorded_score}")
            return True
        return False


# Algorithm Move 1
def algorithm_move(pruning):
    global board
    (new_board, algorithm_score) = decide(board, pruning, DEPTH, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, points, )
    board = new_board
    print(f"AI score: {algorithm_score}")
    if algorithm_score >= SCORE_FOR_WIN:
        print(f"You lost, Your Score = {recorded_score}")
        return True
    return False


# Game Loop
running = True
player_turn = True
pruning = True
while running:
    # background colour
    window.fill(BLUE)

    # Algorithm Move
    if not player_turn:
        player_turn = True
        if algorithm_move(pruning):
            AI_SCORE = AI_SCORE + 1
            pass

    # handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # player move
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            column = x // 100
            if player_turn:
                player_turn = False
                if player_move(column):
                    PLAYER_SCORE = PLAYER_SCORE + 1
                    pass
    # draw the board
    draw_board(board)

    # update window
    pygame.display.update()

    if is_full(board):
        running= False
        print(AI_SCORE, PLAYER_SCORE)

print_board(board)
