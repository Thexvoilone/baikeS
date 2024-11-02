## baike-spider

百度百科简易爬虫

> ⚠️ 该爬虫仅用于学习使用, 不得用于任何非法用途或侵犯他人合法权益 ⚠️

[检察日报: 爬取数据需遵守](https://www.spp.gov.cn/llyj/202202/t20220210_543998.shtml)

---

### 安装

```bash
pip install baike-spider
```

---

### 使用

---

#### 模块

一次性解析全部:
该方法会一次性解析全部的数据并存储进对象属性中

```py
from baikes import Baike

baike = Baike("网络爬虫")

print(baike.album)
print(baike.intro)
print(baike.paragraphs)
# ...
```

部分解析:
当你只需爬取部分数据时, 该方法能会降低部分性能损耗

```py
from baikes import Baike

baike = Baike("网络爬虫", once=Flase)
intro = baike.get_intro()

print(intro)
```

有时会出现同名词, 参数 category 用于限定词条分类:

```py
from baikes import Baike

baike = Baike("黄蜂", category="动物")
```

---

#### 命令行

该爬虫可使用命令行进行调用

示例:

```py
# 获取全部
python -m baikes -n "网络爬虫"

# 限定词条分类
python -m baikes -n "黄蜂" -c "动物"

# 一次性解析:
# 获取百科卡片
python -m baikes -n "网络爬虫" card

# 部分解析:
# 获取百科简介
python -m baikes -n "网络爬虫" -o False get_card
```
