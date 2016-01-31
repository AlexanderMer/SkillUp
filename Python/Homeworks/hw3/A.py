num = int(input ("height of your glorious pyramid? "))

for n in range(num + 1):
    print(' ' * (num - n) , end = '')
    print('*' * n, end = ' ')
    print('*' * n, end = '')
    print()
print()
print()
for n in range(num):
    print(' ' * n , end = '')
    print('*' * (num - n), end = ' ')
    print('*' * (num - n), end = '')
    print()
    
    
