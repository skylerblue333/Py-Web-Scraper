import urllib.request
import html.parser
from dataclasses import dataclass, field
from typing import List

@dataclass
class Page:
    url: str
    title: str = ""
    links: List[str] = field(default_factory=list)

class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag == "a":
            for name, val in attrs:
                if name == "href" and val and val.startswith("http"):
                    self.links.append(val)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title = data.strip()

def scrape(url: str) -> Page:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html_content = resp.read().decode("utf-8", errors="replace")
    parser = LinkParser()
    parser.feed(html_content)
    return Page(url=url, title=parser.title, links=parser.links[:20])
