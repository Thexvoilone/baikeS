import json
import re

from collections import OrderedDict
from typing import Literal, TypeAlias
from urllib.parse import urlparse

from loguru import logger
from bs4 import ResultSet, Tag


from baikes.provider import SourceProvider


BaikeCategory: TypeAlias = Literal["企业", "动物", "品牌", "书刊", "数字产品", "影视作品", "音乐作品", "植物", "其它", "其他"]


class Baike:

    def __init__(self, name: str, category: BaikeCategory | None = None, once: bool = True):
        """
        百度百科

        :param name: 百科条目
        :param category: 百科分类
        :param once: 是否一次性解析
        """
        self.__provider = SourceProvider(name)
        self.name = name
        "条目名"
        if self.__provider.soup == None:
            raise Exception("No Result")

        self.__pagedata = self.__get_pagedata()
        self.__current_lemmaid: int = self.__pagedata["lemmaId"]

        if category != None:
            lemma_id = self.__get_lemmaid(category)
            if lemma_id == None:
                raise Exception("No such category")

            if self.__current_lemmaid != lemma_id:
                self.__current_lemmaid = lemma_id
                self.__provider = SourceProvider(name, lemma_id)
                self.__pagedata = self.__get_pagedata()

        self.title = self.__provider.soup.find("title").string
        "百科标题"

        self.album: str | None = None
        "概述图 URL"
        self.intro: str | None = None
        "简介"
        self.card: OrderedDict | None = None
        "知识卡片"
        self.paragraphs: OrderedDict | None = None
        "百科段落"

        if once:
            self.get_all()

    def __concat(self, str_list: list[str]) -> str:
        result = ""
        for text in str_list:
            result += text
        return result

    def __ord_di_str(self, di: OrderedDict | None, start: str = ""):
        result = ""

        if di == None:
            return "None"

        for key, text in di.items():
            result += f"{start}{key}: {text}\n"

        return result

    def __get_lemmaid(self, category: BaikeCategory) -> int | None:
        """
        返回词义 id (lemma_id)

        :param category: 分类
        :return: int | None
        :rtype: 返回匹配的 lemma_id; 若不存在分类则返回 None
        """
        pagedata = self.__pagedata
        navigation: list = pagedata.get("navigation")  # 会出现 navigation 不存在的情况

        if navigation == None:
            logger.error(f"{self.name} has no category, will use default action")
            return self.__current_lemmaid

        lemmas: list = navigation["lemmas"]

        for e in lemmas:
            if e["classify"][0] == category:
                return e["lemmaId"]

        return None

    def __get_pagedata(self) -> dict:

        html_str = self.__provider.html_str
        # TODO 修改判断逻辑, 避免抛错
        try:
            var_str = re.search(r"window\.PAGE_DATA\=.\{.*\}<", html_str, re.S).group(0)[0:-1]
            pagedata_str = re.search(r"\{.*\}", var_str).group(0)
            return json.loads(pagedata_str)
        except:
            logger.error("Fail to parse html text")

    def get_all(self):
        """
        解析当前条目的所有数据, 并返回对象本身

        :return: Baike
        :rtype: Baike 对象
        """
        self.get_album()
        self.get_intro()
        self.get_card()
        self.get_paragraphs()

        return self

    def get_album(self) -> str | None:
        if self.album != None:
            return self.album

        pagedata = self.__pagedata

        album_src = None
        # TODO 防止抛错
        try:
            album_src: str = pagedata["abstractAlbum"]["coverPic"]["url"]
            # 去除查询参数
            pa = urlparse(album_src)
            album_src = album_src.replace(pa.query, "")
        except:
            logger.error(f"'{self.name}' has no album")

        self.album = album_src
        return album_src

    def get_intro(self) -> str | None:
        if self.intro != None:
            return self.intro

        soup = self.__provider.soup

        intro = soup.find(class_="J-summary")
        if intro != None:
            intro_text = re.sub(r"\[.*?\]", "", intro.text)
            self.intro = intro_text
            return intro_text

        return None

    def get_card(self) -> OrderedDict:
        if self.card != None:
            return self.card

        pagedata = self.__pagedata
        card = pagedata["card"]
        left: list = card["left"]
        right: list = card["right"]
        di = OrderedDict()
        for e in left:
            title: str = e["title"]
            text_list: list = e["data"][0]["text"]

            t_list = []
            for t in text_list:
                t: dict
                t_list.append(t.get("text", ""))
            text = self.__concat(t_list)

            di[title] = text

        for e in right:
            title: str = e["title"]
            text_list: list = e["data"][0]["text"]

            t_list = []
            for t in text_list:
                t: dict
                t_list.append(t.get("text", ""))
            text = self.__concat(t_list)

            di[title] = text

        self.card = di
        return di

    def get_paragraphs(self) -> OrderedDict:
        if self.paragraphs != None:
            return self.paragraphs

        soup = self.__provider.soup

        di = OrderedDict()
        for tag in soup.find_all("h2"):
            tag: Tag
            if not tag.get("name"):
                continue
            title_idx = int(tag["name"]) - 1
            title = tag.text

            desc = ""
            ih3 = 1
            ipragraph = 1

            for i in range(1, 3):
                ipragraph = i
                div = soup.find(attrs={"data-idx": f"{title_idx}-{ipragraph}"})  # data-index h3 标题
                divh3 = soup.find(attrs={"data-index": f"{title_idx+1}-{ih3}"})  # data-idx 自然段

                if div != None:
                    break

            while divh3 != None or div != None:
                if divh3 != None:
                    desc += divh3.text + "\n"
                    ih3 += 1

                # TODO 某些情况下, 整个段落都是表格, 暂未有相关处理
                while div != None:
                    div: Tag
                    dspans: ResultSet[Tag] = div.find_all(attrs={"data-text": "true"})

                    for span in dspans:
                        s = span.text
                        desc += s if s != None else ""
                    desc += "\n"

                    ipragraph += 1
                    div = soup.find(attrs={"data-idx": f"{title_idx}-{ipragraph}"})

                ipragraph += 1
                div = soup.find(attrs={"data-idx": f"{title_idx}-{ipragraph}"})
                divh3 = soup.find(attrs={"data-index": f"{title_idx+1}-{ih3}"})

            # 去除类似 [1] 的脚标
            desc = re.sub(r"\[.*?\]", "", desc)

            di[title] = desc

        self.paragraphs = di
        return di

    def __str__(self) -> str:
        self.get_all()
        output = ""

        output += f"Title: {self.title}\n"
        output += f"Name: {self.name}\n"
        output += f"Album: {self.album}\n"
        output += f"Intro: \t{self.intro}\n"

        card = self.__ord_di_str(self.card, "\t")
        paragraphs = self.__ord_di_str(self.paragraphs)

        output += f"Card: \n{card}"
        output += f"Paragraphs: \n{paragraphs}"

        return output
