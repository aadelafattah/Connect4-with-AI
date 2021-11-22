def print_board(board):
    print("1 2 3 4 5 6 7")
    print("_____________")
    for row in board:
        for item in row:
            print(f"{item} ", end="")
        print("")
    print("~~~~~~~~~~~~~")


def is_full(board):
    for row in board:
        for item in row:
            if item == 0:
                return False
    return True


def is_empty(board):
    for row in board:
        for item in row:
            if not (item == 0):
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


def add_to_board(board, player_piece, row_count, column):
    try:
        if board[0][column] == 0:
            r = 0
            for i in range(0, row_count):
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


def get_children(board, player_piece, row_count, column_count):
    children = []
    for i in range(column_count):
        temp_board = get_copy(board)
        if add_to_board(temp_board, player_piece, row_count, i):
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


def minimize(board, depth, alpha, beta, the_maximising_player, row_count, column_count, number_of_makes,
             point_dictionary):
    player_piece = 2 if the_maximising_player else 1
    if (depth == 0) or is_full(board):
        return board, get_score(board, player_piece, row_count, column_count, number_of_makes,
                                point_dictionary) - get_score(board, 1 if the_maximising_player else 2, row_count,
                                                              column_count, number_of_makes, point_dictionary)

    (min_child, min_utility) = (None, float('inf'))

    for child in get_children(board, player_piece, row_count, column_count):
        (new_child, utility) = maximize(child, depth - 1, alpha, beta, True, row_count, column_count, number_of_makes,
                                        point_dictionary)

        if utility < min_utility:
            (min_child, min_utility) = (child, utility)

        if min_utility <= alpha:
            break
        if min_utility < beta:
            beta = min_utility

    return min_child, min_utility


def maximize(board, depth, alpha, beta, the_maximising_player, row_count, column_count, number_of_makes,
             point_dictionary):
    player_piece = 2 if the_maximising_player else 1
    if (depth == 0) or is_full(board):
        return board, get_score(board, player_piece, row_count, column_count, number_of_makes,
                                point_dictionary) - get_score(board, 1 if the_maximising_player else 2, row_count,
                                                              column_count, number_of_makes, point_dictionary)

    (max_child, max_utility) = (None, float('-inf'))

    for child in get_children(board, player_piece, row_count, column_count):
        new_child, utility = minimize(child, depth - 1, alpha, beta, False, row_count, column_count, number_of_makes,
                                      point_dictionary)

        if utility > max_utility:
            (max_child, max_utility) = (child, utility)

        if max_utility >= beta:
            break
        if max_utility > alpha:
            alpha = max_utility

    return max_child, max_utility


def decide(board, depth, row_count, column_count, number_of_makes,
           point_dictionary):
    (child, max_utility) = maximize(board, depth, float('-inf'), float('inf'), True, row_count, column_count,
                                    number_of_makes, point_dictionary)
    return child, max_utility


def min_max(board, depth, alpha, beta, the_maximising_player, row_count, column_count, number_of_makes,
            point_dictionary):
    player_piece = 2 if the_maximising_player else 1
    if (depth == 0) or is_full(board):
        return board, get_score(board, player_piece, row_count, column_count, number_of_makes,
                                point_dictionary) - get_score(board, 1 if the_maximising_player else 2, row_count,
                                                              column_count, number_of_makes, point_dictionary)

    if the_maximising_player:
        max_child, max_score = None, float('-inf')

        for child in get_children(board, player_piece, row_count, column_count):
            new_child, score = min_max(child, depth - 1, alpha, beta, False, row_count, column_count, number_of_makes,
                                       point_dictionary)
            if score > max_score:
                max_child, max_score = child, score
            alpha = max((alpha, score))
            if beta <= alpha:
                break
        return max_child, float(max_score)

    else:
        min_child, min_score = None, float('inf')
        for child in get_children(board, player_piece, row_count, column_count):
            new_child, score = min_max(child, depth - 1, alpha, beta, True, row_count, column_count, number_of_makes,
                                       point_dictionary)
            if score < min_score:
                min_child, min_score = child, score
            beta = min((beta, score))
            if beta <= alpha:
                break
        return min_child, float(min_score)
