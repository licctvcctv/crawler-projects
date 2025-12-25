# 网络爬虫项目集

本仓库包含两个完整的网络爬虫项目，用于学习和研究目的。

## 项目列表

### 1. 网易云音乐排行榜爬虫

爬取网易云音乐30个排行榜的歌曲数据，包括热歌榜、飙升榜、新歌榜、ACG榜等。

- **数据量**: 1000+ 条
- **字段**: 10个（歌曲ID、歌名、歌手、专辑、时长、榜单等）
- **存储**: MySQL + MongoDB

### 2. 豆瓣电影高分榜爬虫

爬取豆瓣电影12个类型的高分电影数据，包括剧情、喜剧、动作、科幻、动画等。

- **数据量**: 1200 条
- **字段**: 11个（电影ID、片名、评分、评价人数、地区、类型、演员等）
- **存储**: MySQL + MongoDB

## 技术栈

- Python 3.x
- requests + fake_useragent
- pymysql + pymongo
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

## 注意事项

- 仅用于学习研究目的
- 请遵守网站服务条款
- 已设置合理的请求延迟
