# 网络爬虫项目集合

本仓库包含两个网络爬虫项目，用于学习和研究网络数据采集技术。

## 项目列表

### 1. 网易云音乐排行榜爬虫 (project1_netease_music)

爬取网易云音乐多个排行榜的歌曲数据，包括飙升榜、热歌榜、新歌榜、原创榜、ACG榜等30个榜单。

**功能特点：**
- 采集1000+首歌曲数据
- 数据存储到 MySQL 和 MongoDB
- 数据清洗和质量评估
- 可视化分析

### 2. 豆瓣电影爬虫 (project2_douban_movie)

爬取豆瓣电影多个类型的高分电影数据，包括剧情、喜剧、动作、科幻、动画等12个类型。

**功能特点：**
- 采集1200+部电影数据
- 数据存储到 MySQL 和 MongoDB
- 数据清洗和质量评估
- 可视化分析

## 技术栈

- Python 3.x
- requests + fake_useragent
- MySQL + pymysql
- MongoDB + pymongo
- pandas + matplotlib

## 使用方法

```bash
# 进入项目目录
cd project1_netease_music  # 或 project2_douban_movie

# 安装依赖
pip install -r requirements.txt

# 运行爬虫
python crawler.py

# 数据清洗
python data_clean.py

# 生成可视化
python visualize.py
```

## 数据库配置

修改 `config.py` 中的数据库配置：

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的密码',
    'database': 'database_name',
    'charset': 'utf8mb4'
}
```

## 声明

本项目仅用于学习研究目的，请遵守相关网站的服务条款和robots协议。
