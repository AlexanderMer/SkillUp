import pickle


class Game:
    def __init__(self):
        self.attack_paths = {'rs': [1, 1, 1],
                            'cs': [1, 1, 1],
                            'd1': 1,
                            'd2': 1}
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
        self.mode = 'yes'
        self.leader_board = [('rob', 999),('rob', 999),('rob', 999),('rob', 999),('rob', 999),('rob', 999),
                             ('rob', 999),('rob', 999),('rob', 999),('rob', 999)]

    def get_input(self):
        """turn must be either O or X"""
        try:
            temp = int(input('Where to place {} '.format(self.turn)))
        except ValueError:
            print('please enter a number')
            self.get_input()
        else:
            if 1 <= temp <= 9:
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
        self.load_leader_board()
        self.print_leader_board()
        if input('new game or load? (n \ l)').startswith('l'):
            self.load_game()
            self.game_loop()
        else:
            self.mode = input('would you like to play with AI (forever alone)? Yes / No  ').lower()
            self.game_loop()

    def game_loop(self):
        while True:
            self.print_board()
            self.place_char()
            self.moves += 1
            if self.check_wins() == 'X':
                print('X wins!'.upper())
                break
            elif self.check_wins() == 'O':
                print('O wins!'.upper())
                break
            elif self.moves > 9:
                print('stalemate'.upper())
                break
            self.switch_turn()
            self.save_game()
        self.print_board()
        self.update_leader_board()
        self.print_leader_board()
       
    def place_char(self):
        # AI
        if self.mode == 'yes' and self.turn == 'O':
            # inspect board, since during the game there can be only 1 or 2 character in a row / column/diagonal
            # depending whether it's 1 or 2 the AI goes offence or defense

            # First check if AI can win with next move, if not, check if AI needs to defend
            # check rows
            enemy_count = 0
            empty_count = 0
            friendly_count = 0
            empty_tile = None
            
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == 'X':
                        enemy_count += 1
                    elif self.board[r][c] != 'O':
                        empty_tile = (r, c)
                    elif self.board[r][c] == 'O':
                        friendly_count += 1
                if enemy_count > 0:
                    self.attack_paths['rs'][r] = 0
                # attack
                if friendly_count == 2 and empty_tile is not None:
                    self.board[empty_tile[0]][empty_tile[1]] = self.turn
                    return
                # defend
                if enemy_count == 2 and empty_tile is not None:
                    self.board[empty_tile[0]][empty_tile[1]] = self.turn
                    return
                enemy_count = 0
                empty_tile = None
                friendly_count = 0
            # enemy_count = 0
            # empty_tile = None

            # check columns
            for c in range(3):
                for r in range(3):
                    if self.board[r][c] == 'X':
                        enemy_count += 1
                    elif self.board[r][c] != 'O':
                        empty_tile = (r, c)
                    elif self.board[r][c] == 'O':
                        friendly_count += 1
                if enemy_count > 0:
                    self.attack_paths['cs'][c] = 0
                # attack
                if friendly_count == 2 and empty_tile is not None:
                    self.board[empty_tile[0]][empty_tile[1]] = self.turn
                    return
                # defend
                if enemy_count == 2 and empty_tile is not None:
                    self.board[empty_tile[0]][empty_tile[1]] = self.turn
                    return
                enemy_count = 0
                empty_tile = None
                friendly_count = 0
            
            # enemy_count = 0
            # empty_tile = None

            # check diagonal 1
            for t in range(3):
                if self.board[t][t] == 'X':
                    enemy_count += 1
                elif self.board[t][t] != 'O':
                    empty_tile = (t, t)
                elif self.board[t][t] == 'O':
                    friendly_count += 1
            if enemy_count > 0:
                    self.attack_paths['d1'] = 0
            #attack
            if friendly_count == 2 and empty_tile is not None:
                self.board[empty_tile[0]][empty_tile[1]] = self.turn
                return
            #defend
            if enemy_count == 2 and empty_tile is not None:
                self.board[empty_tile[0]][empty_tile[1]] = self.turn
                return
            enemy_count = 0
            empty_tile = None
            friendly_count = 0

            # check diagonal 2
            for t in range(3):
                if self.board[t][2 - t] == 'X':
                    enemy_count += 1
                elif self.board[t][2 - t] != 'O':
                    empty_tile = (t, 2 - t)
                elif self.board[t][2 - t] == 'O':
                    friendly_count += 1
            if enemy_count > 0:
                self.attack_paths['d2'] = 0
            #attack
            if friendly_count == 2 and empty_tile is not None:
                self.board[empty_tile[0]][empty_tile[1]] = self.turn
                return
            #defend
            if enemy_count == 2 and empty_tile is not None:
                self.board[empty_tile[0]][empty_tile[1]] = self.turn
                return
            enemy_count = 0
            empty_tile = None
            friendly_count = 0

            # if AI can't win with one move AND neither can player, AI attacks
            # Get list of avaible attack paths and place 'O' in correct place
          # print(':))))))))') 
            rows = self.attack_paths['rs']
            for r in range(3):
                if rows[r]:
                  # print('Got here, ' + str(r))
                    for t in range(3):
                        if self.board[r][t] != 'O':
                          # print('Niice!')
                            self.board[r][t] = self.turn
                            return
            # check columns
            cols = self.attack_paths['cs']
            for c in range(3):
                if cols[c]:
                  # print('Got here, ' + str(r))
                    for t in range(3):
                        if self.board[t][c] != 'O':
                          # print('Niice!')
                            self.board[t][c] = self.turn
                            return
            # check diagonal 1
            if self.attack_paths['d1']:
                for t in range(3):
                    if self.board[t][t] != 'O':
                        self.board[t][t] = self.turn
                        return
            if self.attack_paths['d2']:
                for t in range(3):
                    if self.board[t][2 - t] != 'O':
                        self.board[t][2 - t] = self.turn
                        return

        # Human player
        else:
            self.get_input()
            tile = self.board[self.map[self.selection][0]][self.map[self.selection][1]]
            if tile != 'X' and tile != 'O':
                self.board[self.map[self.selection][0]][self.map[self.selection][1]] = self.turn
            else:
                print('You can\'t place it there')
                self.place_char()

    def save_game(self):
        pickle.dump((self.board, self.turn, self.moves, self.mode, self.attack_paths), open('TicTacToe_save.tctctoe', 'wb'))

    def load_game(self):
        try:
            self.board, self.turn, self.moves, self.mode, self.attack_paths = pickle.load(open('TicTacToe_save.tctctoe', 'rb'))
        except FileNotFoundError:
            print('save game not found, starting new game')
        except:
            print('something went wrong, starting new game')

    def update_leader_board(self):
        name = input('what\'s your name ? ')
        for i in range(10):
            if self.leader_board[i][1] > self.moves:
                self.leader_board[i] = (name, self.moves)
                break
        pickle.dump(self.leader_board, open('leader_board.tctctoe', 'wb'))

    def load_leader_board(self):
        try:
            self.leader_board = pickle.load(open('leader_board.tctctoe', 'rb'))
        except Exception as e:
            print(e.args)

    def print_leader_board(self):
        for l in self.leader_board:
            print(*l)
g = Game()
g.start()
