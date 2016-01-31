for row in range(9):
    for n in range(10 - row + 1):
        print(' ', end = '')
    for n in range(row):
        print(n + 1, end = '')
    for n in range(row + 1, 0, -1):
        print(n, end ='')
    print()
