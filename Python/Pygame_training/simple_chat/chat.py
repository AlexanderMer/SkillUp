#!/usr/bin/python3
import socket, sys, threading

# Simple chat client that allows multiple connections via threads

PORT = 9871# the port number to run our server on

__version__ = "0.0.1"

class ChatServer(threading.Thread):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print('Bind failed %s' % (socket.error))
            sys.exit()
        self.server.listen(10)

    # Not currently used. Ensure sockets are closed on disconnect
    def exit(self):
        self.server.close()

    def run_thread(self, conn, addr):
        print('Client connected with ' + addr[0] + ':' + str(addr[1]))
        self.users.append(conn)
        print("new connection accepted: {}".format(conn))
        while True:
            data = conn.recv(1024)
            print(data.decode())
            reply = b'Copy that, ' + data
            print(reply)
            conn.sendall(reply)

        conn.close() # Close

    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        # We need to run a loop and create a new thread for each connection
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.run_thread, args=(conn, addr)).start()

class ChatClient:

    def __init__(self, port, host='localhost'):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, port))

    def send_message(self, msg):
        #while True:
         self.socket.send(msg.encode())

if __name__ == '__main__':
    server = ChatServer(PORT)
    server.start()
