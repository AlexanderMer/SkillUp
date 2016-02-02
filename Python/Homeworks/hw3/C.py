for row in range(1, 10):
    print(' ' * (10 - row), end = '')
    print(*(range(1, row)), end = '', sep = '')
    print(*range(row, 0, -1), sep = '')