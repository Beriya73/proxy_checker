import time
import aiohttp
from aiohttp_socks import ProxyConnector
import asyncio
from src.config import CONFIG
from .decorator import retry_async
from loguru import logger
from src.loaders import PROXIES
from src.data_class import ProxyResult
from typing import List, Dict, Optional
from .error import *
import re
IP_API_URL = "http://ip-api.com/json/?fields=123417"


class ProxyChecker:
    def __init__(self):
        super().__init__()
        self.config: Dict = CONFIG
        self.proxies: List[str] = PROXIES
        self.concurrency_limit = CONFIG.get('SETTINGS').get('REQUESTS')
        self.semaphore = asyncio.Semaphore(self.concurrency_limit)
        logger.success(
            f"ProxyChecker initialized. Loaded {len(PROXIES)} proxies. Concurrency limit: {self.concurrency_limit}."
            f" Proxy type: {CONFIG.get('PROXY_TYPE')}")
        self.result: Optional[ProxyResult] = None

    @retry_async(delay=1.0)
    async def check_proxy(self, proxy: str,
                          proxy_type: str = 'http') -> ProxyResult | None:
        start_time = time.perf_counter()
        timeout_obj = aiohttp.ClientTimeout(total=self.config.get("TIMEOUT", 10))
        proxy_url = None

        if proxy:
            proxy_url = f"socks5://{proxy}" if proxy_type == 'socks5' else f"http://{proxy}"

        connector = ProxyConnector.from_url(proxy_url)
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout_obj) as session:
                async with session.get(url=IP_API_URL) as response:

                    if response.status == 200:
                        response_time = time.perf_counter() - start_time
                        data = await response.json()
                        self.result = ProxyResult(
                            working=True,
                            ip=data.get('query'),
                            country=data.get('country'),
                            region=data.get('regionName'),
                            city=data.get('city'),
                            isp=data.get('isp'),
                            resptime=round(response_time, 2),
                            proxy=proxy,
                            error="",
                        )
                        if self.result.working:
                            logger.success(f"Proxy: {self.result.proxy}")
                            logger.info(f"Info: {self.result}")
                        return self.result

                    else:
                        raise ErrorResponseStatus(f"Response status: {response.status}")
        except Exception as e:
            raise e

    async def check_proxy_with_semaphore(self, proxy: str) -> ProxyResult:
        self.concurrency_limit = CONFIG.get('SETTINGS').get('REQUESTS')
        self.semaphore = asyncio.Semaphore(self.concurrency_limit)
        async with self.semaphore:
            try:
                return await self.check_proxy(proxy=proxy, proxy_type=CONFIG['PROXY_TYPE'])
            except Exception as e:
                logger.error(f"Proxy check exception {proxy}: {type(e).__name__}: {e}")
                return ProxyResult(
                    proxy=proxy,
                    working=False,
                    error=f"{type(e).__name__}: {e}"
                )

    async def check_all_proxies(self) -> List[ProxyResult] | None:
        """Проверка всех прокси параллельно и возврат результатов"""
        if not PROXIES:
            logger.warning("No proxy to check")
            return []

        logger.success(f"We're starting a parallel check: {len(PROXIES)} proxies...\n")
        tasks = [self.check_proxy_with_semaphore(proxy) for proxy in PROXIES]

        try:
            all_results = await asyncio.gather(*tasks, return_exceptions=True)
            return all_results
        except Exception as e:
            logger.error(f"Critical error during batch proxy verification: {e}")
            return []
        finally:
            await self.close_connector()

    async def close_connector(self):
        """Метод для корректного закрытия коннектора."""
        if hasattr(self, 'connector') and self.connector and not self.connector.closed:
            await self.connector.close()
            logger.info("Aiohttp TCPConnector closed.")


def split_results(all_results: List[ProxyResult]) -> Dict:
    working_proxies = [res for res in all_results if res.working]
    failed_proxies = [res for res in all_results if not res.working]
    return {"Working": working_proxies, "Failed": failed_proxies}


def statistics_output(parse_results: Dict):
    # --- Подведение итогов ---
    working = parse_results.get("Working")
    works_num = len(working) if working else 0
    failed = parse_results.get("Failed")
    failed_num = len(failed) if failed else 0

    print("\n-------- Inspection results --------")
    logger.info(f"Total checked: {works_num + failed_num}")
    logger.info(f"Working proxies: {works_num}")
    logger.info(f"Non-working proxies: {failed_num}")
    print("------------------------------------")


def save_split_results(parse_results: Dict):
    if parse_results.get("Working"):
        try:
            with open(CONFIG.get("OUTPUT_PROXIES"), 'w', encoding='utf-8') as f:
                for proxy_obj in parse_results.get("Working"):
                    f.write(f"{proxy_obj.proxy}\n")
        except Exception as e:
            logger.error(f"Failed to save {e}")
    # 5. Записываем нерабочие прокси в proxies_failed.txt
    if parse_results.get("Failed"):
        with open(CONFIG.get("FAILED_PROXY"), 'w', encoding='utf-8') as f:
            for proxy_obj in parse_results.get("Failed"):
                f.write(f"{proxy_obj.proxy}\n")
    else:
        with open(CONFIG.get("FAILED_PROXY"), 'w', encoding='utf-8') as f:
            f.write(f"EMPTY\n")


def sanitize_proxy(message: str) -> str:
    pattern = re.compile(r"([a-zA-Z0-9\-]+):([a-zA-Z0-9]+)(@.+)")
    sanitized_message = pattern.sub(r"\1:***\3", message)
    return sanitized_message

def console_sanitizer(record) -> bool:
    record["extra"]["sanitized_message"] = sanitize_proxy(record["message"])
    return True
