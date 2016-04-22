import socket, threading, pickle, logging

# The client shoud send data about one self and  recieve data about everyone else
# The server must get everyone's data, process it and send it back

#TODO sync player's movement e.g. when one player's screen scrolls he moves faster
#TODO sync maps (random map on host and send it to clients)
#TODO for host: reroute client's info to other players
#TODO implement connection termination mechanism in the even of disconnecting
#TODO fix bug where game gets stuck on closing window
PORT = 9876  # the port number to run our server on
# Commands constants
NEW_PLAYER = 1  # Meta data
GAME_STATE = 2  # Player position Meta_data
PLAYER_QUIT = 3  # optional args
KEYS_PRESSED = 4  # tuple (name, keys)

class Message():
    def __init__(self, type, message):
        # If type is NEW_PLAYER message must be pickled meta_data about new player
        self.message_type = type
        self.message = message
        # logging.info("Created message of type {}".format(type))

    def __str__(self):
        return "type: {}, message {}".format(self.message_type, self.message)

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
        raw_message = conn.recv(4096)  # first, client should pass player meta data
        meta_data = pickle.loads(raw_message).message
        logging.info("meta data received {}".format(meta_data))
        self.GAME.add_new_player(meta_data)
        logging.info("players currently connected: {}".format(self.GAME.players))
        # Inform other players about new connection
        for user in self.users:
            user.sendall(raw_message)
            print("sending new player signal to user: {}".format(user))
        self.users.append(conn)  # Append new player AFTER rerouting meta data to players
        while True:
            # for now the data recieved should be name of player and new world coords
            try:
                msg = pickle.loads(conn.recv(4096))
            except pickle.PickleError:
                logging.warning("Received data could not be decoded")
            except socket.error:
                logging.warning("Error getting data from client")
            else:
                if msg.message_type == KEYS_PRESSED:
                    for key in msg.message[1]:
                        self.GAME.players[msg.message[0]].press_key(key)
                elif msg.message_type == GAME_STATE:
                    self.GAME.players[msg.message["name"]].world_coords = msg.message["world_coords"]
        conn.close() # Close

    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        # We need to run a loop and create a new thread for each connection
        while True:
            conn, addr = self.socket.accept()
            logging.info("new connection accepted: {}".format(conn))
            threading.Thread(target=self.add_new_player, args=(conn, addr)).start()

    def send_to_all(self, bytes):
        for user in self.users:
            try:
                user.sendall(bytes)
            except socket.error:
                logging.error("Could not send data to {}".format(user))
            else:
                #logging.info("Data sent successfully to {}".format(user))
                pass

class Client:

    def __init__(self, game, port=9876, host=socket.gethostname()):
        self.game = game
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_thread = threading.Thread(target=self.listen)
        try:
            self.socket.connect((self.host, self.port))
        except socket.error:
            pass
            # logging.error("Could not find host game")
        else:
            self.listening_thread.start()
        self.connect()

    def connect(self):
        self.send_message(pickle.dumps(Message(NEW_PLAYER, self.game.player.get_meta_data())))
        logging.info("Client connected")

    def send_message(self, bytes):
        """msg is a string that must be sent"""
        try:
            self.socket.send(bytes)
        except socket.error:
            pass
            # logging.warning("could not connect to host")

    def listen(self):
        while True:
            try:
                msg = pickle.loads(self.socket.recv(4096))
                print("GOT NEW MESSAGE!  {}".format(msg))
                # logging.info("Got reply {}".format(msg))
            except socket.error:
                logging.error("Something happened in client while listening")
            except pickle.PickleError:
                logging.error("Could not deserialize received Message")
            else:
                if msg.message_type == GAME_STATE:
                    pass
                elif msg.message_type == NEW_PLAYER:
                    self.game.add_new_player(msg.message)

    def add_new_player(self, meta):
        print("Client new player is called")
        self.game.add_new_player(meta)

    def close(self):
        if self.listening_thread.is_alive():
            self.listening_thread.join()
        self.socket.close()
