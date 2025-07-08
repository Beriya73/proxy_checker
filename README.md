# Proxy Checker

Простой, но мощный многопоточный скрипт на Python для проверки работоспособности HTTP и SOCKS5 прокси-серверов.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Основные возможности

- **Многопоточность**: Быстрая проверка большого количества прокси за счет использования нескольких потоков.
- **Поддержка ключевых типов прокси**: Проверка **HTTP** и **SOCKS5**.
- **Гибкая настройка**: Возможность указать файл с прокси, количество потоков, тайм-аут итд.
- **Простота**: Легко использовать как через аргументы командной строки, так и без.
- **Сохранение результатов**: Рабочие прокси автоматически сохраняются в файл.

## 🛠️ Установка

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Beriya73/proxy_checker.git
    ```

2.  **Перейдите в директорию проекта:**
    ```bash
    cd proxy_checker
    ```

3.  **Установите необходимые зависимости:**
    (Убедитесь, что у вас установлен `pip`)
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Использование

Скрипт запускается из командной строки с указанием файла с прокси и типа прокси для проверки.

### Формат команды

```bash
python proxy_checker.py source_proxy_file output_proxy_file --proxy <тип_прокси> [другие_аргументы]
```

Check proxy and save results to file

positional arguments:
  source_proxy_file     Proxy input file
  output_proxy_file     Proxy output file

options:
  -h, --help            show this help message and exit
  -r REQUESTS,      --requests REQUESTS
                        number of simultaneous requests(default: 10)
  -p {http,socks5}, --proxy_type {http,socks5}
                        proxy type(default: http)
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for request(default: 10s))


### Пример файла с прокси (`proxies.txt`)

Файл должен содержать по одному прокси в строке в формате `ip:port` или `user:pass@ip:port`.

```
192.168.1.1:8080
user:password@192.168.1.2:3128
8.8.8.8:1080
```

### Примеры запуска

1.  **Проверить HTTP прокси из файла `proxies.txt`:**
    ```bash
    python proxy_checker.py proxies.txt proxies_success.txt --requests 5  --proxy_type http --timeout 5
    ```

2.  **Проверить SOCKS5 прокси, используя 200 потоков, и сохранить результат в `good_socks.txt`:**
    ```bash
    python proxy_checker.py proxies.txt proxies_success.txt -p socks5 -r 200
    ```


    ```

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.