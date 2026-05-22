import subprocess
import sys
import importlib

# 自动安装缺少的包
required_packages = ["matplotlib", "pandas", "openpyxl", "numpy"]
for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"📦 正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])

# ========== 下面是原来的代码 ==========
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# ... 后面保持不变 ...
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# ========== 设置中文字体 ==========
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC']
matplotlib.rcParams['axes.unicode_minus'] = False

# ========== 读取数据 ==========
df = pd.read_excel("重庆大学周边餐厅数据.xlsx")
print(f"📊 共加载 {len(df)} 家餐厅数据\n")

# ========== 数据清洗 ==========
# 评分转为数值
df['评分'] = pd.to_numeric(df['评分'], errors='coerce')
# 人均价格转为数值
df['人均价格'] = pd.to_numeric(df['人均价格'], errors='coerce')
# 距离转为数值
df['距学校距离(米)'] = pd.to_numeric(df['距学校距离(米)'], errors='coerce')

# ============================================================
# 图1：评分分布直方图
# ============================================================
plt.figure(figsize=(10, 6))
rating_data = df['评分'].dropna()
plt.hist(rating_data, bins=8, color='#FF6B6B', edgecolor='white', alpha=0.8)
plt.title('🎯 重庆大学周边餐厅评分分布', fontsize=16, fontweight='bold')
plt.xlabel('评分', fontsize=12)
plt.ylabel('餐厅数量', fontsize=12)
plt.xticks([1, 2, 3, 4, 5])
plt.grid(axis='y', alpha=0.3)

# 标注平均值
avg_rating = rating_data.mean()
plt.axvline(avg_rating, color='#2D3436', linestyle='--', linewidth=2, label=f'平均评分: {avg_rating:.2f}')
plt.legend(fontsize=11)

# 在柱子上标数字
counts, bins, patches = plt.hist(rating_data, bins=8, color='#FF6B6B', edgecolor='white', alpha=0.8)
for count, bin_edge in zip(counts, bins):
    if count > 0:
        plt.text(bin_edge + 0.15, count + 0.5, int(count), ha='center', fontsize=10)
plt.clf()  # 清除刚才的重复绘图

# 重新画（更干净的方式）
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(rating_data, bins=8, color='#FF6B6B', edgecolor='white', alpha=0.8)
for i, (count, bin_edge) in enumerate(zip(n, bins)):
    if count > 0:
        plt.text(bin_edge + (bins[1]-bins[0])/2, count + 0.3, int(count),
                 ha='center', fontsize=10, fontweight='bold')
plt.axvline(avg_rating, color='#2D3436', linestyle='--', linewidth=2, label=f'平均评分: {avg_rating:.2f}')
plt.title('🎯 重庆大学周边餐厅评分分布', fontsize=16, fontweight='bold')
plt.xlabel('评分', fontsize=12)
plt.ylabel('餐厅数量', fontsize=12)
plt.xticks([1, 2, 3, 4, 5])
plt.grid(axis='y', alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('图1_评分分布图.png', dpi=200, bbox_inches='tight')
plt.show()
print("✅ 图1 已生成：评分分布图.png")

# ============================================================
# 图2：人均价格 TOP15
# ============================================================
plt.figure(figsize=(12, 7))
price_data = df.dropna(subset=['人均价格'])
top15 = price_data.nlargest(15, '人均价格')

colors = plt.cm.Reds(np.linspace(0.3, 0.9, 15))
bars = plt.barh(range(len(top15)), top15['人均价格'].values, color=colors, edgecolor='white')
plt.yticks(range(len(top15)), top15['名称'].values, fontsize=10)
plt.xlabel('人均价格（元）', fontsize=12)
plt.title('💰 重大周边人均价格 TOP15 餐厅', fontsize=16, fontweight='bold')
plt.gca().invert_yaxis()

# 在条形上标价格
for i, (bar, price) in enumerate(zip(bars, top15['人均价格'].values)):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             f'{int(price)}元', va='center', fontsize=10, fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('图2_价格TOP15.png', dpi=200, bbox_inches='tight')
plt.show()
print("✅ 图2 已生成：价格TOP15.png")

# ============================================================
# 图3：餐厅类型分布饼图
# ============================================================
plt.figure(figsize=(9, 9))

# 从标签字段提取类型
def extract_type(tag):
    if pd.isna(tag):
        return '其他'
    parts = str(tag).split(';')
    return parts[-1] if len(parts) >= 2 else parts[0]

df['类型'] = df['标签'].apply(extract_type)
type_counts = df['类型'].value_counts()

# 颜色方案
color_map = {
    '中餐厅': '#FF6B6B',
    '小吃快餐店': '#FFD93D',
    '外国餐厅': '#6BCB77',
    '其他': '#4D96FF'
}
pie_colors = [color_map.get(t, '#95A5A6') for t in type_counts.index]

wedges, texts, autotexts = plt.pie(
    type_counts.values,
    labels=type_counts.index,
    autopct='%1.1f%%',
    colors=pie_colors,
    startangle=90,
    textprops={'fontsize': 12},
    pctdistance=0.75,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)

# 加图例（含数量）
legend_labels = [f'{k}  ({v}家)' for k, v in zip(type_counts.index, type_counts.values)]
plt.legend(wedges, legend_labels, title="餐厅类型", loc="lower right", fontsize=11)
plt.title('🏷️ 重大周边餐厅类型分布', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('图3_餐厅类型分布.png', dpi=200, bbox_inches='tight')
plt.show()
print("✅ 图3 已生成：餐厅类型分布.png")

# ============================================================
# 图4：评分 vs 价格 散点图（含距离气泡）
# ============================================================
plt.figure(figsize=(12, 8))

scatter_data = df.dropna(subset=['评分', '人均价格', '距学校距离(米)'])

# 气泡大小 = 距离映射（越远气泡越大，取倒数让近的更大？这里用距离本身）
bubble_size = scatter_data['距学校距离(米)'] / 20  # 缩放

scatter = plt.scatter(
    scatter_data['人均价格'],
    scatter_data['评分'],
    s=bubble_size,
    c=scatter_data['距学校距离(米)'],
    cmap='RdYlGn_r',
    alpha=0.7,
    edgecolors='white',
    linewidth=0.5
)

# 标注几个特别值得关注的店
highlight = scatter_data[
    (scatter_data['评分'] >= 4.5) & (scatter_data['人均价格'] <= 30)
]
for _, row in highlight.iterrows():
    plt.annotate(
        row['名称'],
        (row['人均价格'], row['评分']),
        xytext=(8, 8),
        textcoords='offset points',
        fontsize=9,
        fontweight='bold',
        color='#2D3436',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7)
    )

plt.colorbar(scatter, label='距学校距离（米）')
plt.xlabel('人均价格（元）', fontsize=12)
plt.ylabel('评分', fontsize=12)
plt.title('📍 评分 vs 人均价格（气泡大小 = 距离学校远近）', fontsize=16, fontweight='bold')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('图4_评分价格散点图.png', dpi=200, bbox_inches='tight')
plt.show()
print("✅ 图4 已生成：评分价格散点图.png")

# ============================================================
# 图5：距离分布直方图
# ============================================================
plt.figure(figsize=(10, 6))
dist_data = df['距学校距离(米)'].dropna()
plt.hist(dist_data, bins=15, color='#6C5CE7', edgecolor='white', alpha=0.8)
plt.title('📏 餐厅距离学校距离分布', fontsize=16, fontweight='bold')
plt.xlabel('距离（米）', fontsize=12)
plt.ylabel('餐厅数量', fontsize=12)
plt.grid(axis='y', alpha=0.3)

# 标注平均距离
avg_dist = dist_data.mean()
plt.axvline(avg_dist, color='#E17055', linestyle='--', linewidth=2, label=f'平均距离: {avg_dist:.0f}米')
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('图5_距离分布图.png', dpi=200, bbox_inches='tight')
plt.show()
print("✅ 图5 已生成：距离分布图.png")

# ============================================================
# 输出统计摘要
# ============================================================
print("\n" + "=" * 50)
print("📋 数据统计摘要")
print("=" * 50)
print(f"🏪 餐厅总数：{len(df)} 家")
print(f"⭐ 平均评分：{avg_rating:.2f} 分（满分5分）")
print(f"💰 平均人均价格：{df['人均价格'].mean():.0f} 元")
print(f"  最贵：{df.loc[df['人均价格'].idxmax(), '名称']}（{int(df['人均价格'].max())}元）")
print(f"  最便宜：{df.loc[df['人均价格'].idxmin(), '名称']}（{int(df['人均价格'].min())}元）")
print(f"📏 平均距学校距离：{avg_dist:.0f} 米")
print(f"🏷️ 餐厅类型：中餐厅 {type_counts.get('中餐厅', 0)} 家 | 小吃快餐 {type_counts.get('小吃快餐店', 0)} 家")
print("=" * 50)
print("\n🎉 全部图表已生成！共 5 张图 ✅")
