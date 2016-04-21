import socket, threading, pickle, logging

# The client shoud send data about one self and  recieve data about everyone else
# The server must get everyone's data, process it and send it back

#TODO sync player's movement e.g. when one player's screen scrolls he moves faster
#TODO sync maps (random map on host and send it to clients)
#TODO for host: reroute client's info to other players
#TODO impleent connection termination mechanism in the even of disconnecting
#TODO fix bug where game gets stuck on closing window
PORT = 9876  # the port number to run our server on


class Server(threading.Thread):
    def __init__(self, game, port=9876, host=socket.gethostname()):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.GAME = game
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []  # current connections
        self.lock = threading.Lock()
        try:
            self.socket.bind((self.host, self.port))
        except socket.error:
            print('Bind failed {}'.format(socket.error))
            return
        print("Server initiated")
        self.socket.listen(10)
        self.start()

    def close(self):
        self.socket.close()

    def add_new_player(self, conn, addr):
        """this method is responsible for listening to commands for a specific player
        conn and addr are obtained by socket upon accepting new coonection and are passed here
        each command is a binary string which when decoded is as follows
        player_name (world_coords)
        """
        logging.info('Client connected with ' + addr[0] + ':' + str(addr[1]))
        self.users.append(conn)
        # first, client should pass player meta data
        meta_data = pickle.loads(conn.recv(1024))
        logging.info("meta data received {}".format(meta_data))
        self.GAME.add_new_player(meta_data ,conn)
        logging.info("players currently connected: {}".format(self.GAME.players))
        # Send level to newly connected client
        #conn.sendall(pickle.dumps(self.GAME.level.LEVEL))
        #logging.info("Sending level to new client {}".format(addr))
        while True:
            # for now the data recieved should be name of player and new world coords
            try:
                data = pickle.loads(conn.recv(1024))
            except pickle.PickleError:
                logging.warning("Received data could not be decoded")
            except socket.error:
                logging.warning("Error getting data from client")
            else:
                self.GAME.players[data["name"]].world_coords = data["world_coords"]
        conn.close() # Close

    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        # We need to run a loop and create a new thread for each connection
        while True:
            conn, addr = self.socket.accept()
            logging.info("new connection accepted: {}".format(conn))
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
            logging.error("Could not find host game")
        else:
            self.send_message(pickle.dumps(self.game.player.get_meta_data()))
            self.listening_thread.start()
            logging.info("Client connected")

    def send_message(self, bytes):
        """msg is a string that must be sent"""
        try:
            self.socket.send(bytes)
        except socket.error:
            logging.warning("could not connect to host")

    def listen(self):
        #try:
        #except pickle.PickleError:
        #    logging.error("Could not decode recieved level")
        #else:
        #    self.game.level.LEVEL = level
        #    logging.info("Received host level")
        while True:
            try:
                msg =  self.socket.recv(1024).decode()
                print("Got reply ",msg)
            except socket.error:
                logging.error("Something happened in client while listening")

    def close(self):
        if self.listening_thread.is_alive():
            self.listening_thread.join()
        self.socket.close()

