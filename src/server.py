import asyncio
import logging
import socket


logger = logging.getLogger(__name__)


class QueuedProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.queue = asyncio.Queue(maxsize=4096)

    def datagram_received(self, data, addr):
        try:
            self.queue.put_nowait(data.decode('utf-8'))
        except asyncio.QueueFull:
            logger.error('unable to handle incoming data, queue oveflow')

    async def rcv_data(self):
        while True:
            yield await self.queue.get()
            self.queue.task_done()


class Server:
    def __init__(self, host, port, callback):
        self.callback = callback
        self.host = host
        self.port = port

    def run(self):
        logger.info('Starting server')
        asyncio.run(self._run())

    async def _run(self):
        loop = asyncio.get_running_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            QueuedProtocol,
            local_addr=(self.host, self.port))

        try:
            async for data in protocol.rcv_data():
                logger.debug(f'received data: {data}')
                await self.callback(data)
        finally:
            transport.close()
