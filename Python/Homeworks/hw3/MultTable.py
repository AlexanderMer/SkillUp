#variant a
'''
for i in range(10):
    for j in range(10):
        res = str((i + 1) * (j + 1))
        p = res if len(res) > 1 else res + ' '
        print(p + ' ', end = '')
    print()
'''

#variant b

limit = 100000
maxSpaces = limit ** 2
for i in range(limit):
    for j in range(limit):
        res = str((i + 1) * (j + 1))
        p = res + (len(str(maxSpaces)) - len(res)) * ' '
        print(p + ' ', end = '')
    print()
