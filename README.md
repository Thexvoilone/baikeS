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

获取你想要的数据

```py
from baikes import Baike

baike = Baike("网络爬虫")

print(baike.album)
print(baike.intro)
print(baike.paragraphs)
# ...
```

`Baike` 对象包含以下属性:

|   属性名   |     类型      |    描述    |
| :--------: | :-----------: | :--------: |
|    name    |     `str`     |  条目名称  |
|   title    |     `str`     |  条目标题  |
|   album    |     `str`     | 概述图 URL |
|   intro    |     `str`     |    简介    |
|    card    | `OrderedDict` |  知识卡片  |
| paragraphs | `OrderedDict` |  描述段落  |

有时可能会出现同名词, 参数 category 用于限定词条分类:

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

# 获取百科卡片
python -m baikes -n "网络爬虫" card
```
