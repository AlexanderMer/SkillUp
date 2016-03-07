import random
from tkinter import *


class Card:
    def __init__(self, name):
        self.name = name


class Deck:
    def __init__(self):
        ranks = '23456789TJQKA'
        suits = 'HCDS'
        self.cards = [Card(r + s) for r in ranks for s in suits]
        random.shuffle(self.cards)

class Game:
    cards=[]
    texts=[]
    card_size = 100, 160

    def __init__(self):
        self.players = [[[], 0, 'Alexander'], [[], 0, 'Dealer']]
        self.turn = False
        global main_window
        self.deck = Deck()
        self.money = 1000
        main_window= Tk()
        self.game_board = Canvas(main_window, width=800, height=600, bg="green")
        self.btn_new = Button(main_window,text="New Game", font="Arial 15", command=self.new_game)
        colors = self.random_color()
        self.btn_hit = Button(main_window, text="   Hit   ", font="Arial 15", bg=colors[0], fg=colors[1], command=self.hit)
        self.btn_hit.grid(row=2, column=1)
        self.btn_hit.config(state="disabled")
        self.btn_done = Button(main_window, text="   Done   ", font="Arial 15", bg=colors[0], fg=colors[1], command=self.done)
        self.btn_done.grid(row=3, column=1)
        self.btn_done.config(state="disabled")
        self.game_board.grid(rowspan=15, row=0, column=0)
        self.player_score_text = self.game_board.create_text(100, 600 - self.card_size[1] - 70, text="0", font="Arial 20")
        self.btn_new.grid(row=1, column=1)
        self.lbl_money = Label(text=str(self.money) + " $", font="Arial 20")
        self.lbl_money.grid(row=0, column = 1)
        self.card_player_pointer_x = 20 # offset in pixels to draw cards
        self.card_dealer_pointer_x = 20
        self.dealer_score_text = self.game_board.create_text(100, 60 + self.card_size[1], text="0", font="Arial 20")
        self.win_text = self.game_board.create_text(300, 300, text="", font="Arial 20")

        main_window.mainloop()  # Must be in the end

    def random_color(self, seed=None):
        random.seed(seed)
        ct = [random.randrange(256) for x in range(3)]
        brightness = int(round(0.299 * ct[0] + 0.587 * ct[1] + 0.114 * ct[2]))
        ct_hex = "%02x%02x%02x" % tuple(ct)
        bg_color = '#' + "".join(ct_hex)
        fg_color = "white" if brightness < 120 else "black"
        random.seed(None)
        return bg_color, fg_color

    def new_game(self):
        self.game_board.itemconfig(self.win_text, text="")
        self.btn_done.config(self.btn_done, state="active")
        self.btn_hit.config(state="active")
        self.game_board.itemconfig(self.player_score_text, text="0")
        self.card_player_pointer_x = 20
        self.card_dealer_pointer_x = 20
        self.deck = Deck();
        self.erase_cards()
        self.players[0][0] = []
        self.players[1][0] = []
        self.players[0][0].append(self.deck.cards.pop())
        self.players[0][0].append(self.deck.cards.pop())
        self.players[1][0].append(self.deck.cards.pop())
        self.players[1][0].append(self.deck.cards.pop())
        for c in self.players[0][0]:
            self.draw_card(c, self.card_player_pointer_x, 400)
            self.card_player_pointer_x += self.card_size[0] + 20
        for c in self.players[1][0]:
            self.draw_card(c, self.card_dealer_pointer_x, 30)
            self.card_dealer_pointer_x += self.card_size[0] + 20
        self.start_game()

    def draw_card(self, card, x, y):
        print("got here card: {}  x {}  y {}".format(card.name, x, y))
        self.cards.append(self.game_board.create_rectangle(x, y, x+self.card_size[0], y+self.card_size[1], fill="white"))
        self.texts.append(self.game_board.create_text(int(x+self.card_size[0] / 2), int(y+self.card_size[1] / 2),
                                     text=card.name, font="Arial {}".format(int(self.card_size[1] / 10))))

    def erase_cards(self):
        for card in self.cards:
            self.game_board.delete(card)
        for t in self.texts:
            self.game_board.delete(t)

    def update_score(self, p):
        self.players[p][1] = 0
        for c in self.players[p][0]:
            if c.name[0] in 'TJQK':
                self.players[p][1] += 10
            elif c.name[0] == 'A':
                if len(self.players[p][0]) == 1:
                    self.players[p][1] += 1
                else:
                    self.players[p][1] += 11
            else:
                self.players[p][1] += int(c.name[0])
        self.game_board.itemconfig(self.player_score_text, text=self.players[0][1])
        self.game_board.itemconfig(self.dealer_score_text, text=self.players[1][1])

    def check_wins(self, final = False):
        if not final:
            if self.players[int(self.turn)][1] == 21:
                self.game_board.itemconfig(self.win_text, text=self.players[int(self.turn)][2] + ' wins')
                self.game_over(1)
                return 1
            elif self.players[int(self.turn)][1] > 21:
                self.game_board.itemconfig(self.win_text, text=self.players[int(self.turn)][2] + ' busts')
                self.game_over(0)
                return 0
            return 0
        else:
            if self.players[0][1] == self.players[1][1]:
                self.game_board.itemconfig(self.win_text, text='Dealer wins ')
                self.game_over(0)
                return 1
            elif self.players[0][1] > self.players[1][1]:
                self.game_board.itemconfig(self.win_text, text='{} wins '.format(self.players[0][2]))
                self.game_over(1)
                return 1
            else:
                self.game_board.itemconfig(self.win_text, text='{} wins '.format(self.players[1][2]))
                self.game_over(0)
                return 1

    def hit(self, t=0):
        self.players[t][0].append(self.deck.cards.pop())
        if t == 0:
            self.draw_card(self.players[t][0][-1], self.card_player_pointer_x, 400)
            self.card_player_pointer_x += self.card_size[0] + 20
        else:
            self.draw_card(self.players[t][0][-1], self.card_player_pointer_x, 30)
            self.card_dealer_pointer_x += self.card_size[0] + 20
        print('{} cards: '.format(self.players[t][2])) # name
        print(*self.players[t][0]) # cards
        self.update_score(t)
        print('{} score {}'.format(self.players[t][2], self.players[t][1])) # name and score
        if self.players[t][1] > 21:
            self.game_board.itemconfig(self.win_text, text='{} busts '.format(self.players[t][2]))
            self.game_over(0)
            return 1
        return self.check_wins()

    def start_game(self):
        self.game_board.itemconfig(self.player_score_text, text="0")
        self.game_board.itemconfig(self.win_text, text="")
        self.game_board.itemconfig(self.btn_done, state="active")
        self.btn_hit.config(state="active")
        self.turn = False
        self.update_score(0)
        self.update_score(1)
        # update_score(1)
        if self.check_wins():
            self.game_over(1)
        #  print('{} score: {}'.format(players[turn][2], players[int(turn)][1]))
        hit = True
        """while input('hit? (yes / no) ') == 'yes':
            if hit(0):
                print('game over')
                self.game_over()"""

    def game_over(self, win):
        self.btn_hit.config(state="disabled")
        self.btn_done.config(state="disabled")
        if win:
            self.update_money(win)
        else:
            self.update_money(win)

    def update_money(self, win):
        if win:
            self.money += 200
        else:
            self.money -= 200
        self.lbl_money.config(text=str(self.money))

    def done(self):
        self.btn_hit.config(state="disabled")
        self.update_score(1)
        self.turn = True
        while self.players[1][1] < 17:
            if self.hit(1):
                self.game_over(False)
        self.check_wins(final = True)

Game()