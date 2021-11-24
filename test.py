from algorithm import get_score_with_remove, print_board

points = {  # Number of pieces of same player in a sequence --> its score
    0: 0,
    1: 0,
    2: 2,
    3: 5,
    4: 1000
}

board = [
    [1, 1, 1, 1, 0, 0, 0],
    [5, 0, 0, 0, 0, 1, 0],
    [2, 5, 0, 0, 1, 0, 6],
    [2, 0, 5, 1, 0, 6, 0],
    [2, 0, 0, 5, 6, 0, 0],
    [2, 0, 0, 6, 0, 0, 0]
]

board_1 = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0],
    [0, 0, 3, 1, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0],
]

board_2 = [
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 0, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 0, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 0, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 0, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
]

print(f"First Move, Player 1: winning = {get_score_with_remove(board_1, 1, 3, len(board_1), len(board_1[0]), 4)}")
print_board(board_1)
#
# print(f"Second Move, Player 2: winning = {get_score_with_remove(board, 2, 4, len(board), len(board[0]), 4)}")
# print_board(board)
#
# print(f"Third Move, Player 3: winning = {get_score_with_remove(board, 5, 7, len(board), len(board[0]), 4)}")
# print_board(board)
#
# print(f"Forth Move, Player 4: winning = {get_score_with_remove(board, 6, 8, len(board), len(board[0]), 4)}")
# print_board(board)
