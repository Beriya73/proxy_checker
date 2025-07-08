import logging

from .error import *
from .proxy_parser import Proxy
from .config import CONFIG
from typing import List

"""Загрузка  прокси"""


def load_proxies() -> List[str]:
    try:
        proxy_file = CONFIG['SOURCE_PROXIES']
        proxy_objects = Proxy.from_file(proxy_file)
        proxies = [proxy.get_default_format() for proxy in proxy_objects]
        if not proxies:
            logging.warning(f"No proxies found in {proxy_file}, works without proxy!")
        return proxies
    except Exception as e:
        raise ProxyLoadError(f"Failed to load proxies: {e}")


# """Загрузка rpc urls"""
# def load_list_rpc() -> List[str]:
#     try:
#         rpc_file = CONFIG['RPC_URLS']
#         list_rpc = load_lines(rpc_file)
#         if not list_rpc:
#             raise UrlsLoadError(f"No urls found in {rpc_file}")
#         return list_rpc
#     except Exception as e:
#         raise UrlsLoadError(f"Failed to load urls: {e}")
# """Возвращает уже загруженный объект конфигурации."""


def get_proxies() -> List:
    return PROXIES

PROXIES = load_proxies()

