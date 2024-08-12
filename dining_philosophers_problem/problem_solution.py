import asyncio
import logging
import random


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("MAIN")


class Fork:
    def __init__(self, name: str) -> None:
        self.name = name
        self.lock = asyncio.Lock()

    async def __aenter__(self) -> 'Fork':
        await self.lock.acquire()
        logger.info(f"Виделка {self.name} піднята зі стола")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.lock.release()
        logger.info(f"Виделка {self.name} покладена на стіл")


class Philosopher:
    def __init__(self, name: str, left_fork: Fork, right_fork: Fork) -> None:
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork

    async def dine(self) -> None:
        while True:
            await self.think()
            await self.eat()

    async def think(self) -> None:
        logger.info(f"Філософ {self.name} міркує")
        await asyncio.sleep(random.uniform(3, 5))

    async def eat(self) -> None:
        logger.info(f"Філософ {self.name} зголоднів")
        async with self.right_fork:
            logger.info(f"Філософ {self.name} підняв праву виделку")
            async with self.left_fork:
                logger.info(f"Філософ {self.name} підняв ліву виделку")
                await asyncio.sleep(random.uniform(5, 7))
                logger.info(f"Філософ {self.name} закінчив трапезу і поклав виделки на стіл")


async def main():
    """
    Кожен філософ представлений великою буквою від A до E (протигодиникової стрілки)

    Якщо філосов піднімає виделку, що ліворуч від нього, то лівору від імені філософа буде буква,
    інакше буде праворуч.

    Приклад:
    Філософ А, ліворуч від нього виделка EA, праворуч AB
    Філософ D, ліворуч від нього виделка CD, праворуч DE

             D
            ***
         E *   * C
           *   *
         A  ***  B
    """

    names: list[str] = ["A", "B", "C", "D", "E"]

    forks: list[Fork] = [Fork(names[i] + names[(i + 1) % 5]) for i in range(5)]

    philosophers: list[Philosopher] = [
        Philosopher(f"{names[i]}", forks[(i - 1)], forks[i]) for i in range(5)
    ]
    # [EA AB, AB BC, BC CD, CD DE, DE EA]
    await asyncio.gather(*(philosopher.dine() for philosopher in philosophers))


if __name__ == "__main__":
    asyncio.run(main())
