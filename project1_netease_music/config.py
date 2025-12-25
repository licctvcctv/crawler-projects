# 数据库配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',  # 修改为你的密码
    'database': 'netease_music',
    'charset': 'utf8mb4'
}

MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'netease_music',
    'collection': 'songs'
}

# 爬虫配置
CRAWL_CONFIG = {
    'delay_min': 2,
    'delay_max': 4,
    'max_songs': 1500,  # 最大爬取歌曲数
}

# 排行榜/歌单ID列表
PLAYLIST_IDS = [
    {'id': 19723756, 'name': '飙升榜'},
    {'id': 3778678, 'name': '热歌榜'},
    {'id': 3779629, 'name': '新歌榜'},
    {'id': 2884035, 'name': '原创榜'},
    {'id': 991319590, 'name': '中文说唱榜'},
    {'id': 71385702, 'name': 'ACG榜'},
    {'id': 71384707, 'name': '古典榜'},
    {'id': 1978921795, 'name': '电音榜'},
    {'id': 2809513713, 'name': '欧美热歌榜'},
    {'id': 2809577409, 'name': '欧美新歌榜'},
    {'id': 5059644681, 'name': '日语榜'},
    {'id': 3001835560, 'name': 'ACG动画榜'},
    {'id': 3001795926, 'name': 'ACG游戏榜'},
    {'id': 21845217, 'name': 'KTV唛榜'},
    {'id': 60131, 'name': '日本Oricon榜'},
    {'id': 745956260, 'name': '网络热歌榜'},
    {'id': 2250011882, 'name': '抖音排行榜'},
    {'id': 5453912201, 'name': '黑胶VIP爱听榜'},
    {'id': 180106, 'name': 'UK排行榜周榜'},
    {'id': 27135204, 'name': '法国NRJ Vos Hits周榜'},
    {'id': 112463, 'name': '美国Billboard周榜'},
    {'id': 4395559, 'name': '华语金曲榜'},
    {'id': 5338990334, 'name': '云音乐民谣榜'},
    {'id': 5059633707, 'name': '云音乐国电榜'},
    {'id': 5059661515, 'name': '云音乐摇滚榜'},
    {'id': 10520166, 'name': '云音乐电子榜'},
    {'id': 6732051, 'name': '云音乐说唱榜'},
    {'id': 6732014, 'name': '云音乐古风榜'},
    {'id': 64016, 'name': '中国TOP排行榜'},
    {'id': 11641012, 'name': 'iTunes榜'},
    {'id': 120001, 'name': 'Hit FM Top榜'},
]
