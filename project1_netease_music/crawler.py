"""
网易云音乐排行榜爬虫
爬取多个排行榜的歌曲数据
"""
import requests
import time
import random
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pymysql
from pymongo import MongoClient
from config import MYSQL_CONFIG, MONGODB_CONFIG, CRAWL_CONFIG, PLAYLIST_IDS


class NeteaseMusicCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.songs = []
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
        CREATE TABLE IF NOT EXISTS songs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            song_id BIGINT UNIQUE,
            song_name VARCHAR(500),
            artist_name VARCHAR(500),
            artist_id BIGINT,
            album_name VARCHAR(500),
            album_id BIGINT,
            duration INT,
            playlist_name VARCHAR(200),
            playlist_id BIGINT,
            rank_num INT,
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
        self.mongo_collection = self.mongo_db[MONGODB_CONFIG['collection']]
        print("✓ MongoDB初始化完成")
    
    def get_headers(self):
        """获取随机请求头"""
        return {
            'User-Agent': self.ua.random,
            'Referer': 'https://music.163.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
    
    def fetch_playlist(self, playlist_id, playlist_name):
        """获取歌单/排行榜歌曲"""
        url = f'https://music.163.com/api/playlist/detail?id={playlist_id}'
        
        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    tracks = data.get('result', {}).get('tracks', [])
                    return tracks
            return []
        except Exception as e:
            print(f"  请求失败: {e}")
            return []
    
    def parse_song(self, song_data, playlist_id, playlist_name, rank):
        """解析歌曲数据"""
        try:
            if isinstance(song_data, dict):
                song_id = song_data.get('id')
                song_name = song_data.get('name', '')
                
                artists = song_data.get('artists', song_data.get('ar', []))
                if artists:
                    artist_name = '/'.join([a.get('name', '') for a in artists])
                    artist_id = artists[0].get('id', 0)
                else:
                    artist_name = ''
                    artist_id = 0
                
                album = song_data.get('album', song_data.get('al', {}))
                album_name = album.get('name', '') if album else ''
                album_id = album.get('id', 0) if album else 0
                
                duration = song_data.get('duration', song_data.get('dt', 0))
                if duration > 1000:
                    duration = duration // 1000
                
                return {
                    'song_id': song_id,
                    'song_name': song_name,
                    'artist_name': artist_name,
                    'artist_id': artist_id,
                    'album_name': album_name,
                    'album_id': album_id,
                    'duration': duration,
                    'playlist_name': playlist_name,
                    'playlist_id': playlist_id,
                    'rank_num': rank,
                }
            return None
        except Exception as e:
            print(f"  解析失败: {e}")
            return None
    
    def save_to_mysql(self, song_data):
        """保存到MySQL"""
        try:
            sql = """
            INSERT IGNORE INTO songs 
            (song_id, song_name, artist_name, artist_id, album_name, album_id, 
             duration, playlist_name, playlist_id, rank_num)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.mysql_cursor.execute(sql, (
                song_data['song_id'],
                song_data['song_name'],
                song_data['artist_name'],
                song_data['artist_id'],
                song_data['album_name'],
                song_data['album_id'],
                song_data['duration'],
                song_data['playlist_name'],
                song_data['playlist_id'],
                song_data['rank_num'],
            ))
            self.mysql_conn.commit()
            return True
        except Exception as e:
            print(f"  MySQL保存失败: {e}")
            return False
    
    def save_to_mongodb(self, song_data):
        """保存到MongoDB"""
        try:
            self.mongo_collection.update_one(
                {'song_id': song_data['song_id']},
                {'$set': song_data},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"  MongoDB保存失败: {e}")
            return False
    
    def crawl(self):
        """执行爬取"""
        print("\n" + "="*50)
        print("网易云音乐排行榜爬虫")
        print("="*50)
        
        total_count = 0
        max_songs = CRAWL_CONFIG['max_songs']
        
        for playlist in PLAYLIST_IDS:
            if total_count >= max_songs:
                break
            
            playlist_id = playlist['id']
            playlist_name = playlist['name']
            print(f"\n正在爬取: {playlist_name} (ID: {playlist_id})")
            
            songs_data = self.fetch_playlist(playlist_id, playlist_name)
            
            if not songs_data:
                print(f"  {playlist_name} 获取失败，跳过")
                continue
            
            playlist_count = 0
            for rank, song in enumerate(songs_data, 1):
                if total_count >= max_songs:
                    break
                
                parsed = self.parse_song(song, playlist_id, playlist_name, rank)
                if parsed and parsed['song_id']:
                    self.save_to_mysql(parsed)
                    self.save_to_mongodb(parsed)
                    self.songs.append(parsed)
                    total_count += 1
                    playlist_count += 1
            
            print(f"  已爬取 {playlist_count} 首歌曲")
            
            delay = random.uniform(
                CRAWL_CONFIG['delay_min'], 
                CRAWL_CONFIG['delay_max']
            )
            time.sleep(delay)
        
        print(f"\n{'='*50}")
        print(f"爬取完成！共获取 {total_count} 首歌曲")
        print(f"数据已保存到 MySQL 和 MongoDB")
        print(f"{'='*50}")
        
        self.save_to_json()
        return total_count
    
    def save_to_json(self):
        """保存到JSON文件"""
        with open('data/songs.json', 'w', encoding='utf-8') as f:
            json.dump(self.songs, f, ensure_ascii=False, indent=2)
        print("✓ 数据已备份到 data/songs.json")
    
    def close(self):
        """关闭连接"""
        self.mysql_cursor.close()
        self.mysql_conn.close()
        self.mongo_client.close()


if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    crawler = NeteaseMusicCrawler()
    try:
        crawler.crawl()
    finally:
        crawler.close()
