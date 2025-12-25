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
    return pd.read_csv('data/movies_cleaned.csv')


def plot_score_distribution(df):
    plt.figure(figsize=(10, 6))
    scores = df['score']
    plt.hist(scores, bins=20, color='coral', edgecolor='white', alpha=0.7)
    plt.axvline(scores.mean(), color='red', linestyle='--', label=f'平均: {scores.mean():.2f}')
    plt.xlabel('评分')
    plt.ylabel('电影数量')
    plt.title('豆瓣电影评分分布')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/score_distribution.png', dpi=150)
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/score_distribution.png")


def plot_category_distribution(df):
    plt.figure(figsize=(12, 6))
    cat_counts = df['category'].value_counts()
    colors = plt.cm.Set3(range(len(cat_counts)))
    bars = plt.bar(range(len(cat_counts)), cat_counts.values, color=colors)
    plt.xticks(range(len(cat_counts)), cat_counts.index, rotation=45, ha='right')
    plt.xlabel('电影类型')
    plt.ylabel('数量')
    plt.title('各类型电影数量分布')
    for bar, count in zip(bars, cat_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                str(count), ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/category_distribution.png', dpi=150)
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/category_distribution.png")


def plot_region_distribution(df):
    plt.figure(figsize=(12, 6))
    region_counts = df['main_region'].value_counts().head(10)
    colors = plt.cm.Pastel1(range(len(region_counts)))
    bars = plt.bar(range(len(region_counts)), region_counts.values, color=colors)
    plt.xticks(range(len(region_counts)), region_counts.index, rotation=45, ha='right')
    plt.xlabel('国家/地区')
    plt.ylabel('数量')
    plt.title('电影地区分布 (Top 10)')
    for bar, count in zip(bars, region_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                str(count), ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/region_distribution.png', dpi=150)
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/region_distribution.png")


def plot_score_by_category(df):
    plt.figure(figsize=(12, 6))
    avg_score = df.groupby('category')['score'].mean().sort_values(ascending=False)
    colors = plt.cm.viridis(range(0, 256, int(256/len(avg_score))))
    bars = plt.bar(range(len(avg_score)), avg_score.values, color=colors)
    plt.xticks(range(len(avg_score)), avg_score.index, rotation=45, ha='right')
    plt.xlabel('电影类型')
    plt.ylabel('平均评分')
    plt.title('各类型电影平均评分')
    for bar, val in zip(bars, avg_score.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.2f}', ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/score_by_category.png', dpi=150)
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/score_by_category.png")


def plot_top_movies(df, top_n=15):
    plt.figure(figsize=(12, 8))
    top = df.nlargest(top_n, 'score')[['title', 'score', 'category']]
    colors = plt.cm.RdYlGn(range(50, 250, int(200/top_n)))[::-1]
    bars = plt.barh(range(len(top)), top['score'].values, color=colors)
    labels = [f"{row['title'][:15]} ({row['category']})" for _, row in top.iterrows()]
    plt.yticks(range(len(top)), labels)
    plt.xlabel('评分')
    plt.title(f'评分最高的{top_n}部电影')
    plt.xlim(8.5, 10)
    for bar, score in zip(bars, top['score'].values):
        plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{score:.1f}', ha='left', va='center', fontsize=9)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/top_movies.png', dpi=150)
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/top_movies.png")


def plot_votes_vs_score(df):
    plt.figure(figsize=(10, 8))
    plt.scatter(df['vote_count'] / 10000, df['score'], alpha=0.5, c='steelblue', s=30)
    plt.xlabel('评价人数 (万)')
    plt.ylabel('评分')
    plt.title('电影评分与评价人数关系')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/votes_vs_score.png', dpi=150)
    plt.close()
    print(f"✓ 已生成 {OUTPUT_DIR}/votes_vs_score.png")


def generate_stats(df):
    print("\n" + "="*50)
    print("数据统计摘要")
    print("="*50)
    print(f"  电影总数: {len(df)}")
    print(f"  平均评分: {df['score'].mean():.2f}")
    print(f"  类型数量: {df['category'].nunique()}")
    print(f"  地区数量: {df['main_region'].nunique()}")


def main():
    print("开始生成可视化图表...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()
    generate_stats(df)
    print("\n生成图表中...")
    plot_score_distribution(df)
    plot_category_distribution(df)
    plot_region_distribution(df)
    plot_score_by_category(df)
    plot_top_movies(df)
    plot_votes_vs_score(df)
    print("\n" + "="*50)
    print("可视化完成！")
    print("="*50)


if __name__ == '__main__':
    main()
