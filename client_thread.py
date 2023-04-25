import sys
import socket
import logging
import threading
import time

def send_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 45000)
    logging.warning(f"Connecting to {server_address}")
    sock.connect(server_address)

    try:
        request = f'TIME threading \r\n'
        logging.warning(f"Dikirim dari client: {request}")
        sock.sendall(request.encode())
        # Listening response
        data = sock.recv(32)
        logging.warning(f"Diterima dari server: {data}")
    finally:
        logging.warning("closing")
        sock.close()
    return

if __name__ == '__main__':
    count = 0
    maximum = 0
    start_time = time.time()
    while time.time() - start_time < 30:
        thread = threading.Thread(target=send_request)
        thread.start()
        thread.join()

        count += 1
        if count > maximum:
            maximum = count
    # Thread created
    with open('threading.txt', 'w') as f:
        f.write(f"{maximum}\n\n")
    print(f"Total threads maximum: {maximum}")

