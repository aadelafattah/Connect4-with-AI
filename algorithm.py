import sys

NUMBER_OF_MAKES = 4
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_ONE_PIECE = 1
PLAYER_TWO_PIECE = 2
points = {  # Number of pieces of same player in a sequence --> its score
    0: 0,
    1: 1,
    2: 2,
    3: 5,
    4: 500
}

board = [[0 for column in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]


def print_board(board):
    for row in board:
        for item in row:
            print(f"{item} ", end="")
        print("")


def is_full(board):
    for row in board:
        for item in row:
            if item == 0:
                return False
    return True


def get_copy(board):
    new_board = []
    for row in board:
        new_row = []
        for item in row:
            new_row.append(item)
        new_board.append(new_row)
    return new_board


def add_to_board(board, player_piece, column):
    try:
        if board[0][column] == 0:
            r = 0
            for i in range(0, ROW_COUNT):
                r = i
                if not (board[i][column] == 0):
                    r -= 1
                    break
            board[r][column] = player_piece
            return True
        else:
            return False
    except IndexError:
        print("Wrong Index!!!")
        return False


def get_children(board, player_piece, column_count):
    children = []
    for i in range(column_count):
        temp_board = get_copy(board)
        if add_to_board(temp_board, player_piece, i):
            children.append(temp_board)
    return children


def get_score(board, player_piece, row_count, column_count, number_of_makes, point_dictionary):
    number_of_unfinished_makes = number_of_makes - 1
    score = 0
    # Horizontal check
    for row in board:
        for index in range(column_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            for i in range(number_of_makes):
                if row[index + i] == player_piece:
                    confirmed_assignment += 1
            # if confirmed_assignment == number_of_makes:
            #     return True
            score += point_dictionary.get(confirmed_assignment)

    # Vertical check
    for col in range(column_count):
        for row in range(row_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col] == player_piece:
                    confirmed_assignment += 1
            # if confirmed_assignment == number_of_makes:
            #     return True
            score += point_dictionary.get(confirmed_assignment)

    # top to bottom, left to right diagonal check
    for row in range(row_count - number_of_unfinished_makes):
        for col in range(column_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col + i] == player_piece:
                    confirmed_assignment += 1
            # if confirmed_assignment == number_of_makes:
            #     return True
            score += point_dictionary.get(confirmed_assignment)

    # bottom to top, right to left diagonal check
    for row in range(row_count - number_of_unfinished_makes):
        for col in range(column_count - 1, number_of_unfinished_makes - 1, -1):
            confirmed_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col - i] == player_piece:
                    confirmed_assignment += 1
            # if confirmed_assignment == number_of_makes:
            #     return True
            score += point_dictionary.get(confirmed_assignment)
    return score


def minmax(board, depth, alpha, beta, the_maximising_player, row_count, column_count, number_of_makes,
           point_dictionary):
    player_piece = 1 if the_maximising_player else 2
    if (depth == 0) or is_full(board):
        return get_score(board, player_piece, row_count, column_count, number_of_makes,
                         point_dictionary)

    if the_maximising_player:
        max_score = float('inf')
        for child in get_children(board, player_piece, column_count):
            score = minmax(child, depth - 1, alpha, beta, False, row_count, column_count, number_of_makes,
                           point_dictionary)
            max_score = max((score, max_score))
            alpha = max((alpha, score))
            if beta <= alpha:
                break
        return max_score

    else:
        min_score = float('-inf')
        for child in get_children(board, player_piece, column_count):
            score = minmax(child, depth - 1, alpha, beta, True, row_count, column_count, number_of_makes,
                           point_dictionary)
            min_score = min((score, min_score))
            beta = min((beta, score))
            if beta <= alpha:
                break
        return min_score

# for row in range(ROW_COUNT - 2):
#     for col in range(COLUMN_COUNT -2):
#         print(f"{board[row][col]} ", end="")
#     print("")
# board[5][5] = 1
# board[5][6] = 1
# print(get_score(board, 1, ROW_COUNT, COLUMN_COUNT, NUMBER_OF_MAKES, points))


quit = False
player_one_move = True
while not quit:
    print_board(board)
    if player_one_move:
        try:
            column_1 = int(input("Player one> "))
            if add_to_board(board, PLAYER_ONE_PIECE, column_1):
                if get_score(board, PLAYER_ONE_PIECE, points):
                    print("congrats!! one")
                    quit = True
            else:
                print("Wrong move!!")
                continue
            player_one_move = False
        except ValueError:
            print("Wrong Input!!")
            continue
    else:
        try:
            column_2 = int(input("Player two> "))
            if add_to_board(board, PLAYER_TWO_PIECE, column_2):
                if get_score(board, PLAYER_TWO_PIECE, points):
                    print("congrats!! two")
                    quit = True
            else:
                print("Wrong move!!")
                continue
            player_one_move = True
        except ValueError:
            print("Wrong Input!!")
            continue
