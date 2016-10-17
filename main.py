import sys 
import inputbox
import cpu
import gui
import copy
from gui import *
from common import *

pygame.init()

opp = [1,0]
depth = 3
player = -1
first_play = -1
n = 0

GAME_EXIT_MSGS = ["You Lose!", "You Win!", "DRAW!"]

def get_rcscore(board, p, n, fl, c=0):
    scr = 0

    if c==0:
	for i in xrange(n):
	    prev = 0
	    end = False
	    for j in xrange(n):
	        if board[i][j] == p:
		    end = True
		    if prev:
		        fl[i][j] = 1
		        fl[i][j-1] = 1
		    elif fl[i][j]==0:
		        fl[i][j] = -1
		    prev += 1
	        else:
		    if prev!=1:
		        scr += prev
		    prev = 0
		    end = False
	    if end and prev!=1:
	        scr += prev

    if c==1:
        for i in xrange(n):
            prev = 0
            end = False
            for j in xrange(n):
                if board[j][i] == p:
                    end = True
                    if prev:
                        fl[j][i] = 1
                        fl[j-1][i] = 1
                    elif fl[j][i]==0:
                        fl[j][i] = -1
                    prev += 1
                else:
                    if prev!=1:
                        scr += prev
                    prev = 0
                    end = False
            if end and prev!=1:
                scr += prev
        
    return scr

def get_diagscore(board, p, n, fl, c=0):
    scr = 0
    scr1 = 0
    if c==0:
        for k in xrange(n):
            j = k
            prev = 0
            prev1 = 0
            for i in xrange(n+1):
                if j==n or i==n:
                    if prev!=1:
                        scr += prev
                    if prev1!=1:
                        scr1 += prev1
                    break

                if board[i][j] == p:
                    if prev:
                        fl[i][j] = 1
                        fl[i-1][j-1] = 1
                    elif fl[i][j]==0:
                        fl[i][j] = -1
                    prev += 1
                else:
                    if prev!=1:
                        scr += prev
                    prev = 0
                    
                if board[j][i] == p and i!=j:
                    if prev1:
                        fl[j][i] = 1
                        fl[j-1][i-1] = 1
                    elif fl[j][i]==0:
                        fl[j][i] = -1
                    prev1 += 1
                else:
                    if prev1!=1:
                        scr1 += prev1
                    prev1 = 0
                j += 1

    elif c==1:
        for k in xrange(n):
            j=k
            prev = 0
            prev1 = 0
            for i in xrange(n+1):
                if j<0:
                    if prev!=1:
                        scr += prev
                    if prev1!=1:
                        scr1 += prev1
			print k
                    break
                

                if board[i][j] == p:
                    if prev:
                        fl[i][j] = 1
                        fl[i-1][j+1] = 1
                    elif fl[i][j]==0:
                        fl[i][j] = -1
                    prev += 1
                else:
                    if prev!=1:
                        scr += prev
                    prev = 0

                if board[n-i-1][n-j-1] == p and k!=n-1:
                    if prev1:
                        fl[n-i-1][n-j-1] = 1
                        fl[n-i][n-j-2] = 1
                    elif fl[n-i-1][n-j-1]==0:
                        fl[n-i-1][n-j-1] = -1
                    prev1 += 1
                else:
                    if prev1!=1:
                        scr1 += prev1
                    prev1 = 0

                j -= 1
        
    return scr + scr1

def leftovers(fl, n):
    scr = 0
    for i in xrange(n):
        for j in xrange(n):
            if fl[i][j] == -1:
                scr += 1
                fl[i][j] = 1
    return scr

def get_score(board, p, n):
	fl = [[0 for i in xrange(n)] for i in xrange(n)]

	score = get_rcscore(board, p, n, fl)
	score += get_rcscore(board, p, n, fl, c=1)
	score += get_diagscore(board, p, n, fl)
	score += get_diagscore(board, p, n, fl, c=1)
	score += leftovers(fl, n)

	return score

def get_square(x,y):
	return [(y*n)/SIZE, (x*n)/SIZE]

def init_board():
	board = [[-1 for x in range(n)] for x in range(n)]
	return board

def check_game_end(board, player, mode):
	'''msg = GAME_EXIT_MSGS
	if mode==2:
		msg[0] = "O wins"
		msg[1] = "X wins"

	if win(board,opp[player],n):
		display_message(msg[0])
		return 1
	if win(board,player,n):
		display_message(msg[1])
		return -1
	if board_full(board, n):
		display_message(msg[2])
	        return 0

	return 2'''

	if board_full(board, n):
		if player==0:
			x_scr = get_score(board, player, n)
			o_scr = get_score(board, opp[player], n)
		else:
			o_scr = get_score(board, player, n)
			x_scr = get_score(board, opp[player], n)
		display_message("Score - O = "+str(o_scr) + " X = " + str(x_scr))
		return 1

	return 2

def cpu_turn(board, player, mode):
	cpu_move = cpu.minimax(board, player, depth, n)
	if cpu_move:
		board[cpu_move[0]][cpu_move[1]] = player
		draw_board(board,SIZE,n)

	end = check_game_end(board,opp[player], mode)

	return end

def run_game(mode):
	global player, first_play, n

	if mode==1:
		while player not in [0,1]:
			x = inputbox.ask(screen,"Press 1 for circle, 0 for cross")
                	if len(x) == 1 and x in ['1','0']:
                        	player = int (x)

		while first_play not in [0,1]:
			x = inputbox.ask(screen,"Press 0 for cross to play first, 1 for circle")
	                if len(x) == 1 and x in ['1','0']:
        	                first_play = int (x)
	
	if mode!=3:
		while n<=0 or n>8:
			x = inputbox.ask(screen, "Enter N")
			if len(x)==1 and x in [str(i) for i in xrange(1,8)]:
				n = int (x)

	board = init_board()
	draw_board(board,SIZE,n)

	if first_play == opp[player] and mode!=2:
		cpu_turn(board,opp[player], mode)

	game_loop = True
	while game_loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN and mode!=2:
				x,y = pygame.mouse.get_pos()
				p = get_square(x,y)
				if board[p[0]][p[1]] == -1:
					board[p[0]][p[1]] = player
			
					draw_board(board,SIZE,n)

					end = check_game_end(board, player, mode)

					if end==2:
						end = cpu_turn(board,opp[player], mode)
						'''if end != 2:
							first_play = not first_play
							run_game(3)'''
					'''else:
						first_play = not first_play
						run_game(3)'''

		if mode==2:
			end = cpu_turn(board,player, mode)
			if end==2:
				pass
			pygame.time.wait(100)
			player = opp[player]

def main():
	screen.fill((0,0,0))
	ch = -1
	while ch not in [1,2]:
		x = inputbox.ask(screen,"Press 1 for CPU v/s You and 2 for CPU v/s CPU")
		if len(x) == 1 and x[0] in ['1','2']:
			ch = int (x[0])

	run_game(ch)

if __name__=="__main__":
	main()
