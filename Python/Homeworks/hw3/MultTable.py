for i in range(10):
    for j in range(10):
        res = str((i + 1) * (j + 1))
        p = res if len(res) > 1 else res + ' '
        print(p + ' ', end = '')
    print()
