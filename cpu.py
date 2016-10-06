import copy
from common import *

opp = [1,0]

def eval_rc(board,player,n, roc):
	score_sum = 0

	clone_board = board

	if roc=="c":
		clone_board = [[ board[j][i] for j in xrange(n)] for i in xrange(n)]

	for i in xrange(n):
		score = 0
		if clone_board[i][0] == player:
			score = 1
		elif clone_board[i][0] == opp[player]:
			score = -1
		for j in xrange(1,n):
			if clone_board[i][j] == player:
				if score>0:
					score = score*10
				elif score<0:
					score = 0
					break
				else:
					score=1
			elif clone_board[i][j]==opp[player]:
				if score<0:
					score = score*10
                                elif score>0:
                                        score = 0
                                        break
                                else:
                                        score=1
		score_sum = score_sum+score

	return score_sum

def eval_diags(board,player,n):
	score = 0
	if board[0][0] == player:
		score = 1
	elif board[0][0]==opp[player]:
		score = -1
	for i in range(1,n):
		if board[i][i]==player:
			if score>0:
				score=score*10
			elif score<0:
				score = 0
				break
			else:
				score = 1
		elif board[i][i]==opp[player]:
			if score<0:
                                score=score*10
                        elif score>0:
                                score = 0
                                break
                        else:
                                score = 1

	score_sum = score

	score = 0
        if board[n-1][0] == player:
                score = 1
        elif board[n-1][0]==opp[player]:
                score = -1
        for i in range(1,n):
                if board[n-i-1][i]==player:
                        if score>0:
                                score=score*10
                        elif score<0:
                                score = 0
                                break
                        else:
                                score = 1
                elif board[n-i-1][i]==opp[player]:
                        if score<0:
                                score=score*10
                        elif score>0:
                                score = 0
                                break
                        else:
                                score = 1


	score_sum = score_sum+score

	return score_sum

def evaluate(board,player,n):
	score = eval_rc(board,player,n, "r")
	score += eval_rc(board,player,n, "c")
	score += eval_diags(board,player,n)

	return score


def get_moves(board, n):
	moves = []
	for i in range(n):
		for j in range(n):
			if board[i][j]==-1:	
				moves = moves + [[i,j]]
	return moves

def gen_board(board,player, m):
	new_board = copy.deepcopy(board)
	new_board[m[0]][m[1]] = player
	return new_board

def if_second_move(board,n):
	c = 0
	for i in xrange(n):
		for j in xrange(n):
			if board[i][j]==0 or board[i][j]==1:
				c += 1
			if c>1:
				return 0
	return 1

def minimax(board, player, depth, n):
	moves = get_moves(board, n)

	if not moves:
		return None

	if len(moves) == 1 or if_second_move(board,n):
		return moves[0]

	best_move = moves[0]
	best_score = 0

	for move in moves:
                clone_board=gen_board(board,player,move)
                if win(clone_board,player,n):
                        return move

	for move in moves:
		clone_board=gen_board(board,opp[player],move)
		if win(clone_board,opp[player],n):
			return move

	for move in moves:
		clone_board=gen_board(board,player,move)
                
		if win(clone_board,player,n):
                        return move

		score = min_play(clone_board,opp[player],depth,n)

		if best_score < score:
			best_score = score
			best_move = move

	return best_move


def min_play(board, player, depth, n):
	moves = get_moves(board,n)

	if not moves or depth==0:	
		return evaluate(board,player,n)
	
	best_score = float('inf')

	for move in moves:
		clone_board = gen_board(board,player,move)

		if win(clone_board,player,n):
                        return evaluate(clone_board,player,n)

		score = max_play(clone_board,opp[player],depth-1, n)

		if score < best_score:
			best_score = score

	return best_score

def max_play(board, player, depth, n):
        moves = get_moves(board,n)

        if not moves or depth==0:       
		return evaluate(board,player,n)

        best_score = float('-inf')

        for move in moves:
		clone_board = gen_board(board,player,move)

		if win(clone_board,player,n):
                        return evaluate(clone_board,player,n)

                score = max_play(clone_board,opp[player],depth-1, n)

                if score > best_score:
                        best_score = score

        return best_score

