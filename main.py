"""
The main program to run the game
"""

import sys
import copy
import inputbox
import cpu
import gui
from gui import *
from common import board_full, win

pygame.init()

OPP = [1, 0]
DEPTH = 3
PLAYER = -1
FIRST_PLAY = -1
GLENGTH = 0
USCORE = 0
CPUSCORE = 0

GAME_EXIT_MSGS = ["You Lose!", "You Win!", "DRAW!"]


def get_rcscore(board, player, glength, flag, check=0):
    """
    Returns the row/column score of a player after the game is over
    """
    scr = 0

    if check == 0:
        for i in xrange(glength):
            prev = 0
            end = False
            for j in xrange(glength):
                if board[i][j] == player:
                    end = True
                    if prev:
                        flag[i][j] = 1
                        flag[i][j - 1] = 1
                    elif flag[i][j] == 0:
                        flag[i][j] = -1
                    prev += 1
                else:
                    if prev != 1:
                        scr += prev
                    prev = 0
                    end = False
            if end and prev != 1:
                scr += prev

    if check == 1:
        for i in xrange(glength):
            prev = 0
            end = False
            for j in xrange(glength):
                if board[j][i] == player:
                    end = True
                    if prev:
                        flag[j][i] = 1
                        flag[j - 1][i] = 1
                    elif flag[j][i] == 0:
                        flag[j][i] = -1
                    prev += 1
                else:
                    if prev != 1:
                        scr += prev
                    prev = 0
                    end = False
            if end and prev != 1:
                scr += prev

    return scr


def get_main_diagscore(board, player, glength, flag):
    """
    Returns the main diagonal score of a player after the game is over
    """
    scr = 0
    scr1 = 0
    for k in xrange(glength):
        j = k
        prev = 0
        prev1 = 0
        for i in xrange(glength + 1):
            if j == glength or i == glength:
                if prev != 1:
                    scr += prev
                if prev1 != 1:
                    scr1 += prev1
                break

            if board[i][j] == player:
                if prev:
                    flag[i][j] = 1
                    flag[i - 1][j - 1] = 1
                elif flag[i][j] == 0:
                    flag[i][j] = -1
                prev += 1
            else:
                if prev != 1:
                    scr += prev
                prev = 0

            if board[j][i] == player and i != j:
                if prev1:
                    flag[j][i] = 1
                    flag[j - 1][i - 1] = 1
                elif flag[j][i] == 0:
                    flag[j][i] = -1
                prev1 += 1
            else:
                if prev1 != 1:
                    scr1 += prev1
                prev1 = 0
            j += 1
    return scr + scr1

def get_other_diagscore(board, player, glength, flag):
    """
    Returns the other diagonal score of a player after the game is over
    """

    scr = 0
    scr1 = 0
    for k in xrange(glength):
        j = k
        prev = 0
        prev1 = 0
        for i in xrange(glength + 1):
            if j < 0:
                if prev != 1:
                    scr += prev
                if prev1 != 1:
                    scr1 += prev1
                break

            if board[i][j] == player:
                if prev:
                    flag[i][j] = 1
                    flag[i - 1][j + 1] = 1
                elif flag[i][j] == 0:
                    flag[i][j] = -1
                prev += 1
            else:
                if prev != 1:
                    scr += prev
                prev = 0

            if board[glength - i - 1][glength - j - 1] == player and k != glength - 1:
                if prev1:
                    flag[glength - i - 1][glength - j - 1] = 1
                    flag[glength - i][glength - j - 2] = 1
                elif flag[glength - i - 1][glength - j - 1] == 0:
                    flag[glength - i - 1][glength - j - 1] = -1
                prev1 += 1
            else:
                if prev1 != 1:
                    scr1 += prev1
                prev1 = 0

            j -= 1

    return scr + scr1


def leftovers(flag, glength):
    """
    Returns the score of the singular (unmatched) move
    """
    scr = 0
    for i in xrange(glength):
        for j in xrange(glength):
            if flag[i][j] == -1:
                scr += 1
                flag[i][j] = 1
    return scr


def get_score(board, player, glength):
    """
    Returns the total score of a player
    """
    flag = [[0 for i in xrange(glength)] for i in xrange(glength)]

    score = get_rcscore(board, player, glength, flag)
    score += get_rcscore(board, player, glength, flag, check=1)
    score += get_main_diagscore(board, player, glength, flag)
    score += get_other_diagscore(board, player, glength, flag)
    score += leftovers(flag, glength)

    return score


def get_square(x_coord, y_coord):
    """
    Returns the [row_number, column_number]
    """
    return [(y_coord * GLENGTH) / SIZE, (x_coord * GLENGTH) / SIZE]


def init_board():
    """
    Initializes the board, sets -1 for empty blocks
    """
    board = [[-1 for x in range(GLENGTH)] for x in range(GLENGTH)]
    return board


def check_game_end(board, player, mode):
    """
    Returns 1 if the game ended or 2 if not
    """

    global USCORE, CPUSCORE
    if board_full(board, GLENGTH):
        if player == 0:
            x_scr = get_score(board, player, GLENGTH)
            o_scr = get_score(board, OPP[player], GLENGTH)
            USCORE += x_scr
            CPUSCORE += o_scr
        else:
            o_scr = get_score(board, player, GLENGTH)
            x_scr = get_score(board, OPP[player], GLENGTH)
            USCORE += o_scr
            CPUSCORE += x_scr
        display_message("Score - O = " + str(o_scr) + ", X = " + str(x_scr))
        return 1

    return 2


def cpu_turn(board, player, mode):
    """
    Returns the move by the cpu
    """
    cpu_move = cpu.minimax(board, player, DEPTH, GLENGTH)
    if cpu_move:
        board[cpu_move[0]][cpu_move[1]] = player
        draw_board(board, SIZE, GLENGTH)

    end = check_game_end(board, OPP[player], mode)

    return end


def run_game(mode):
    """
    Runs the game and quits on user call
    """
    global PLAYER, FIRST_PLAY, GLENGTH

    if mode == 1:
        while PLAYER not in [0, 1]:
            ans = inputbox.ask(SCREEN, "Press 1 for circle, 0 for cross")
            if len(ans) == 1 and ans in ['1', '0']:
                PLAYER = int(ans)

        while FIRST_PLAY not in [0, 1]:
            ans = inputbox.ask(
                SCREEN, "Press 0 for cross to play first, 1 for circle")
            if len(ans) == 1 and ans in ['1', '0']:
                FIRST_PLAY = int(ans)

    if mode != 3:
        while GLENGTH <= 0 or GLENGTH > 8:
            ans = inputbox.ask(SCREEN, "Enter N")
            if len(ans) == 1 and ans in [str(i) for i in xrange(1, 8)]:
                GLENGTH = int(ans)

    board = init_board()
    draw_board(board, SIZE, GLENGTH)

    if FIRST_PLAY == OPP[PLAYER] and mode != 2:
        cpu_turn(board, OPP[PLAYER], mode)

    game_loop = True
    rounds = 0
    first_turn = True
    while game_loop:
        if rounds % 2 and first_turn == True and FIRST_PLAY == OPP[PLAYER]:
            cpu_turn(board, OPP[PLAYER], mode)
            first_turn = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and mode != 2:
                x_coord, y_coord = pygame.mouse.get_pos()
                sqr = get_square(x_coord, y_coord)
                if board[sqr[0]][sqr[1]] == -1:
                    board[sqr[0]][sqr[1]] = PLAYER

                    draw_board(board, SIZE, GLENGTH)

                    end = check_game_end(board, PLAYER, mode)

                    if end == 1:
                        rounds += 1
                        if rounds != 5:
                            board = init_board()
                            FIRST_PLAY = OPP[PLAYER]
                            draw_board(board, SIZE, GLENGTH)
                            first_turn = True
                        else:
                            SCREEN.fill((0, 0, 0))
                            display_message("All rounds over!")
                            display_message("Score: You - "+str(USCORE)+", CPU - "+str(CPUSCORE), off_height=60)
                            pygame.time.wait(2000)
                        end = -1

                    if end == 2:
                        end = cpu_turn(board, OPP[PLAYER], mode)

                    if end == 1:
                        rounds += 1
                        if rounds < 5:
                            board = init_board()
                            FIRST_PLAY = OPP[PLAYER]
                            draw_board(board, SIZE, GLENGTH)
                            first_turn = False
                        else:
                            SCREEN.fill((0, 0, 0))
                            display_message("All rounds over!")
                            display_message("Score: You - "+str(USCORE)+", CPU - "+str(CPUSCORE), off_height=60)
                            pygame.time.wait(5000)
                        end = -1


        if mode == 2:
            end = cpu_turn(board, PLAYER, mode)
            if end == 2:
                pass
            pygame.time.wait(100)
            PLAYER = OPP[PLAYER]


def main():
    """
    Main program to call appropriate methods to initialize and run the game
    """

    black = (0, 0, 0)
    SCREEN.fill(black)
    choice = -1
    while choice not in [1, 2]:
        ans = inputbox.ask(
            SCREEN, "Press 1 for CPU v/s You and 2 for CPU v/s CPU")
        if len(ans) == 1 and ans[0] in ['1', '2']:
            choice = int(ans[0])

    run_game(choice)

if __name__ == "__main__":
    main()
