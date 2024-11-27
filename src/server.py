import asyncio
import logging


logger = logging.getLogger(__name__)


class QueuedProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue):
        self.queue = queue

    def datagram_received(self, data, addr):
        try:
            self.queue.put_nowait(data.decode("utf-8"))
        except asyncio.QueueFull:
            logger.error("unable to handle incoming data, queue oveflow")


class Server:
    def __init__(self, host, port, callback):
        self.callback = callback
        self.host = host
        self.port = port
        self.queue = asyncio.Queue(maxsize=4096)

    def run(self):
        logger.info("Starting server")
        asyncio.run(self._run())

    async def _run(self):
        loop = asyncio.get_running_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: QueuedProtocol(self.queue),
            local_addr=(self.host, self.port),
        )

        try:
            while True:
                data = await self.queue.get()
                logger.debug(f"received data: {data}")
                loop.create_task(self.callback(data))
                self.queue.task_done()
        finally:
            transport.close()
