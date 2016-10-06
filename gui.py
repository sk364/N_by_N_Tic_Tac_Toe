import pygame
from pygame.locals import *

SIZE = 450
screen = pygame.display.set_mode((SIZE,SIZE),0,32)

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

