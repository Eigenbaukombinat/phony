import logging
import socket


logger = logging.getLogger(__name__)


class Server:
    def __init__(self, host, port, callback):
        self.callback = callback
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        self.s.bind((self.host, self.port))
        logger.info('Server started')

        while True:
            data, address = self.s.recvfrom(4096)
            logger.debug(f"Server received: {data.decode('utf-8')}")

            self.callback(data.decode('utf-8'))
