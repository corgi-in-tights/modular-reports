import requests
from .utils import get_file_content

class Provider:
    """Basic provider parent."""

    def get_content(self) -> str:
        pass


class StringProvider(Provider):
    """Holds content as a string in memory."""

    def __init__(self, value: str) -> None:
        self.value = value

    def get_content(self):
        return self.value
    

class FileProvider(Provider):
    """Holds content as a string on storage."""

    def __init__(self, path: str) -> None:
        self.path = path

    def get_content(self):
        return get_file_content(self.path)
    

class UrlProvider(Provider):
    """Holds content as a string on a different host."""

    def __init__(self, url: str) -> None:
        self.url = url

    def get_content(self):
        r = requests.get(self.url)
        if (r.status_code == 200):
            return r.text()
        return f'Error in obtaining data from {self.url}, status code {r.status_code}.'