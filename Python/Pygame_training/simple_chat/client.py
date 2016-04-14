import socket


PORT = 9871  # the port number to run our server on

class ChatClient:

    def __init__(self, port, host='localhost'):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, port))

    def send_message(self):
        while True:
            msg = input("Message? ")
            if msg == "quit":
                break
            else:
                self.socket.send(msg.encode())

if __name__ == '__main__':
    client = ChatClient(PORT)
    client.send_message()