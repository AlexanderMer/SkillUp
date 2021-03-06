import socket, threading, pickle, logging, sys
from multiprocessing.connection import Listener, Client

# The client shoud send data about one self and  recieve data about everyone else
# The server must get everyone's data, process it and send it back

#TODO sync player's movement e.g. when one player's screen scrolls he moves faster
#TODO implement connection termination mechanism in the even of disconnecting
#TODO fix bug where game gets stuck on closing window
PORT = 9876  # the port number to run our server on
# Commands constants
NEW_PLAYER = 1  # Meta data
PLAYERS_STATES = 2  # Players position each player's meta_data
PLAYER_QUIT = 3  # player's name
KEYS_PRESSED = 4  # tuple (name, keys)
FIRE_PROJECTILE = 5

class Message():
    def __init__(self, type, message):
        # If type is NEW_PLAYER message must be pickled meta_data about new player
        self.message_type = type
        self.message = message
        # logging.info("Created message of type {}".format(type))

    def __str__(self):
        return "type: {}, message {}".format(self.message_type, self.message)

class GameServer(threading.Thread):
    def __init__(self, game, port=9876, host=socket.gethostname()):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.game = game
        self.socket = Listener((host, port))
        self.users = []  # current connections
        self.lock = threading.Lock()
        """try:
            self.socket.bind((self.host, self.port))
        except socket.error:
            logging.error('Bind failed {}'.format(socket.error))
            sys.exit(-1)"""
        print("Server initiated")
        #self.socket.listen(10)
        self.start()

    def add_new_player(self, conn):
        """this method is responsible for listening to commands for a specific player
        conn and addr are obtained by socket upon accepting new coonection and are passed here
        each command is a binary string which when decoded is as follows
        player_name (world_coords)
        """
        logging.info('Client connected with {}'.format(str(conn)))
        raw_message = conn.recv()  # first, client should pass player meta data
        meta_data = raw_message.message
        logging.info("meta data received {}".format(meta_data))
    # Send info about game state to new player
        conn.send(Message(type=NEW_PLAYER, message=self.game.player.get_meta_data()))
        for player in self.game.players:
            conn.send(Message(type=NEW_PLAYER, message=self.game.players[player].get_meta_data()))
        self.game.add_new_player(meta_data)
        logging.info("players currently connected: {}".format(self.game.players))
    # Inform other players about new connection
        for user in self.users:
            user.send(raw_message)
            print("sending new player signal to user: {}".format(user))
        self.users.append(conn)  # Append new player AFTER rerouting meta data to players
    # Main event listening loop
        while True:
            # for now the data recieved should be name of player and new world coords
            msg = conn.recv()
            if msg.message_type == KEYS_PRESSED:
                with self.lock:
                    for key in msg.message[1]:
                        self.game.players[msg.message[0]].press_key(key)
            elif msg.message_type == PLAYERS_STATES:
                logging.info("SERVER PLAYER STATES RECEIVED!!!!!")
                #self.game.players[msg.message["name"]].world_coords = msg.message["world_coords"]
            elif msg.message_type == FIRE_PROJECTILE:
                logging.info("Recieved FIRE command")
                self.game.players[msg.message[0]].fire_projectile(msg.message[1])
                self.send_to_all(msg, except_user=conn)
            elif msg.message_type == PLAYER_QUIT:
                self.send_to_all(msg, except_user=conn)
                if msg.message in self.game.players.keys():
                    self.game.players[msg.message].kill()
                    del self.game.players[msg.message]
                    #conn.close()

        conn.close() # Close

    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        # We need to run a loop and create a new thread for each connection
        while True:
            try:
                conn = self.socket.accept()
            except OSError as e:
                logging.error("Player disconnected: {}".format(e))
            else:
                logging.info("new connection accepted: {}".format(conn))
                threading.Thread(target=self.add_new_player, args=(conn,)).start()

    def send_to_all(self, msg, except_user=0):
        if except_user:
            users = self.users[:]
            if except_user in users:
                print("User removed")
                users.remove(except_user)
        else:
            users = self.users[:]
        for user in users:
            try:
                user.send(msg)
            except socket.error:
                logging.error("Could not send data to {}".format(user))
            else:
                #logging.info("Data sent successfully to {}".format(user))
                pass

    def close(self):
        self.socket.close()

class GameClient:

    def __init__(self, game, port=9876, host=socket.gethostname()):
        self.game = game
        host = '192.168.0.101'
        self.host = host
        self.port = port
        try:
            self.socket = Client((host, port))
        except ConnectionRefusedError:
            logging.error("Could not connect to host")
            return
        else:
            self.listening_thread = threading.Thread(target=self.listen)
            self.listening_thread.start()
            #self.connect()

    def connect(self):
        self.send_message(Message(NEW_PLAYER, self.game.player.get_meta_data()))
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
                msg = self.socket.recv()
            except:
                logging.error("Error while decoding message")
            else:
                #logging.info("Got reply {}".format(msg))
                if msg.message_type == PLAYERS_STATES:
                    # list of dicks with meta_data
                    for player in msg.message:
                        # temp workaround, should avoid IFs in the future
                        if player["name"] == self.game.player.name:
                            self.game.player.world_coords = player["world_coords"]
                            self.game.player.health = player["health"]
                        else:
                            # TODO implement better protocol, one that doesn't require comparison
                           #if player['name'] in self.game.players:
                            try:
                                self.game.players[player["name"]].world_coords = player["world_coords"]
                            except KeyError as e:
                                logging.error("Error assigning world_coords. Player with name {} not found".format(player['name']))
                elif msg.message_type == FIRE_PROJECTILE:
                    name = msg.message[0]
                    if name == self.game.player.name:
                        self.game.player.fire_projectile(msg.message[1])
                    else:
                        self.game.players[name].fire_projectile(msg.message[1])
                elif msg.message_type == NEW_PLAYER:
                    logging.info("New player Message received")
                    self.game.add_new_player(msg.message)
                elif msg.message_type == PLAYER_QUIT:
                    if msg.message in self.game.players.keys():
                        self.game.players[msg.message].kill()
                        del self.game.players[msg.message]

    def add_new_player(self, meta):
        print("Client new player is called")
        self.game.add_new_player(meta)

    def close(self):
        self.send_message(Message(type=PLAYER_QUIT, message=self.game.player.name))
        self.socket.close()
