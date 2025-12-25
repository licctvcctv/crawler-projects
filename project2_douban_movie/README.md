# 豆瓣电影高分榜爬虫

爬取豆瓣电影多个类型的高分电影数据，进行数据分析和可视化。

## 功能

- 爬取12个类型共1200部高分电影数据
- 数据存储到 MySQL 和 MongoDB
- 数据清洗和质量评估
- 可视化分析（评分分布、类型分布、地区分布等）

## 数据字段

| 字段 | 说明 |
|------|------|
| movie_id | 电影ID |
| title | 电影名称 |
| score | 豆瓣评分 |
| vote_count | 评价人数 |
| release_date | 上映日期 |
| regions | 国家/地区 |
| types | 电影类型 |
| actors | 主演 |
| movie_url | 电影链接 |
| cover_url | 海报链接 |
| category | 采集分类 |

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
    'database': 'douban_movie',
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

- 随机延迟（1.5-3秒）
- 随机User-Agent
- Session保持
- 内存级去重

## 输出文件

- `data/movies.json` - 原始数据
- `data/movies_cleaned.csv` - 清洗后数据
- `output/*.png` - 可视化图表
