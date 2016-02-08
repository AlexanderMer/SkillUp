print('Think of number between 0 and 100 not included. If my guess is bigger than your number, type \'>\' without quots, otherwise type \'<\' if it\'s smaller')
min, max = 0, 100
guess = int((min + max) / 2)
inp = input('Is it %s ?' % str(guess))
while inp != 'yes':
	if inp == '>':
		min = guess
	else:
		max = guess
	guess = int((min + max) / 2)
	inp = input('Is it %s ?' % str(guess))
print('I guessed it :)')
