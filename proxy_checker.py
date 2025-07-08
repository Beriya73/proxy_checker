import asyncio
import sys
from loguru import logger
from typing import List
from src.data_class import ProxyResult


from src.mixins import ProxyChecker,split_results,save_split_results,statistics_output

logger.remove()
log_path = "logs/proxy_checker.log"
logger.add(sys.stderr,
           format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
logger.add(log_path, format="{time:HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}", level="DEBUG",
           rotation="10 MB")



async def main():
    try:

        checker = ProxyChecker()
        all_results:List[ProxyResult] = await checker.check_all_proxies()
        split_data =split_results(all_results)
        statistics_output(split_data)
        save_split_results(split_data)

    except Exception as e:
        logger.error("An error occurred in main execution:")
        logger.exception(e)


if __name__ == "__main__":
    asyncio.run(main())
