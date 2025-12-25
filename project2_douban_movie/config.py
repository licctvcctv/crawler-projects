 # 数据库配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',  # 修改为你的密码
    'database': 'douban_movie',
    'charset': 'utf8mb4'
}

MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'douban_movie',
    'collection_movies': 'movies',
}

# 爬虫配置
CRAWL_CONFIG = {
    'delay_min': 1.5,
    'delay_max': 3,
    'max_movies': 1200,  # 最大爬取数量
    'max_per_type': 120,  # 每个类型最多爬取数量
}

# 电影类型ID
MOVIE_TYPES = [
    {'id': 11, 'name': '剧情'},
    {'id': 24, 'name': '喜剧'},
    {'id': 5, 'name': '动作'},
    {'id': 13, 'name': '爱情'},
    {'id': 17, 'name': '科幻'},
    {'id': 25, 'name': '动画'},
    {'id': 10, 'name': '悬疑'},
    {'id': 19, 'name': '惊悚'},
    {'id': 1, 'name': '恐怖'},
    {'id': 3, 'name': '奇幻'},
    {'id': 22, 'name': '战争'},
    {'id': 14, 'name': '传记'},
]
