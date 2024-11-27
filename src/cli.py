import click
import logging
import os
import pwd
import socket
import itertools

from evdev import UInput

from keyboard import PhoneBoard
from mapper import Mapper
from server import Server


logger = logging.getLogger(__name__)


@click.command()
@click.option("-h", "--host", default="localhost", help="Host or IP to bind")
@click.option("-p", "--port", default=1234, help="Port to bind")
def phony(host, port):
    logging.basicConfig(level=logging.DEBUG)

    mapper = Mapper()
    with UInput() as ui:
        phoneboard = PhoneBoard(ui, mapper)
        server = Server(host, port, phoneboard.keystroke)

        os.setuid(pwd.getpwnam("nobody")[2])
        server.run()


@click.command()
@click.option("-h", "--host", default="localhost", help="Host or IP to bind")
@click.option("-p", "--port", default=1234, help="Port to bind")
def test_client(host, port):
    logging.basicConfig(level=logging.DEBUG)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i in itertools.count(start=1):
        sock.sendto(b"0", (host, port))

        if i % 1000 == 0:
            logger.info(f"{i} messages senf")
