import sys 
import inputbox
import cpu
import gui
from gui import *
from common import *

pygame.init()

opp = [1,0]
depth = 5
player = 1
first_play = 1
n = 1

GAME_EXIT_MSGS = ["You Lose!", "You Win!", "DRAW!"]

def get_square(x,y):
	return [(y*n)/SIZE, (x*n)/SIZE]

def init_board():
	board = [[-1 for x in range(n)] for x in range(n)]
	return board

def check_game_end(board, player, mode):
	msg = GAME_EXIT_MSGS
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
		player = int (inputbox.ask(screen, "0 for cross, 1 for circle"))
		first_play = int (inputbox.ask(screen, "play 0 or 1 first ?"))

	if mode!=3:
		n = int (inputbox.ask(screen, "Enter N"))

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
				print [x,y]
				p = get_square(x,y)
				if board[p[0]][p[1]] == -1:
					board[p[0]][p[1]] = player
			
					draw_board(board,SIZE,n)

					end = check_game_end(board, player, mode)

					if end==2:
						end = cpu_turn(board,opp[player], mode)
						if end != 2:
							first_play = not first_play
							run_game(3)
					else:
						first_play = not first_play
						run_game(3)			

		if mode==2:
			end = cpu_turn(board,player, mode)
			if end==2:
				pass
			pygame.time.wait(100)
			player = opp[player]

def main():
	screen.fill((0,0,0))
	ch = int (inputbox.ask(screen,"Press 1 for CPU v/s You and 2 for CPU v/s CPU"))
	run_game(ch)

if __name__=="__main__":
	main()
