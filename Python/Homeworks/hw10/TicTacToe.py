class Game:
    def __init__(self):
        self.board = [[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]]
        self.map = {1: (0, 0),
                    2: (0, 1),
                    3: (0, 2),
                    4: (1, 0),
                    5: (1, 1),
                    6: (1, 2),
                    7: (2, 0),
                    8: (2, 1),
                    9: (2, 2)}
        self.turn = 'X'
        self.moves = 0
        self.selection = 0

    def get_input(self):
        '''turn must be either O or X'''
        temp = 0
        try:
            temp = int(input('Where to place {} '.format(self.turn)))
        except:
            print('please enter a number')
            self.get_input()
        else:
            #if 1 <= temp <= 9:
            if temp >= 1 and temp <= 9:
                print(temp)
                self.selection = temp
            else:
                print('Please enter number between 1 and 9')
                self.get_input()
            

    def print_board(self):
        print('------------')
        for a in self.board:
            print('|', end = '')
            print(*a, sep = '|')
            print('-------------')

    def switch_turn(self):
        self.turn = 'X' if self.turn == 'O' else 'O'

    def check_wins(self):
        '''Returns char of winner if any, otherwise returns \'N\''''
        # Checking horizontal lines
        for l in range(3):
            if self.board[l][0] == self.board[l][1] == self.board[l][2]:
                return self.board[l][0]
        # Checking columns
        for c in range(3):
            if self.board[0][c] == self.board[1][c] == self.board[2][c]:
                return self.board[1][c]
        #Checking diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]

    def start(self):
        self.game_loop()

    def game_loop(self):
        while True:
            self.print_board()
            self.place_char()
            if self.check_wins() == 'X':
                print('X wins!')
                break
            elif self.check_wins() == 'O':
                print('O wins!')
                break
            elif self.moves > 9:
                print('stalemate')
                break
            self.switch_turn()
        self.print_board()
       
    def place_char(self):
        self.get_input()
        player = self.selection
        print('player ' + str(player))
        tile = self.board[self.map[player][0]][self.map[player][1]]
        if tile != 'X' and tile != 'O':
            self.board[self.map[player][0]][self.map[player][1]] = self.turn
            self.moves += 1
        else:
            print('You can\'t place it there')
            self.place_char()



g = Game()
g.start()
