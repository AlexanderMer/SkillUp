#list generaors:
#this generates a deck of cards by crossing r and s using following expression
ranks = '23456789TJQKA'
suits = 'HCDS'
deck = [r + s for r in ranks for s in suits]
print(*deck)