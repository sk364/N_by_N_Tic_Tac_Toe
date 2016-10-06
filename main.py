import pygame, sys, inputbox, cpu
from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((400,400),0,32)

opp = [1,0]

def get_square(x,y,size):
	return [y/size, x/size]

def draw_board(board, size, n):
	SIZE = size

	BLACK = (0,0,0)
	WHITE = (255,255,255)

	screen.fill(WHITE)

	for i in range(n):
		for j in range(n):
			pygame.draw.rect(screen,BLACK, ((j*SIZE/n, i*SIZE/n),(SIZE/n,SIZE/n)),4)

	for i in range(n):
		for j in range(n):
			if board[i][j]==1:
				pygame.draw.circle(screen,BLACK, ((SIZE/(2*n))*((2*j)+1),(SIZE/(2*n))*((2*i)+1)),SIZE/(2*n) - 4, 4)
			elif board[i][j]==0:
				pygame.draw.line(screen, BLACK, (j*SIZE/n+5,i*SIZE/n+5), ((j+1)*SIZE/n-5,(i+1)*SIZE/n-5), 4)
				pygame.draw.line(screen, BLACK, ((j+1)*SIZE/n-5,i*SIZE/n+5), (j*SIZE/n+5,(i+1)*SIZE/n-5), 4)
	pygame.display.update()

def display_message(msg):
	BLUE = (0,0,200)
	
	font = pygame.font.SysFont(None, 100)

	label = font.render(msg,True,BLUE)

	x = (screen.get_rect().width - label.get_rect().width)/2
	y = (screen.get_rect().height - label.get_rect().height)/2

	screen.blit(label, (x,y))
	
	pygame.display.flip()

	pygame.time.wait(1000)

def board_full(board,n):
	for i in range(n):
		for j in range(n):
			if board[i][j] == -1:
				return 0

	return 1

def win(board, player, n):
	for i in range(n):
		fl = 0
		for j in range(n):
			if board[i][j]!=player:
				fl=1
				break
		if fl==0:
			return 1

	for i in range(n):
                fl = 0
                for j in range(n):
                        if board[j][i]!=player:
                                fl=1
                                break
                if fl==0:
                        return 1
	fl = 0
	for i in range(n):
		if board[i][i]!=player:
			fl = 1
			break
	if fl==0:
		return 1

	fl = 0
	for i in range(n):
		if board[n-i-1][i]!=player:
			fl = 1
			break

	if fl==0:
		return 1

	return 0

def cpu_turn(board, player, n, depth, size):
	cpu_move = cpu.minimax(board, player, depth, n)
	if cpu_move:
		board[cpu_move[0]][cpu_move[1]] = player
		draw_board(board,size,n)

	if board_full(board,n):
		display_message("Draw!")
		main()

	if win(board,player,n):
		display_message("You Lose")
		main()
	if win(board,opp[player],n):
                display_message("You Win")
                main()


def init_board(n):
	board = [[-1 for x in range(n)] for x in range(n)]
	return board

def run_human_vs_cpu():
	SIZE = 400

	depth = 2

	player = int (inputbox.ask(screen, "0 for cross, 1 for circle"))
	n = int (inputbox.ask(screen, "Enter N"))
	first_play = int (inputbox.ask(screen, "play 0 or 1 first ?"))

	board = init_board(n)

	draw_board(board,SIZE,n)

	if first_play == opp[player]:
		cpu_turn(board,opp[player],n,depth,SIZE)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				x,y = pygame.mouse.get_pos()
				p = get_square(x,y,SIZE/n)
				if board[p[0]][p[1]] == -1:
					board[p[0]][p[1]] = player
			
					draw_board(board,SIZE,n)

					if board_full(board, n):
						display_message("Draw!")
					        main()
					if win(board,opp[player],n):
						display_message("You Lose")
						main()
					if win(board,player,n):
						display_message("You Win")
						main()

					cpu_turn(board,opp[player],n,depth,SIZE)


def run_cpu_vs_cpu():
	SIZE = 400

	depth = 1
	
        n = int (inputbox.ask(screen, "Enter N"))

        board = init_board(n)

        draw_board(board,SIZE,n)

	player = 1

	while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()


                        cpu_turn(board,player,n,depth,SIZE)

			pygame.time.wait(100)
	
			player = opp[player]


def main():
	screen.fill((0,0,0))
	ch = int (inputbox.ask(screen,"press 1 for cpu vs human and 2 for vs cpu"))

	if ch==1:
		run_human_vs_cpu()

	if ch==2:
		run_cpu_vs_cpu()

if __name__=="__main__":
	main()
