import socket, threading


PORT = 9871  # the port number to run our server on


class ChatClient:
    def __init__(self, port, host=socket.gethostname()):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, port))
        thread = threading.Thread(target=self.listen)
        thread.start()

    def send_message(self):
            msg = ("testing", 5)
            if msg == "quit":
                return
            else:
                self.socket.send(str(msg).encode())

    def listen(self):
        while True:
            print("Got reply ",self.socket.recv(1024).decode())


if __name__ == '__main__':
    client = ChatClient(PORT)
    client.send_message()