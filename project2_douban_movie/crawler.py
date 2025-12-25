"""
豆瓣电影爬虫
爬取多个类型的高分电影数据
"""
import requests
import time
import random
import json
from fake_useragent import UserAgent
import pymysql
from pymongo import MongoClient
from config import MYSQL_CONFIG, MONGODB_CONFIG, CRAWL_CONFIG, MOVIE_TYPES


class DoubanMovieCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.movies = []
        self.seen_ids = set()
        self.init_mysql()
        self.init_mongodb()
    
    def init_mysql(self):
        """初始化MySQL数据库"""
        conn = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            charset=MYSQL_CONFIG['charset']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        conn.close()
        
        self.mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        self.mysql_cursor = self.mysql_conn.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id VARCHAR(50) UNIQUE,
            title VARCHAR(500),
            score DECIMAL(3,1),
            vote_count INT,
            release_date VARCHAR(50),
            regions VARCHAR(200),
            types VARCHAR(200),
            actors VARCHAR(1000),
            movie_url VARCHAR(500),
            cover_url VARCHAR(500),
            category VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        self.mysql_cursor.execute(create_table_sql)
        self.mysql_conn.commit()
        print("✓ MySQL数据库初始化完成")
    
    def init_mongodb(self):
        """初始化MongoDB"""
        self.mongo_client = MongoClient(
            MONGODB_CONFIG['host'], 
            MONGODB_CONFIG['port']
        )
        self.mongo_db = self.mongo_client[MONGODB_CONFIG['database']]
        self.mongo_collection = self.mongo_db[MONGODB_CONFIG['collection_movies']]
        print("✓ MongoDB初始化完成")
    
    def get_headers(self):
        """获取随机请求头"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://movie.douban.com/typerank',
        }
    
    def fetch_movies(self, type_id, type_name, start=0, limit=50):
        """获取电影列表"""
        url = 'https://movie.douban.com/j/chart/top_list'
        params = {
            'type': type_id,
            'interval_id': '100:90',
            'action': '',
            'start': start,
            'limit': limit
        }
        
        try:
            response = self.session.get(
                url, headers=self.get_headers(), 
                params=params, timeout=15
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"  请求失败: {e}")
            return []
    
    def parse_movie(self, movie, category):
        """解析电影数据"""
        try:
            movie_id = movie.get('id', '')
            return {
                'movie_id': str(movie_id),
                'title': movie.get('title', ''),
                'score': float(movie.get('score', 0)) if movie.get('score') else 0,
                'vote_count': int(movie.get('vote_count', 0)),
                'release_date': movie.get('release_date', ''),
                'regions': '/'.join(movie.get('regions', [])),
                'types': '/'.join(movie.get('types', [])),
                'actors': '/'.join(movie.get('actors', [])[:5]),
                'movie_url': movie.get('url', ''),
                'cover_url': movie.get('cover_url', ''),
                'category': category,
            }
        except Exception as e:
            print(f"  解析失败: {e}")
            return None
    
    def save_to_mysql(self, movie):
        """保存到MySQL"""
        try:
            sql = """
            INSERT IGNORE INTO movies 
            (movie_id, title, score, vote_count, release_date, regions, 
             types, actors, movie_url, cover_url, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.mysql_cursor.execute(sql, (
                movie['movie_id'], movie['title'], movie['score'],
                movie['vote_count'], movie['release_date'], movie['regions'],
                movie['types'], movie['actors'], movie['movie_url'],
                movie['cover_url'], movie['category'],
            ))
            self.mysql_conn.commit()
            return True
        except Exception as e:
            print(f"  MySQL保存失败: {e}")
            return False
    
    def save_to_mongodb(self, movie):
        """保存到MongoDB"""
        try:
            self.mongo_collection.update_one(
                {'movie_id': movie['movie_id']},
                {'$set': movie},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"  MongoDB保存失败: {e}")
            return False
    
    def crawl(self):
        """执行爬取"""
        print("\n" + "="*50)
        print("豆瓣电影爬虫")
        print("="*50)
        
        total_count = 0
        max_movies = CRAWL_CONFIG['max_movies']
        max_per_type = CRAWL_CONFIG.get('max_per_type', 200)
        
        for movie_type in MOVIE_TYPES:
            if total_count >= max_movies:
                break
            
            type_id = movie_type['id']
            type_name = movie_type['name']
            print(f"\n正在爬取: {type_name} (type={type_id})")
            
            start = 0
            type_count = 0
            
            while total_count < max_movies and type_count < max_per_type:
                movies = self.fetch_movies(type_id, type_name, start)
                
                if not movies:
                    break
                
                for movie in movies:
                    if total_count >= max_movies or type_count >= max_per_type:
                        break
                    
                    movie_id = str(movie.get('id', ''))
                    if movie_id in self.seen_ids:
                        continue
                    
                    parsed = self.parse_movie(movie, type_name)
                    if parsed:
                        self.save_to_mysql(parsed)
                        self.save_to_mongodb(parsed)
                        self.movies.append(parsed)
                        self.seen_ids.add(movie_id)
                        total_count += 1
                        type_count += 1
                
                print(f"  已爬取 {type_count} 部电影...")
                start += 50
                
                delay = random.uniform(
                    CRAWL_CONFIG['delay_min'], 
                    CRAWL_CONFIG['delay_max']
                )
                time.sleep(delay)
                
                if len(movies) < 50:
                    break
        
        print(f"\n{'='*50}")
        print(f"爬取完成！共获取 {total_count} 部电影")
        print(f"数据已保存到 MySQL 和 MongoDB")
        print(f"{'='*50}")
        
        self.save_to_json()
        return total_count
    
    def save_to_json(self):
        """保存到JSON文件"""
        with open('data/movies.json', 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)
        print("✓ 数据已备份到 data/movies.json")
    
    def close(self):
        """关闭连接"""
        self.mysql_cursor.close()
        self.mysql_conn.close()
        self.mongo_client.close()


if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    crawler = DoubanMovieCrawler()
    try:
        crawler.crawl()
    finally:
        crawler.close()
