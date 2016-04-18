import socket, threading, pickle

#TODO sync player's movement
#TODO sync maps (random map on host and send it to clients)
#TODO for host: reroute client's info to other players
PORT = 9876  # the port number to run our server on


class Server(threading.Thread):
    def __init__(self, game, port=9876, host=socket.gethostname()):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.GAME = game
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []  # current connections
        self.lock = threading.Lock()
        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print('Bind failed {}'.format(socket.error))
            return
        print("Server initiated")
        self.server.listen(10)
        self.start()

    def close(self):
        self.server.close()

    def add_new_player(self, conn, addr):
        """this method is responsible for listening to commands for a specific player
        conn and addr are obtained by socket upon accepting new coonection and are passed here
        each command is a binary string which when decoded is as follows
        player_name (world_coords)
        """
        print('Client connected with ' + addr[0] + ':' + str(addr[1]))
        self.users.append(conn)
        # first, client should pass player name
        meta_data = pickle.loads(conn.recv(1024))
        self.GAME.add_new_player(meta_data ,conn)
        print(self.GAME.players)
        while True:
            # for now the data recieved should be name of player and new world coords
            try:
                data = pickle.loads(conn.recv(1024))
            except (EOFError, pickle.PickleError):
                pass
            else:
                self.GAME.players[data["name"]].world_coords = data["world_coords"]
                print(data["world_coords"])
            # print(data.decode())
            # reply = b'Copy that, ' + data
            # print(reply)
            # conn.sendall(reply)

        conn.close() # Close

    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        # We need to run a loop and create a new thread for each connection
        while True:
            conn, addr = self.server.accept()
            print("new connection accepted: {}".format(conn))
            threading.Thread(target=self.add_new_player, args=(conn, addr)).start()


class Client:

    def __init__(self, game, port=9876, host=socket.gethostname()):
        self.game = game
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_thread = threading.Thread(target=self.listen)
        self.connect()

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
        except socket.error:
            print("Could not find host game")
        else:
            self.send_message(pickle.dumps(self.game.player.get_meta_data()))
            self.listening_thread.start()
            print("Client connected")

    def send_message(self, bytes):
        """msg is a string that must be sent"""
        self.socket.send(bytes)

    def listen(self):
        while True:
            msg =  self.socket.recv(1024).decode()
            print("Got reply ",msg)

    def close(self):
        self.socket.close()
