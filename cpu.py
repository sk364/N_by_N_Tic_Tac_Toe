import copy
from gui_basic import win

opp = [1,0]

def eval_rows(board,player,n):
	score_sum = 0
	for i in range(n):
		score = 0
		if board[i][0] == player:
			score = 1
		elif board[i][0] == opp[player]:
			score = -1
		for j in range(1,n):
			if board[i][j] == player:
				if score>0:
					score = score*10
				elif score<0:
					score = 0
					break
				else:
					score=1
			elif board[i][j]==opp[player]:
				if score<0:
					score = score*10
                                elif score>0:
                                        score = 0
                                        break
                                else:
                                        score=1
		score_sum = score_sum+score

	return score_sum


def eval_cols(board,player,n):
	score_sum = 0
        for j in range(n):
                score = 0
                if board[0][j] == player:
                        score = 1
                elif board[0][j] == opp[player]:
                        score = -1
                for i in range(1,n):
                        if board[i][j] == player:
                                if score>0:
                                        score = score*10
                                elif score<0:
                                        score = 0
                                        break
                                else:
                                        score=1
                        elif board[i][j]==opp[player]:
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
	score = eval_rows(board,player,n)
	score += eval_cols(board,player,n)
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


def minimax(board, player, depth, n):
	moves = get_moves(board, n)

	if not moves:
		return None

	best_move = moves[0]
	best_score = 0

	for move in moves:
		clone_board=gen_board(board,opp[player],move)
		#print clone_board
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

	if not moves or depth==0 or win(board,player,n) or win(board,opp[player],n):	evaluate(board,player,n)
	
	best_score = float('inf')

	for move in moves:
		clone_board = gen_board(board,player,move)
		score = max_play(clone_board,opp[player],depth-1, n)

		if score < best_score:
			best_score = score

	return best_score

def max_play(board, player, depth, n):
        moves = get_moves(board,n)

        if not moves or depth==0 or win(board,player,n) or win(board,opp[player],n):       evaluate(board,player,n)

        best_score = float('-inf')

        for move in moves:
		clone_board = gen_board(board,player,move)
                score = max_play(clone_board,opp[player],depth-1, n)

                if score > best_score:
                        best_score = score

        return best_score

