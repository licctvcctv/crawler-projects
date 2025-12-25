"""
数据清洗和质量评估
"""
import json
import pandas as pd
import pymysql
from config import MYSQL_CONFIG


def load_data():
    """从MySQL加载数据"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    df = pd.read_sql("SELECT * FROM songs", conn)
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
    dup_songs = df['song_id'].duplicated().sum()
    print(f"   - 重复歌曲ID: {dup_songs} 条")
    
    print("\n4. 数据完整性:")
    complete = df.dropna().shape[0]
    print(f"   - 完整记录: {complete} ({complete/total*100:.2f}%)")
    
    print("\n5. 字段统计:")
    print(f"   - 歌曲数量: {df['song_id'].nunique()}")
    print(f"   - 歌手数量: {df['artist_id'].nunique()}")
    print(f"   - 榜单数量: {df['playlist_id'].nunique()}")
    
    return {'total': total, 'complete': complete, 'duplicates': dup_songs}


def clean_data(df):
    """数据清洗"""
    print("\n" + "="*50)
    print("数据清洗")
    print("="*50)
    
    original_count = len(df)
    
    df = df.drop_duplicates(subset=['song_id'], keep='first')
    print(f"1. 去重后: {len(df)} 条 (删除 {original_count - len(df)} 条)")
    
    df['song_name'] = df['song_name'].fillna('未知歌曲')
    df['artist_name'] = df['artist_name'].fillna('未知歌手')
    df['album_name'] = df['album_name'].fillna('未知专辑')
    print("2. 已填充缺失值")
    
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0).astype(int)
    print("3. 已转换数据类型")
    
    df = df[df['duration'] >= 0]
    df = df[df['duration'] <= 3600]
    print(f"4. 清理异常值后: {len(df)} 条")
    
    df['duration_min'] = (df['duration'] / 60).round(2)
    print("5. 已添加衍生字段")
    
    return df


def save_cleaned_data(df):
    """保存清洗后的数据"""
    import os
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/songs_cleaned.csv', index=False, encoding='utf-8-sig')
    print("\n✓ 清洗后数据已保存到 data/songs_cleaned.csv")
    
    df.to_json('data/songs_cleaned.json', orient='records', force_ascii=False, indent=2)
    print("✓ 清洗后数据已保存到 data/songs_cleaned.json")


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
