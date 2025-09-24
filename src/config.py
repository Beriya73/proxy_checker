import yaml
from .error import *
from typing import Dict
from .parse_arg import get_config_args
import sys
import os
from pathlib import Path

# Определяем абсолютный путь к корневой папке проекта
PROJECT_ROOT = Path(__file__).resolve().parent.parent

"""Открываем и читаем YAML файл, используя абсолютный путь"""
def load_config() -> Dict:
    config_path = PROJECT_ROOT / 'config.yaml'
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
            # --- Преобразование путей в абсолютные ---
            # Ключи в конфиге, которые могут содержать относительные пути
            path_keys = ["SOURCE_PROXIES", "OUTPUT_PROXIES"]
            
            for key in path_keys:
                if key in config and config[key]:
                    # Получаем путь из конфига
                    file_path = Path(config[key])
                    # Если путь не абсолютный, делаем его абсолютным относительно корня проекта
                    if not file_path.is_absolute():
                        config[key] = str(PROJECT_ROOT / file_path)
            # --- КОНЕЦ НОВОГО БЛОКА ---
            
            return config
            
    except Exception as e:
        raise ConfigLoadError(f"Failed to load {config_path}: {e}")

"""Возвращает уже загруженный объект конфигурации."""
def get_config() -> Dict:
    # Если запуск без аргументов, используем config.yaml
    if len(sys.argv) == 1:
        return load_config()
    # Если есть аргументы командной строки, используем их
    else:
        return get_config_args()

CONFIG = get_config()


output_directory = os.path.dirname(CONFIG.get("OUTPUT_PROXIES", "."))
if not os.path.exists(output_directory) and output_directory:
    os.makedirs(output_directory)

source_filename = os.path.basename(CONFIG.get("SOURCE_PROXIES", "default_source.txt"))
filename_without_extension, file_extension = os.path.splitext(source_filename)

# Создаем путь для _failed файла в той же директории, что и выходной файл
failed_proxy_path = os.path.join(output_directory, f"{filename_without_extension}_failed{file_extension}")
CONFIG['FAILED_PROXY'] = failed_proxy_path
