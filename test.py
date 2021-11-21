from algorithm import print_board, add_to_board, get_score, min_max

NUMBER_OF_MAKES = 4
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_ONE_PIECE = 1
PLAYER_TWO_PIECE = 2
SCORE_FOR_WIN = 1000
DEPTH = 5
points = {  # Number of pieces of same player in a sequence --> its score
    0: 0,
    1: 1,
    2: 2,
    3: 5,
    4: 1000
}

board = [[0 for column in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]

# command line testing

# end_loop = False
# player_one_move = True
# while not end_loop:
#     print_board(board)
#     if player_one_move:
#         try:
#             column_1 = int(input("Player one> "))
#             if add_to_board(board, PLAYER_ONE_PIECE,ROW_COUNT, column_1):
#                 score = get_score(board, 1, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, points)
#                 if score >= SCORE_FOR_WIN:
#                     print("congrats!! one")
#                     end_loop = True
#             else:
#                 print("Wrong move!!")
#                 continue
#             player_one_move = False
#         except ValueError:
#             print("Wrong Input!!")
#             continue
#     else:
#         try:
#             column_2 = int(input("Player two> "))
#             if add_to_board(board, PLAYER_TWO_PIECE,ROW_COUNT, column_2):
#                 score = get_score(board,2,ROW_COUNT,COLUMN_COUNT,NUMBER_OF_MAKES,points)
#                 if score >= SCORE_FOR_WIN:
#                     print("congrats!! two")
#                     end_loop = True
#             else:
#                 print("Wrong move!!")
#                 continue
#             player_one_move = True
#         except ValueError:
#             print("Wrong Input!!")
#             continue
#
# print_board(board)


quit_loop = False
player_one_move = True

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
                score = get_score(board, 1, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, points)
                recorded_score = score
                if score >= SCORE_FOR_WIN:
                    print(f"Congrats Player, Your Score = {score}")
                    quit_loop = True
        except ValueError:
            print("Wrong move!!")
            continue

    # Player Two (algorithm) Move
    else:
        player_one_move = True
        # (board, algorithm_score) = decide(board, DEPTH, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, points)
        (board, algorithm_score) = min_max(board, DEPTH, float('-inf'), float('inf'), True, ROW_COUNT, COLUMN_COUNT,
                                           NUMBER_OF_MAKES, points)
        if algorithm_score < SCORE_FOR_WIN:
            continue
        print(f"You lost, Your Score = {recorded_score}")
        quit_loop = True

print_board(board)
