"""
数据清洗和质量评估
"""
import json
import os
import pandas as pd
import pymysql
from config import MYSQL_CONFIG


def load_data():
    """从MySQL加载数据"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    df = pd.read_sql("SELECT * FROM movies", conn)
    conn.close()
    return df


def assess_quality(df):
    """数据质量评估"""
    print("\n" + "="*50)
    print("数据质量评估报告")
    print("="*50)
    
    total = len(df)
    print(f"\n1. 数据总量: {total} 条")
    
    print("\n2. 缺失值分析:")
    for col in df.columns:
        null_count = df[col].isnull().sum()
        empty_count = (df[col] == '').sum() if df[col].dtype == 'object' else 0
        missing = null_count + empty_count
        if missing > 0:
            print(f"   - {col}: {missing} ({missing/total*100:.2f}%)")
    
    print("\n3. 重复值分析:")
    dup_movies = df['movie_id'].duplicated().sum()
    print(f"   - 重复电影: {dup_movies} 条")
    
    print("\n4. 数据完整性:")
    complete = df[['title', 'score', 'regions', 'types']].dropna().shape[0]
    print(f"   - 核心字段完整: {complete} ({complete/total*100:.2f}%)")
    
    print("\n5. 数据范围检查:")
    print(f"   - 评分范围: {df['score'].min()} - {df['score'].max()}")
    print(f"   - 评价人数范围: {df['vote_count'].min()} - {df['vote_count'].max()}")
    print(f"   - 类型数量: {df['category'].nunique()}")
    
    return {'total': total, 'complete': complete, 'duplicates': dup_movies}


def clean_data(df):
    """数据清洗"""
    print("\n" + "="*50)
    print("数据清洗")
    print("="*50)
    
    original_count = len(df)
    
    df = df.drop_duplicates(subset=['movie_id'], keep='first')
    print(f"1. 去重后: {len(df)} 条 (删除 {original_count - len(df)} 条)")
    
    df['title'] = df['title'].fillna('未知电影')
    df['actors'] = df['actors'].fillna('')
    df['regions'] = df['regions'].fillna('未知')
    df['types'] = df['types'].fillna('未知')
    print("2. 已填充缺失值")
    
    df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
    df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce').fillna(0).astype(int)
    print("3. 已转换数据类型")
    
    df = df[df['score'] >= 0]
    df = df[df['score'] <= 10]
    print(f"4. 清理异常值后: {len(df)} 条")
    
    df['main_region'] = df['regions'].apply(lambda x: x.split('/')[0] if x else '未知')
    df['main_type'] = df['types'].apply(lambda x: x.split('/')[0] if x else '未知')
    df['is_high_rating'] = df['score'] >= 8.5
    print("5. 已添加衍生字段")
    
    return df


def save_cleaned_data(df):
    """保存清洗后的数据"""
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/movies_cleaned.csv', index=False, encoding='utf-8-sig')
    print("\n✓ 清洗后数据已保存到 data/movies_cleaned.csv")
    
    df.to_json('data/movies_cleaned.json', orient='records', force_ascii=False, indent=2)
    print("✓ 清洗后数据已保存到 data/movies_cleaned.json")


def main():
    print("开始数据清洗和质量评估...")
    df = load_data()
    assess_quality(df)
    df_cleaned = clean_data(df)
    save_cleaned_data(df_cleaned)
    print("\n" + "="*50)
    print("数据清洗完成！")
    print("="*50)


if __name__ == '__main__':
    main()
