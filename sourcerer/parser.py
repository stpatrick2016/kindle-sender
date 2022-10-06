import re


class SourceParser:
    def __init__(self, url):
        self._url = url

    def get_download_url(self) -> str:
        m = re.search("flibusta\\.is/b/([0-9]+)", self._url)
        id = m.group(1)
        return f"https://flibusta.is/b/{id}/epub"
