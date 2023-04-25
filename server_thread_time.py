from socket import *
import threading
import logging
import time
import sys

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address, response):
        self.connection = connection
        self.address = address
        self.response = response
        threading.Thread.__init__(self)

    def run(self):
        msg = ""
        while True:
            data = self.connection.recv(32)
            if data:
                d = data.decode()
                msg = msg + d
                print(msg[-2:], msg[:4])
                if msg[-2:] == '\r\n' and msg[:4] == 'TIME':
                    curr_time = time.strftime("%H:%M:%S")
                    hasil = f"JAM {curr_time}\r\n"
                    logging.warning(f"[SERVER] balas ke client: {hasil}")
                    hasil = hasil.encode()
                    self.connection.sendall(hasil)
                    msg = ""
                    self.response.update_response()
                else:
                    break
            else:
                break
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.response = 0
        self.my_socket = socket(AF_INET, SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")
            clt = ProcessTheClient(self.connection, self.client_address, self)
            clt.start()
            self.the_clients.append(clt)

    def update_response(self):
        self.response += 1
        print(f"Total response: {self.response}")

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
