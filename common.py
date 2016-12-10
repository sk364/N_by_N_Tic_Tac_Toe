"""
Common functions used by two or more scripts
"""

def board_full(board, glength):
    """
    Returns True if the board is full or False if not
    """
    for i in range(glength):
        for j in range(glength):
            if board[i][j] == -1:
                return False

    return True


def win(board, player, glength):
    """
    Returns if there is a win situation for the player
    """
    for i in range(glength):
        flag = False
        for j in range(glength):
            if board[i][j] != player:
                flag = True
                break
        if not flag:
            return True

    for i in range(glength):
        flag = False
        for j in range(glength):
            if board[j][i] != player:
                flag = True
                break
        if not flag:
            return True
    flag = False
    for i in range(glength):
        if board[i][i] != player:
            flag = True
            break
    if not flag:
        return True

    flag = False
    for i in range(glength):
        if board[glength - i - 1][i] != player:
            flag = True
            break

    if not flag:
        return True

    return 0
