import asyncio
import random
import logging

HOST: str = "127.0.0.1"
PORT: int = 8888

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SERVER")


class WeatherServer:
    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host = host
        self.port = port
        self.clients: list[asyncio.Transport] = []

    def create_protocol(self) -> 'WeatherServerProtocol':
        return WeatherServerProtocol(self)

    @staticmethod
    async def get_weather_data() -> str:
        temperature: float = random.uniform(-15, 35)
        humidity: float = random.uniform(30, 100)
        wind_speed: float = random.uniform(0, 15)
        return f"Температура: {temperature:.2f}C, Вологість: {humidity:.2f}%, Швидкість вітру: {wind_speed:.2f} m/s"

    async def broadcast_weather_data(self) -> None:
        while True:
            weather_data: str = await self.get_weather_data()
            logger.info(f"Передаю дані погоди: {weather_data}")
            for client in self.clients:
                client.write(weather_data.encode())
            await asyncio.sleep(5)

    async def start_server(self) -> None:
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        server: asyncio.base_events.Server = await loop.create_server(
            self.create_protocol,
            self.host, self.port
        )

        async with server:
            await server.start_serving()
            asyncio.create_task(self.broadcast_weather_data())
            await server.serve_forever()


class WeatherServerProtocol(asyncio.Protocol):
    def __init__(self, server: WeatherServer) -> None:
        self.server = server
        self.transport: asyncio.Transport | None = None

    def connection_made(self, transport: asyncio.Transport) -> None:
        self.transport = transport
        self.server.clients.append(transport)
        client_name: tuple[str, int] | None = transport.get_extra_info("peername")
        logger.info(f"Клієнт приєднався: {client_name}")

    def connection_lost(self, exc: Exception | None) -> None:
        self.server.clients.remove(self.transport)
        logger.info(f"Клієнт від'єднався: {self.transport.get_extra_info('peername')}")


if __name__ == "__main__":
    weather_server = WeatherServer()
    asyncio.run(weather_server.start_server())
