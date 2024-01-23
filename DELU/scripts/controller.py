import socket, sys

class controller:
    def __init__(self) -> None:
        self.host = '127.0.0.1'
        self.port = 12345

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        self.client_id = "controller"
        self.client_socket.send(self.client_id.encode('utf-8'))


    def command(self) -> None:
        try:
            while True:
                message = input(" >>> ")
                self.client_socket.send(message.encode('utf-8'))

        except KeyboardInterrupt:
            print("\nClosing the client.")
            self.client_socket.close()
            sys.exit()