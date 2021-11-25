class Tree:
    def __init__(self, board, parent):
        self.parent = parent
        self.board = board
        self.children = []


def print_tree(tree):
    if tree.board is None:
        print("NO TREE FOUND!!")
    else:
        print_board(tree.board)

    command = input("For next child enter child and position (c,p), or sibling (s,p), or quit(q): ").split(",")
    if command[0].strip().lower().__eq__("q"):
        return True
    if not (len(command) == 2):
        print("WRONG INPUT!!")
    else:
        position = 0
        try:
            position = int(command[1].strip()) - 1
        except ValueError:
            print("WRONG POSITION")
        command = command[0].strip().lower()
        if command.__eq__("c"):
            if (len(tree.children) < 1) or (tree.children is None):
                print("NO TREE FOUND!!")
            else:
                if position < len(tree.children):
                    return print_tree(tree.children[position])
                else:
                    print("WRONG POSITION!!")
        elif command.__eq__("s"):
            if tree.parent is None:
                print("THIS IS THE ROOT TREE!!")
            else:
                if position < len(tree.parent.children):
                    return print_tree(tree.parent.children[position])
                else:
                    print("WRONG POSITION!!")
        else:
            print("WRONG INPUT!!")

    return print_tree(tree)


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


# returns (+ve) number as the points of the move if winning, (-ve) if not winning
def get_score_with_remove(board, player_piece, replacement_piece, row_count, column_count, number_of_makes):
    number_of_unfinished_makes = number_of_makes - 1
    # score = 0
    points = 0
    # Horizontal check
    k = 0
    for row in board:
        for index in range(column_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            replacement_piece_assignment = 0
            for i in range(number_of_makes):
                if row[index + i] == player_piece:
                    confirmed_assignment += 1
                elif row[index + i] == replacement_piece:
                    replacement_piece_assignment += 1
            # if true then we have number_of_makes (4) or bigger in a row, then we  replace them with replacement_piece
            if (confirmed_assignment + replacement_piece_assignment >= number_of_makes) and not (
                    confirmed_assignment == 0):
                replace_in_row(board, k, index, confirmed_assignment + replacement_piece_assignment, replacement_piece)
                # 0 0 0 0 3
                # 0 0 0 0 3
                # 0 0 3 0 3
                # 1 1 3 1 3  --> 4 + 5 - 2 * 4 + 2 = 3
                # return the number of points when winning, or returns a (-ve) number if no winning
                points += confirmed_assignment + replacement_piece_assignment - number_of_makes + 1
        k += 1
        # score += point_dictionary.get(confirmed_assignment)

    # Vertical check
    for col in range(column_count):
        for row in range(row_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            replacement_piece_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col] == player_piece:
                    confirmed_assignment += 1
                elif board[row + i][col] == replacement_piece:
                    replacement_piece_assignment += 1
            # if true then we have number_of_makes (4) in a column or bigger, then we  replace them with
            # replacement_piece
            if (confirmed_assignment + replacement_piece_assignment >= number_of_makes) and (
                    replacement_piece_assignment < number_of_makes):
                replace_in_col(board, row, col, confirmed_assignment + replacement_piece_assignment, replacement_piece)
                # return true meaning that we have a winning move
                points += confirmed_assignment + replacement_piece_assignment - number_of_makes + 1
            # score += point_dictionary.get(confirmed_assignment)

    # top to bottom, left to right diagonal check, type (1)
    for row in range(row_count - number_of_unfinished_makes):
        for col in range(column_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            replacement_piece_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col + i] == player_piece:
                    confirmed_assignment += 1
                elif board[row + i][col + i] == replacement_piece:
                    replacement_piece_assignment += 1
            # if true then we have number_of_makes (4) in a diagonal line, then we  replace them with
            # replacement_piece
            if (confirmed_assignment + replacement_piece_assignment >= number_of_makes) and (
                    replacement_piece_assignment < number_of_makes):
                replace_in_diagonal_1(board, row, col, confirmed_assignment + replacement_piece_assignment,
                                      replacement_piece)
                # return true meaning that we have a winning move
                points += confirmed_assignment + replacement_piece_assignment - number_of_makes + 1
            # score += point_dictionary.get(confirmed_assignment)

    # bottom to top, right to left diagonal check, type (2)
    for row in range(row_count - number_of_unfinished_makes):
        for col in range(column_count - 1, number_of_unfinished_makes - 1, -1):
            confirmed_assignment = 0
            replacement_piece_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col - i] == player_piece:
                    confirmed_assignment += 1
                elif board[row + i][col - i] == replacement_piece:
                    replacement_piece_assignment += 1
            # if true then we have number_of_makes (4) in a diagonal line, then we  replace them with
            # replacement_piece
            if (confirmed_assignment + replacement_piece_assignment >= number_of_makes) and (
                    replacement_piece_assignment < number_of_makes):
                replace_in_diagonal_2(board, row, col, confirmed_assignment + replacement_piece_assignment,
                                      replacement_piece)
                # return true meaning that we have a winning move
                points += confirmed_assignment + replacement_piece_assignment - number_of_makes + 1
            # score += point_dictionary.get(confirmed_assignment)

    return points


def get_utility(board, player_piece, replacement_piece, row_count, column_count, number_of_makes):
    number_of_unfinished_makes = number_of_makes - 1
    score = 0
    # Horizontal check
    for row in board:
        for index in range(column_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            replacement_piece_assignment = 0
            for i in range(number_of_makes):
                if row[index + i] == player_piece:
                    confirmed_assignment += 1
                if row[index + i] == replacement_piece:
                    replacement_piece_assignment += 1
            # if confirmed_assignment == number_of_makes:
            #     return True
            score += 3 ** (confirmed_assignment + replacement_piece_assignment)
            # score += point_dictionary.get(confirmed_assignment)

    # Vertical check
    for col in range(column_count):
        for row in range(row_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            replacement_piece_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col] == player_piece:
                    confirmed_assignment += 1
                if board[row + i][col] == replacement_piece:
                    replacement_piece_assignment += 1
            # if confirmed_assignment == number_of_makes:
            #     return True
            score += 3 ** (confirmed_assignment + replacement_piece_assignment)
            # score += point_dictionary.get(confirmed_assignment)

    # top to bottom, left to right diagonal check
    for row in range(row_count - number_of_unfinished_makes):
        for col in range(column_count - number_of_unfinished_makes):
            confirmed_assignment = 0
            replacement_piece_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col + i] == player_piece:
                    confirmed_assignment += 1
                if board[row + i][col + i] == replacement_piece:
                    replacement_piece_assignment += 1
            # if confirmed_assignment == number_of_makes:
            #     return True
            score += 3 ** (confirmed_assignment + replacement_piece_assignment)
            # score += point_dictionary.get(confirmed_assignment)

    # bottom to top, right to left diagonal check
    for row in range(row_count - number_of_unfinished_makes):
        for col in range(column_count - 1, number_of_unfinished_makes - 1, -1):
            confirmed_assignment = 0
            replacement_piece_assignment = 0
            for i in range(number_of_makes):
                if board[row + i][col - i] == player_piece:
                    confirmed_assignment += 1
                if board[row + i][col - i] == replacement_piece:
                    replacement_piece_assignment += 1
            # if confirmed_assignment == number_of_makes:
            #     return True
            score += 3 ** (confirmed_assignment + replacement_piece_assignment)
            # score += point_dictionary.get(confirmed_assignment)
    return score


def minimize(board, pruning, depth, alpha, beta, row_count, column_count, number_of_makes, pieces, tree):
    # player_piece = 2 if the_maximising_player else 1
    if (depth == 0) or is_full(board):
        utility = get_utility(board, pieces.get("player2"), pieces.get("replacement2"), row_count, column_count,
                              number_of_makes) - get_utility(board, pieces.get("player1"),
                                                             pieces.get("replacement1"), row_count, column_count,
                                                             number_of_makes)
        return board, utility, tree

    (min_child, min_utility) = (None, float('inf'))

    for child in get_children(board, pieces.get("player1"), row_count, column_count):
        temp_tree = Tree(child, tree)
        (new_child, utility, child_tree) = maximize(child, pruning, depth - 1, alpha, beta, row_count, column_count,
                                                    number_of_makes, pieces, temp_tree)

        if utility < min_utility:
            (min_child, min_utility) = (child, utility)

        tree.children.append(child_tree)
        if pruning:
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility

    return min_child, min_utility, tree


def maximize(board, pruning, depth, alpha, beta, row_count, column_count, number_of_makes, pieces, tree):
    # player_piece = 2 if the_maximising_player else 1
    if (depth == 0) or is_full(board):
        utility = get_utility(board, pieces.get("player2"), pieces.get("replacement2"), row_count, column_count,
                              number_of_makes) - get_utility(board, pieces.get("player1"),
                                                             pieces.get("replacement1"), row_count,
                                                             column_count, number_of_makes)
        return board, utility, tree

    (max_child, max_utility) = (None, float('-inf'))

    for child in get_children(board, pieces.get("player2"), row_count, column_count):
        temp_tree = Tree(child, tree)
        new_child, utility, child_tree = minimize(child, pruning, depth - 1, alpha, beta, row_count, column_count,
                                                  number_of_makes, pieces, temp_tree)

        if utility > max_utility:
            (max_child, max_utility) = (child, utility)

        tree.children.append(child_tree)

        if pruning:
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility

    return max_child, max_utility, tree


def decide(board, pruning, depth, row_count, column_count, number_of_makes, pieces):
    temp_tree = Tree(board, None)
    (child, max_utility, tree) = maximize(board, pruning, depth, float('-inf'), float('inf'), row_count, column_count,
                                          number_of_makes, pieces, temp_tree)

    return child, max_utility, tree


def min_max(board, pruning, depth, the_maximising_player, alpha, beta, row_count, column_count, number_of_makes,
            pieces):
    if (depth == 0) or is_full(board):
        return board, get_utility(board, pieces.get("player2"), pieces.get("replacement2"), row_count, column_count,
                                  number_of_makes) - get_utility(board, pieces.get("player1"),
                                                                 pieces.get("replacement1"), row_count, column_count,
                                                                 number_of_makes)

    if the_maximising_player:
        max_child, max_score = None, float('-inf')

        for child in get_children(board, pieces.get("player2"), row_count, column_count):
            new_child, score = min_max(child, pruning, depth - 1, alpha, beta, False, row_count, column_count,
                                       number_of_makes,
                                       pieces)
            if score > max_score:
                max_child, max_score = child, score

            if pruning:
                alpha = max((alpha, score))
                if beta <= alpha:
                    break
        return max_child, float(max_score)

    else:
        min_child, min_score = None, float('inf')
        for child in get_children(board, pieces.get("player1"), row_count, column_count):
            new_child, score = min_max(child, pruning, depth - 1, alpha, beta, True, row_count, column_count,
                                       number_of_makes,
                                       pieces)
            if score < min_score:
                min_child, min_score = child, score

            if pruning:
                beta = min((beta, score))
                if beta <= alpha:
                    break
        return min_child, float(min_score)
