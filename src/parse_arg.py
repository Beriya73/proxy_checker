import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(
        description='Check proxy and save results to file.',
        formatter_class=argparse.RawTextHelpFormatter # Для красивого отображения переносов строк в help
    )

    # --- ИЗМЕНЕНИЕ 1: Первый аргумент снова обязательный ---
    # Убираем nargs='?' и default, чтобы он стал обязательным
    parser.add_argument(
        'source_proxy_file',
        type=str,
        help='Proxy input file (required)'
    )

    # --- ИЗМЕНЕНИЕ 2: Второй аргумент остается опциональным ---
    # Используем nargs='?' и default=None, чтобы отследить, был ли он передан
    parser.add_argument(
        'output_proxy_file',
        nargs='?',
        default=None,
        type=str,
        help='Proxy output file for successful proxies.\n'
             'Default: [source_filename]_success.[ext]'
    )

    parser.add_argument(
        '-r', '--requests',
        type=int,
        default=10,
        help='number of simultaneous requests (default: 10)'
    )
    parser.add_argument(
        '-p', '--proxy_type',
        type=str,
        default='http',
        choices=['http', 'socks5'],
        help='proxy type (default: http)'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='timeout for request (default: 10s))'
    )
    return parser.parse_args()


def get_config_args():
    _config = parse_args()

    # --- Логика для генерации имени выходного файла остается той же ---
    # Если пользователь не указал имя выходного файла, генерируем его сами.
    if _config.output_proxy_file is None:
        # Разбираем имя входного файла на имя и расширение
        base_name, extension = os.path.splitext(_config.source_proxy_file)
        # Собираем новое имя для успешных прокси
        _config.output_proxy_file = f"{base_name}_success{extension}"

    return {
        "SETTINGS": {
            "REQUESTS": _config.requests,
            "ATTEMPTS": 2
        },
        "PROXY_TYPE": _config.proxy_type,
        "SOURCE_PROXIES": _config.source_proxy_file,
        "OUTPUT_PROXIES": _config.output_proxy_file,
        "TIMEOUT": _config.timeout
    }