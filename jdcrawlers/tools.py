import requests


class StaticWebCrawler:

    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        }
        self.proxy_ip = {}

    def get_response(self, url, **kwargs):
        response = requests.get(url, **kwargs)
        if response.status_code == 200:
            return response
        else:
            raise ConnectionError


class ConnectionError(Exception):
    """Connection Error for requests

    Args:
        Exception (Error): exception
    """