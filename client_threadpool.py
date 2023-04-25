import sys
import socket
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor

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
    except Exception as ee:
        logging.info(f"ERROR: {str(ee)}")
        exit(0)
    finally:
        logging.warning("closing")
        sock.close()
    return

if __name__ == '__main__':
    with ThreadPoolExecutor() as ThreadPool:
        count = 0
        maximum = 0
        requests = set()
        start_time = time.time()

        while time.time() - start_time < 30:
            request = ThreadPool.submit(send_request)
            requests.add(request)

            complete_request = {req for req in requests if req.done()}
            requests -= complete_request
	
            count += len(complete_request)
            if count > maximum:
                maximum = count
        for req in requests:
            req.result()

        # ThreadPool created
        with open('threadpool.txt', 'w') as f:
            f.write(f'{maximum}\n\n')
        logging.warning(f"Total thread pool maximum: {maximum}")

