num = int(input('number? '))

if num > 10:
    print('your number is more than 10')
elif num < 10:
    print('your number is less than 10')
else:
    print('It\'s 10!!')


#with dictionary we can simulate switch case  
dic = {2 : 'it\'s two!', 5 : 'it\'s five!', 551548784845313212151 : 'go away'}
print(dic.get(num))