import asyncio
import sys
from loguru import logger
from typing import List
from src.data_class import ProxyResult
from src.mixins import sanitize_proxy, console_sanitizer

from src.mixins import ProxyChecker, split_results, save_split_results, statistics_output

logger.remove()
logger.add(
    sys.stderr,
    filter=console_sanitizer,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{extra[sanitized_message]}</level>"
)

log_path = "logs/proxy_checker.log"
logger.add(
    log_path,
    format="{time:HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="10 MB",
    encoding="utf-8"
)

log_path = "logs/proxy_checker.log"
logger.add(
    log_path,
    # Здесь фильтр не нужен, используем оригинальное {message} со всеми данными
    format="{time:HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="10 MB",
    encoding="utf-8"  # Рекомендуется всегда указывать кодировку
)


async def main():
    try:
        checker = ProxyChecker()
        all_results: List[ProxyResult] = await checker.check_all_proxies()
        split_data = split_results(all_results)
        statistics_output(split_data)
        save_split_results(split_data)

    except Exception as e:
        logger.error("An error occurred in main execution:")
        logger.exception(e)


if __name__ == "__main__":
    asyncio.run(main())
