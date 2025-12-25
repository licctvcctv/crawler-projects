"""
数据可视化分析
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
import os
import warnings
warnings.filterwarnings('ignore')

matplotlib.rcParams['font.sans-serif'] = ['Heiti SC', 'STHeiti', 'PingFang SC', 'Hiragino Sans GB', 'Arial Unicode MS']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = 'output'


def load_data():
    return pd.read_csv('data/songs_cleaned.csv')


def plot_playlist_distribution(df):
    plt.figure(figsize=(12, 6))
    playlist_counts = df['playlist_name'].value_counts()
    colors = plt.cm.Set3(range(len(playlist_counts)))
    bars = plt.bar(range(len(playlist_counts)), playlist_counts.values, color=colors)
    plt.xticks(range(len(playlist_counts)), playlist_counts.index, rotation=45, ha='right')
    plt.xlabel('榜单名称')
    plt.ylabel('歌曲数量')
    plt.title('各榜单歌曲数量分布')
    for bar, count in zip(bars, playlist_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                str(count), ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/playlist_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/playlist_distribution.png")


def plot_duration_distribution(df):
    plt.figure(figsize=(10, 6))
    durations = df['duration_min'].dropna()
    plt.hist(durations, bins=30, color='steelblue', edgecolor='white', alpha=0.7)
    plt.axvline(durations.mean(), color='red', linestyle='--', label=f'平均: {durations.mean():.2f}分钟')
    plt.axvline(durations.median(), color='orange', linestyle='--', label=f'中位数: {durations.median():.2f}分钟')
    plt.xlabel('时长 (分钟)')
    plt.ylabel('歌曲数量')
    plt.title('歌曲时长分布')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/duration_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/duration_distribution.png")


def plot_top_artists(df, top_n=15):
    plt.figure(figsize=(12, 8))
    artist_counts = df['artist_name'].value_counts().head(top_n)
    colors = plt.cm.Blues(range(50, 250, int(200/top_n)))[::-1]
    bars = plt.barh(range(len(artist_counts)), artist_counts.values, color=colors)
    plt.yticks(range(len(artist_counts)), artist_counts.index)
    plt.xlabel('上榜歌曲数')
    plt.ylabel('歌手')
    plt.title(f'Top {top_n} 热门歌手 (按上榜歌曲数)')
    for bar, count in zip(bars, artist_counts.values):
        plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
                str(count), ha='left', va='center', fontsize=9)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/top_artists.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/top_artists.png")


def plot_duration_by_playlist(df):
    plt.figure(figsize=(12, 6))
    avg_duration = df.groupby('playlist_name')['duration_min'].mean().sort_values(ascending=False)
    colors = plt.cm.Pastel1(range(len(avg_duration)))
    bars = plt.bar(range(len(avg_duration)), avg_duration.values, color=colors)
    plt.xticks(range(len(avg_duration)), avg_duration.index, rotation=45, ha='right')
    plt.xlabel('榜单名称')
    plt.ylabel('平均时长 (分钟)')
    plt.title('各榜单歌曲平均时长对比')
    for bar, val in zip(bars, avg_duration.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                f'{val:.1f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/duration_by_playlist.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/duration_by_playlist.png")


def plot_pie_chart(df):
    plt.figure(figsize=(10, 10))
    playlist_counts = df['playlist_name'].value_counts()
    colors = plt.cm.Set3(range(len(playlist_counts)))
    explode = [0.02] * len(playlist_counts)
    plt.pie(playlist_counts.values, labels=playlist_counts.index, autopct='%1.1f%%',
            colors=colors, explode=explode, shadow=True, startangle=90)
    plt.title('各榜单歌曲占比')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/playlist_pie.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/playlist_pie.png")


def generate_stats_summary(df):
    summary = {
        '总歌曲数': len(df),
        '唯一歌曲数': df['song_id'].nunique(),
        '歌手数量': df['artist_id'].nunique(),
        '榜单数量': df['playlist_id'].nunique(),
        '平均时长(分钟)': round(df['duration_min'].mean(), 2),
        '最长歌曲时长(分钟)': round(df['duration_min'].max(), 2),
        '最短歌曲时长(分钟)': round(df['duration_min'].min(), 2),
    }
    print("\n" + "="*50)
    print("数据统计摘要")
    print("="*50)
    for key, value in summary.items():
        print(f"  {key}: {value}")
    return summary


def main():
    print("开始生成可视化图表...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()
    generate_stats_summary(df)
    print("\n生成图表中...")
    plot_playlist_distribution(df)
    plot_duration_distribution(df)
    plot_top_artists(df)
    plot_duration_by_playlist(df)
    plot_pie_chart(df)
    print("\n" + "="*50)
    print(f"可视化完成！图表已保存到 {OUTPUT_DIR}/ 目录")
    print("="*50)


if __name__ == '__main__':
    main()
