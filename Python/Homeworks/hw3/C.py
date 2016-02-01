for row in range(9):
    print(' ' * (10 - row + 1), end = '')
    print(*(range(1, row + 1)), end = '', sep = '')
    print(*range(row + 1, 0, -1), sep = '')