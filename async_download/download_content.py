import asyncio
import aiohttp
import aiofiles
import argparse
import logging
import os
import sys


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("MAIN")


TIMEOUT: int = 10


async def fetch_content(session: aiohttp.ClientSession, url: str, index: int, output_dir: str) -> bool:
    try:
        async with session.get(url, timeout=TIMEOUT) as response:
            content: str = await response.text()
            filename: str = os.path.join(output_dir, f"output_{index}.txt")
            async with aiofiles.open(filename, "w", encoding="utf-8") as file:
                await file.write(content)
            logger.info(f"Завантажено контент за посиланням: [{url}] та збережно до {filename}")
            return True
    except asyncio.TimeoutError:
        logger.error(f"Час очікування вичерпано: {url}")
    except aiohttp.ClientError as ex:
        logger.error(f"Сталась помилка {ex} при завантажені даних за посиланням: {url}")
    except Exception as ex:
        logger.error(f"Непередбачена помилка: {ex}")
    return False


async def download_all(urls: list[str], output_dir: str) -> None:
    total_urls: int = len(urls)
    successful_downloads: int = 0
    failed_downloads: int = 0

    async with aiohttp.ClientSession() as session:
        tasks: list[asyncio.Task] = [
            asyncio.create_task(fetch_content(session, url.strip(), index, output_dir))
            for index, url in enumerate(urls, start=1)
        ]

        for i, task in enumerate(asyncio.as_completed(tasks), start=1):
            result: bool = await task
            if result:
                successful_downloads += 1
            else:
                failed_downloads += 1

            logger.info(f"Прогрес: {i}/{total_urls} URL-лів оброблено")

        logger.info(f"Успішно завантажено: {successful_downloads} / Не завантажено: {failed_downloads}")


def main():
    parser = argparse.ArgumentParser(description="Асинхроне завантаження URL")
    parser.add_argument("file", type=str, help="Посилання на файл, що містить в собі URL-ли")
    parser.add_argument("--output-dir", type=str, default="content", help="Папка в яку буде збережно контент")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        logger.error(f"Файл {args.file} не знайдено")
        sys.exit(1)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        logger.debug(f"Створено папку, куди буде завантажено контент: {args.output_dir}")

    with open(args.file, "r") as file:
        urls: list[str] = file.readlines()

    asyncio.run(download_all(urls, args.output_dir))


if __name__ == "__main__":
    # Команда для виконання
    # python async_download\download_content.py async_download\urls.txt --output-dir async_download\content
    main()
