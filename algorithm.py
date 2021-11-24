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


def replace_in_row(board, start_row, start_col, number_of_makes, replacement_piece):
    for j in range(start_col, start_col + number_of_makes):
        board[start_row][j] = replacement_piece


def replace_in_col(board, start_row, start_col, number_of_makes, replacement_piece):
    for j in range(start_row, start_row + number_of_makes):
        board[j][start_col] = replacement_piece


def replace_in_diagonal_1(board, start_row, start_col, number_of_makes, replacement_piece):
    i = start_row
    j = start_col
    while (i < start_row + number_of_makes) and (j < start_col + number_of_makes):
        board[i][j] = replacement_piece
        i += 1
        j += 1


def replace_in_diagonal_2(board, start_row, start_col, number_of_makes, replacement_piece):
    i = start_row
    j = start_col
    while (i < start_row + number_of_makes) and (j > start_col - number_of_makes):
        board[i][j] = replacement_piece
        i += 1
        j -= 1


def get_score_with_remove(board, player_piece, replacement_piece, row_count, column_count, number_of_makes):
    number_of_unfinished_makes = number_of_makes - 1
    score = 0
    # Horizontal check
    k = 0
    for row in board:
        for index in range(column_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            for i in range(number_of_makes):
                if row[index + i] == player_piece:
                    confirmed_assignment += 1

            if confirmed_assignment == number_of_makes:
                # if true then we have number_of_makes (4) in a row, then we  replace them with replacement_piece
                replace_in_row(board, k, index, number_of_makes, replacement_piece)
                # return true meaning that we have a winning move
                return True
        k += 1
        # score += point_dictionary.get(confirmed_assignment)

    # Vertical check
    for col in range(column_count):
        for row in range(row_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col] == player_piece:
                    confirmed_assignment += 1
            if confirmed_assignment == number_of_makes:
                # if true then we have number_of_makes (4) in a column, then we  replace them with replacement_piece
                replace_in_col(board, row, col, number_of_makes, replacement_piece)
                # return true meaning that we have a winning move
                return True
            # score += point_dictionary.get(confirmed_assignment)

    # top to bottom, left to right diagonal check, type (1)
    for row in range(row_count - number_of_unfinished_makes):
        for col in range(column_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col + i] == player_piece:
                    confirmed_assignment += 1
            if confirmed_assignment == number_of_makes:
                # if true then we have number_of_makes (4) in a diagonal line, then we  replace them with
                # replacement_piece
                replace_in_diagonal_1(board, row, col, number_of_makes, replacement_piece)
                # return true meaning that we have a winning move
                return True
            # score += point_dictionary.get(confirmed_assignment)

    # bottom to top, right to left diagonal check, type (2)
    for row in range(row_count - number_of_unfinished_makes):
        for col in range(column_count - 1, number_of_unfinished_makes - 1, -1):
            confirmed_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col - i] == player_piece:
                    confirmed_assignment += 1
            if confirmed_assignment == number_of_makes:
                # if true then we have number_of_makes (4) in a diagonal line, then we  replace them with
                # replacement_piece
                replace_in_diagonal_2(board, row, col, number_of_makes, replacement_piece)
                # return true meaning that we have a winning move
                return True
            # score += point_dictionary.get(confirmed_assignment)

    # this move didn't give a win
    return False


def get_utility(board, player_piece, row_count, column_count, number_of_makes, point_dictionary):
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


def minimize(board, pruning, depth, alpha, beta, the_maximising_player, row_count, column_count, number_of_makes,
             point_dictionary):
    player_piece = 2 if the_maximising_player else 1
    if (depth == 0) or is_full(board):
        return board, get_utility(board, player_piece, row_count, column_count, number_of_makes,
                                  point_dictionary) - get_utility(board, 1 if the_maximising_player else 2, row_count,
                                                                  column_count, number_of_makes, point_dictionary)

    (min_child, min_utility) = (None, float('inf'))

    for child in get_children(board, player_piece, row_count, column_count):
        (new_child, utility) = maximize(child, pruning, depth - 1, alpha, beta, True, row_count, column_count,
                                        number_of_makes,
                                        point_dictionary)

        if utility < min_utility:
            (min_child, min_utility) = (child, utility)

        if pruning:
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility

    return min_child, min_utility


def maximize(board, pruning, depth, alpha, beta, the_maximising_player, row_count, column_count, number_of_makes,
             point_dictionary):
    player_piece = 2 if the_maximising_player else 1
    if (depth == 0) or is_full(board):
        return board, get_utility(board, player_piece, row_count, column_count, number_of_makes,
                                  point_dictionary) - get_utility(board, 1 if the_maximising_player else 2, row_count,
                                                                  column_count, number_of_makes, point_dictionary)

    (max_child, max_utility) = (None, float('-inf'))

    for child in get_children(board, player_piece, row_count, column_count):
        new_child, utility = minimize(child, pruning, depth - 1, alpha, beta, False, row_count, column_count,
                                      number_of_makes,
                                      point_dictionary)

        if utility > max_utility:
            (max_child, max_utility) = (child, utility)

        if pruning:
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility

    return max_child, max_utility


def decide(board, pruning, depth, row_count, column_count, number_of_makes,
           point_dictionary):
    (child, max_utility) = maximize(board, pruning, depth, float('-inf'), float('inf'), True, row_count, column_count,
                                    number_of_makes, point_dictionary)

    return child, max_utility


def min_max(board, pruning, depth, alpha, beta, the_maximising_player, row_count, column_count, number_of_makes,
            point_dictionary):
    player_piece = 2 if the_maximising_player else 1
    if (depth == 0) or is_full(board):
        return board, get_utility(board, player_piece, row_count, column_count, number_of_makes,
                                  point_dictionary) - get_utility(board, 1 if the_maximising_player else 2, row_count,
                                                                  column_count, number_of_makes, point_dictionary)

    if the_maximising_player:
        max_child, max_score = None, float('-inf')

        for child in get_children(board, player_piece, row_count, column_count):
            new_child, score = min_max(child, pruning, depth - 1, alpha, beta, False, row_count, column_count,
                                       number_of_makes,
                                       point_dictionary)
            if score > max_score:
                max_child, max_score = child, score

            if pruning:
                alpha = max((alpha, score))
                if beta <= alpha:
                    break
        return max_child, float(max_score)

    else:
        min_child, min_score = None, float('inf')
        for child in get_children(board, player_piece, row_count, column_count):
            new_child, score = min_max(child, pruning, depth - 1, alpha, beta, True, row_count, column_count,
                                       number_of_makes,
                                       point_dictionary)
            if score < min_score:
                min_child, min_score = child, score

            if pruning:
                beta = min((beta, score))
                if beta <= alpha:
                    break
        return min_child, float(min_score)
