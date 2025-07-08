import yaml
from .error import *
from typing import Dict
from .parse_arg import get_config_args
import sys
import os

"""Открываем и читаем YAML файл"""
def load_config() -> Dict:
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            return config
    except Exception as e:
        raise ConfigLoadError(f"Failed to load config.yaml: {e}")
"""Возвращает уже загруженный объект конфигурации."""


def get_config() -> Dict:
    if len(sys.argv) == 1:
        return load_config()
    else:
        return get_config_args()

CONFIG = get_config()
output_directory = os.path.dirname(CONFIG.get("OUTPUT_PROXIES"))
source_filename = os.path.basename(CONFIG.get("SOURCE_PROXIES"))
filename_without_extension, file_extension = os.path.splitext(source_filename)
CONFIG['FAILED_PROXY'] = os.path.join(output_directory, f"{filename_without_extension}_failed{file_extension}")
# print(CONFIG)
# exit()


