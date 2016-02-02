pegs = [[], [], []]

def hanoi(height):
	pegs[0] = list(range(1, height + 1))
	print(*pegs)
	move(0, 2, height)


def move(from_peg, to_peg, n):
	if n > 1:
		temp = 3 - (from_peg + to_peg)
		move(from_peg, temp, n - 1 )
		move(from_peg, to_peg, 1)
		move(temp, to_peg, n - 1)
	else:
		pegs[to_peg].append(pegs[from_peg][-1])
		pegs[from_peg].pop()

hanoi(5)
print(*pegs)

