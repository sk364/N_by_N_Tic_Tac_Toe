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
