from time import sleep, time
from baikes.baike import Baike

TEST_WORDS = [
    "黄蜂",  # 0
    "兰博基尼",  # 1
    "小米",  # 2
    "石蝇",  # 3
    "石蛃",  # 4
    "爬虫",  # 5
    "麻雀",  # 6
    "七星瓢虫",  # 7
]


def test_basic():
    baike = Baike(TEST_WORDS[4])
    assert baike.title != None

    sleep(1)


def test_category():
    intro1 = Baike(TEST_WORDS[0], category="其他").intro
    intro2 = Baike(TEST_WORDS[0], category="动物").intro

    assert intro1 != intro2
    sleep(1)


def test_all_members():
    baike = Baike(TEST_WORDS[3])
    assert baike.title != None
    assert baike.intro != None
    assert baike.album != None
    assert len(baike.card.keys()) > 0
    assert len(baike.paragraphs.keys()) > 0

    sleep(1)


# TODO test TEST_WORDS[6]
