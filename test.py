from algorithm import print_board, add_to_board, get_score, decide

NUMBER_OF_MAKES = 4
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_ONE_PIECE = 1
PLAYER_TWO_PIECE = 2
SCORE_FOR_WIN = 1000
DEPTH = 6
points = {  # Number of pieces of same player in a sequence --> its score
    0: 0,
    1: 0,
    2: 2,
    3: 5,
    4: 1000
}


board = [[0 for column in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]


pruning = True
quit_loop = False
player_one_move = True

# while quit_loop:
#     global pruning
#     p = False
#     x = input("would you like pruning (Y) or no (N): ").upper()
#     if x.__eq__('Y'):
#         p = True
#         quit_loop = True
#     elif x.__eq__('N'):
#         p = False
#         quit_loop = True
#     else:
#         print("WRONG ANSWER!")
#
#     pruning = p
#


x = input("would you like pruning (Y) or no (N): ").upper()
if x.__eq__('Y'):
    pruning = True
elif x.__eq__('N'):
    pruning = False

quit_loop = False

while not quit_loop:
    # Print Game grid
    print_board(board)

    global recorded_score

    # Player One Move
    if player_one_move:
        player_one_move = False
        try:
            choice = int(input("Enter column number: ")) - 1
            if add_to_board(board, 1, ROW_COUNT, choice):
                score = get_score(board, 1, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, points) - get_score(board, 2,
                                                                                                          ROW_COUNT,
                                                                                                          COLUMN_COUNT,
                                                                                                          NUMBER_OF_MAKES,
                                                                                                          points)
                recorded_score = score
                print(f"Player score: {recorded_score}")
                if recorded_score >= SCORE_FOR_WIN:
                    print(f"Congrats Player, Your Score = {recorded_score}")
                    quit_loop = True
        except ValueError:
            print("Wrong move!!")
            continue

    # Player Two (algorithm) Move
    else:
        player_one_move = True
        (board, algorithm_score) = decide(board, pruning, DEPTH, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, points)
        # (board, algorithm_score) = min_max(board,pruning, DEPTH, float('-inf'), float('inf'), True, ROW_COUNT,
        # COLUMN_COUNT, NUMBER_OF_MAKES, points)
        print(f"Algorithm score: {algorithm_score}")
        if algorithm_score < SCORE_FOR_WIN:
            continue
        print(f"You lost, Your Score = {recorded_score}")
        quit_loop = True

print_board(board)
