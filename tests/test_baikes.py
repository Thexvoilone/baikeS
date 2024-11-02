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

    intro1 = Baike(TEST_WORDS[0], category="其他", once=False).get_intro()
    sleep(1)
    intro2 = Baike(TEST_WORDS[0], category="动物", once=False).get_intro()

    assert intro1 != intro2
