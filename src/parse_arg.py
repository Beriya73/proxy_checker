import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Check proxy and save results to file')

    parser.add_argument(
        'source_proxy_file',
        type=str,
        help='Proxy input file')

    parser.add_argument(
        'output_proxy_file',
        type=str,
        help='Proxy output file')

    parser.add_argument(
        '-r','--requests',
        type=int,
        default=10,
        help='number of simultaneous requests(default: 10)'
    )
    parser.add_argument(
        '-p','--proxy_type',
        type=str,
        default='http',
        choices=['http', 'socks5'],
        help='proxy type(default: http)'
    )
    parser.add_argument(
        '-t','--timeout',
        type=int,
        default=10,
        help='timeout for request(default: 10s))'
    )
    return parser.parse_args()



def get_config_args():
    _config = parse_args()
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
