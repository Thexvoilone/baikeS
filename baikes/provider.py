import httpx
from bs4 import BeautifulSoup


class SourceProvider:
    """
    负责发送请求, 提供 HTML, BeautifulSoup
    """

    __client = httpx.Client(follow_redirects=True)
    "Http client"

    def __init__(self, name: str, lemma_id: int | None = None) -> None:
        """
        SourceProvider

        :param name: 要爬取的条目
        """
        soup, html_str = SourceProvider.get_source(name, lemma_id)

        self.name: str = name
        self.soup: BeautifulSoup = soup
        self.html_str: str = html_str

    @staticmethod
    def source_by_url(name: str) -> tuple[BeautifulSoup, str] | None:
        """
        通过 GET `https://baike.baidu.com/item/{name}` 获取 Source

        :param name: 要爬取的条目
        :return: 返会元组 (soup, html_str), 若无词条则返回 None
        :rtype: tuple[bs4.BeautifulSoup, str]  | None
        """
        r = SourceProvider.__client.get(f"https://baike.baidu.com/item/{name}")
        html_str = r.text
        soup = BeautifulSoup(html_str, "html.parser")

        if name in soup.find("title").string:
            return soup, html_str

        return None

    @staticmethod
    def source_by_lemma(name: str, lemma_id: int) -> tuple[BeautifulSoup, str] | None:
        """
        指定词条义项进行请求
        通过 GET `https://baike.baidu.com/item/{name}/{lemma_id}` 获取 Source

        :param name: 要爬取的条目
        :return: 返会元组 (soup, html_str), 若无词条则返回 None
        :rtype: tuple[bs4.BeautifulSoup, str]  | None
        """
        r = SourceProvider.__client.get(f"https://baike.baidu.com/item/{name}/{lemma_id}")
        html_str = r.text
        soup = BeautifulSoup(html_str, "html.parser")

        if name in soup.find("title").string:
            return soup, html_str

        return None

    @staticmethod
    def get_source(name: str, lemma_id: int | None) -> tuple[BeautifulSoup, str]:
        """
        获取解析源

        :param name: 要爬取的条目
        :return: 返会元组 (soup, html_str), 若无词条则会触发报错
        :rtype: tuple[bs4.BeautifulSoup, str]  | None
        """

        if lemma_id != None:
            provider = SourceProvider.source_by_lemma(name, lemma_id)
            return provider if provider != None else None
        else:
            provider = SourceProvider.source_by_url(name)
            if provider != None:
                return provider

        raise Exception("No Result found!")
