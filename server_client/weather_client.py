import asyncio
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CLIENT")


HOST: str = "127.0.0.1"
PORT: int = 8888


class WeatherClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport: asyncio.Transport | None = None

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.transport = transport
        logger.info("Підключено до серверу погоди")

    def data_received(self, data: bytes) -> None:
        logger.info(f"Погодні дані: {data.decode()}")

    def connection_lost(self, exc: Exception | None) -> None:
        logger.info("Відключено від серверу")


async def main():
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

    transport: asyncio.Transport
    protocol: WeatherClientProtocol

    transport, protocol = await loop.create_connection(
        lambda: WeatherClientProtocol(),
        HOST, PORT
    )

    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()

if __name__ == '__main__':
    asyncio.run(main())
