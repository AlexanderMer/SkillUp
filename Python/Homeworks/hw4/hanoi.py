pegs = [[], [], []]
moves = 0

def hanoi(height):
	pegs[0] = list(range(1, height + 1))
	print(*pegs)
	move_discs(0, 2, height)
	print(*pegs)
	print('completed in %s moves' % str(moves))

def move_discs(from_peg, to_peg, n):
	global moves
	if n > 1:
		temp = 3 - (from_peg + to_peg)
		move_discs(from_peg, temp, n - 1 )
		move_discs(from_peg, to_peg, 1)
		move_discs(temp, to_peg, n - 1)
	else:
		pegs[to_peg].append(pegs[from_peg][-1])
		pegs[from_peg].pop()
		moves += 1

hanoi(15)