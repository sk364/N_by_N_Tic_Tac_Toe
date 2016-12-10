"""Script to execute CPU and get a best move using Minimax algorithm"""

import copy
from common import board_full, win

OPP = [1, 0]

def eval_rc(board, player, glength, roc):
    """Returns row or column score"""
    score_sum = 0

    clone_board = board

    if roc == "c":
        clone_board = [[board[j][i] for j in xrange(glength)] for i in xrange(glength)]

    for i in xrange(glength):
        score = 0
        if clone_board[i][0] == player:
            score = 1
        else:
            score = -1
        for j in xrange(1, glength):
            if clone_board[i][j] == player and score > 0:
                score = score * 10
            elif board[i][j] == player and score < 0:
                score = 0
                break
            elif board[i][j] == player:
                score = 1
            elif board[i][j] == OPP[player] and score < 0:
                score = score * 10
            elif board[i][j] == OPP[player] and score > 0:
                score = 0
                break
            elif board[i][j] == OPP[player]:
                score = 1
        score_sum = score_sum + score

    return score_sum


def eval_diags(board, player, glength):
    """Returns diagonal score"""
    score = 0
    if board[0][0] == player:
        score = 1
    elif board[0][0] == OPP[player]:
        score = -1
    for i in range(1, glength):
        if board[i][i] == player and score > 0:
            score = score * 10
        elif board[i][j] == player and score < 0:
            score = 0
            break
        elif board[i][j] == player:
            score = 1
        elif board[i][j] == OPP[player] and score < 0:
            score = score * 10
        elif board[i][j] == OPP[player] and score > 0:
            score = 0
            break
        elif board[i][j] == OPP[player]:
            score = 1

    score_sum = score

    score = 0
    if board[glength - 1][0] == player:
        score = 1
    else:
        score = -1
    for i in range(1, glength):
        if board[glength - i - 1][i] == player and score > 0:
            score = score * 10
        elif board[i][j] == player and score < 0:
            score = 0
            break
        elif board[i][j] == player:
            score = 1
        elif board[i][j] == OPP[player] and score < 0:
            score = score * 10
        elif board[i][j] == OPP[player] and score > 0:
            score = 0
            break
        elif board[i][j] == OPP[player]:
            score = 1

    score_sum = score_sum + score

    return score_sum


def evaluate(board, player, glength):
    """Evaluates the score for the player based on horizontal, vertical and diagonal advantages"""
    score = eval_rc(board, player, glength, "r")
    score += eval_rc(board, player, glength, "c")
    score += eval_diags(board, player, glength)

    return score

def get_moves(board, glength):
    """Returns all possible moves"""
    moves = []
    for i in range(glength):
        for j in range(glength):
            if board[i][j] == -1:
                moves = moves + [[i, j]]
    return moves


def gen_board(board, player, pos):
    """Returns a new clone board by playing a move"""
    new_board = copy.deepcopy(board)
    new_board[pos[0]][pos[1]] = player
    return new_board


def if_second_move(board, glength):
    """Returns True if it is the second move of the game, otherwise False"""
    check = 0
    for i in xrange(glength):
        for j in xrange(glength):
            if board[i][j] == 0 or board[i][j] == 1:
                check += 1
            if check > 1:
                return False
    return True


def minimax(board, player, depth, glength):
    """Returns the best move for the CPU by traversing
    all best CPU and worst user moves with depth
    """
    moves = get_moves(board, glength)

    if not moves:
        return None

    if len(moves) == 1 or if_second_move(board, glength):
        return moves[0]

    best_move = moves[0]
    best_score = 0.0

    for move in moves:
        clone_board = gen_board(board, player, move)
        if win(clone_board, player, glength):
            return move

    for move in moves:
        clone_board = gen_board(board, OPP[player], move)
        if win(clone_board, OPP[player], glength):
            return move

    for move in moves:
        clone_board = gen_board(board, player, move)

        if win(clone_board, player, glength):
            return move

        score = min_play(clone_board, OPP[player], depth, glength)

        if best_score < score:
            best_score = score
            best_move = move

    return best_move


def min_play(board, player, depth, glength):
    """Returns the worst score for the player"""
    moves = get_moves(board, glength)

    if not moves or depth == 0:
        return evaluate(board, player, glength)

    best_score = float('inf')

    for move in moves:
        clone_board = gen_board(board, player, move)

        if win(clone_board, player, glength):
            return evaluate(clone_board, player, glength)

        score = max_play(clone_board, OPP[player], depth - 1, glength)

        if score < best_score:
            best_score = score

    return best_score


def max_play(board, player, depth, glength):
    """Returns the best score for the CPU"""
    moves = get_moves(board, glength)

    if not moves or depth == 0:
        return evaluate(board, player, glength)

    best_score = float('-inf')

    for move in moves:
        clone_board = gen_board(board, player, move)

        if win(clone_board, player, glength):
            return evaluate(clone_board, player, glength)

        score = max_play(clone_board, OPP[player], depth - 1, glength)

        if score > best_score:
            best_score = score

    return best_score
