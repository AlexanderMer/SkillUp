import random as rand

'''Ace = 11 when alone, 1 otherwise
   Jack, Queen, King = 10
'''

ranks = '23456789TJQKA'
suits = 'HCDS'
deck = [r + s for r in ranks for s in suits]
rand.shuffle(deck)

players = [[[], 0, 'Alexander'], [[], 0, 'Dealer']]
turn = False # indicates turn of players, rework into integer if more than 2 players

def update_score(p):
    players[p][1] = 0
    for c in players[p][0]:
        if c[0] in 'TJQK':
            players[p][1] += 10
        elif c[0] == 'A':
            if len(players[p][0]) == 1:
                players[p][1] += 1
            else:
                players[p][1] += 11
        else:
            players[p][1] += int(c[0])


def check_wins(final = False):
    if not final:
        if players[int(turn)][1] == 21:
            print(players[int(turn)][2] + ' wins')
            return 1
        elif players[int(turn)][1] > 21:
            print(players[int(turn)][2] + ' busts')
            return 1
        return 0
    else:
        if players[0][1] == players[1][1]:
            print('Dealer wins ')
            return 1
        elif players[0][1] > players[1][1]:
            print('{} wins '.format(players[0][2]))
            return 1
        else:
            print('{} wins '.format(players[1][2]))
            return 1

def hit(t):
    players[t][0].append(deck.pop())
    print('{} cards: '.format(players[t][2])) # name
    print(*players[t][0]) # cards
    update_score(t)
    print('{} score {}'.format(players[t][2], players[t][1])) # name and score 
    if players[t][1] > 21:
        print('{} busts '.format(players[t][2]))
        return 1
    return check_wins()
    


players[0][0].append(deck.pop())
players[0][0].append(deck.pop())
players[1][0].append(deck.pop())
players[1][0].append(deck.pop())
def game():
    turn = False
    print('{} cards: '.format(players[0][2])) # name
    print(*players[int(turn)][0]) # cards
    print('Dealer cards: ')
    print('## ' + players[1][0][1]) # cards
    update_score(0)
    # update_score(1)
    print()
    if check_wins():
        return
    print('{} score: {}'.format(players[turn][2], players[int(turn)][1]))
    while input('hit? (yes / no) ') == 'yes':
        if hit(0):
            print('game over')
            return
    update_score(1)
    turn = True
    while players[1][1] < 17:
        if hit(1):
            return
    check_wins(final = True)
game()