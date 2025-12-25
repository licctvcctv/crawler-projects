# 网易云音乐排行榜爬虫

爬取网易云音乐多个排行榜的歌曲数据，进行数据分析和可视化。

## 功能

- 爬取13个排行榜共1000+首歌曲数据
- 数据存储到 MySQL 和 MongoDB
- 数据清洗和质量评估
- 可视化分析（榜单分布、时长分布、热门歌手等）

## 数据字段

| 字段 | 说明 |
|------|------|
| song_id | 歌曲ID |
| song_name | 歌曲名称 |
| artist_name | 歌手名称 |
| artist_id | 歌手ID |
| album_name | 专辑名称 |
| album_id | 专辑ID |
| duration | 时长(秒) |
| playlist_name | 榜单名称 |
| playlist_id | 榜单ID |
| rank_num | 排名 |

## 安装依赖

```bash
pip install -r requirements.txt
```

## 数据库配置

修改 `config.py` 中的数据库配置：

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的密码',
    'database': 'netease_music',
    'charset': 'utf8mb4'
}
```

## 使用方法

```bash
# 1. 运行爬虫
python crawler.py

# 2. 数据清洗
python data_clean.py

# 3. 生成可视化
python visualize.py
```

## 反爬策略

- 随机延迟（2-4秒）
- 随机User-Agent
- Session保持

## 输出文件

- `data/songs.json` - 原始数据
- `data/songs_cleaned.csv` - 清洗后数据
- `output/*.png` - 可视化图表
