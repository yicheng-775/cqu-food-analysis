import subprocess
import sys
import importlib

# 自动安装缺少的包
required_packages = ["requests", "pandas", "openpyxl"]
for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 导入依赖
import requests
import time
import pandas as pd

# ==================== 配置区域 ====================
API_KEY = "tFV2Z7eUb0Dy1iXMV64FCarq97JY7v4Z"  # 你的 API Key
CITY = "重庆"
KEYWORD = "餐厅"

# 重庆大学 A 区（沙坪坝老校区）坐标
LAT = 29.5718
LNG = 106.4617
RADIUS = 2000  # 搜索半径（米），2000 = 2公里

# ================================================

def get_pois(lat, lng, radius, keyword, city, page_num=0):
    """调用百度地图 Place API 搜索周边 POI"""
    url = "https://api.map.baidu.com/place/v2/search"
    params = {
        "query": keyword,
        "location": f"{lat},{lng}",
        "radius": radius,
        "output": "json",
        "ak": API_KEY,
        "page_size": 20,
        "page_num": page_num,
        "scope": 2,
        "city": city,
        "coord_type": 1  # 1=GPS坐标(WGS-84), 如果报坐标偏移可改为3(百度坐标)
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()

        if data.get("status") != 0:
            print(f"❌ API 返回错误：{data.get('message')} (状态码 {data.get('status')})")
            return []

        return data.get("results", [])

    except Exception as e:
        print(f"❌ 请求异常：{e}")
        return []


def search_all_restaurants():
    """翻页获取全部餐厅数据"""
    all_results = []
    page = 0

    while True:
        print(f"📄 正在获取第 {page + 1} 页...")
        results = get_pois(LAT, LNG, RADIUS, KEYWORD, CITY, page)

        if not results:
            print("✅ 没有更多数据了")
            break

        for poi in results:
            # 安全获取 detail_info（可能为 None）
            detail = poi.get("detail_info") or {}

            all_results.append({
                "名称": poi.get("name", ""),
                "地址": poi.get("address", ""),
                "评分": detail.get("overall_rating", ""),
                "人均价格": detail.get("price", ""),
                "标签": detail.get("tag", ""),
                "点评数": detail.get("comment_num", ""),
                "营业状态": detail.get("shop_hours") or detail.get("business_hours", ""),
                "纬度": poi.get("location", {}).get("lat", ""),
                "经度": poi.get("location", {}).get("lng", ""),
                "距学校距离(米)": detail.get("distance", ""),
            })

        page += 1

        # 防止无限循环（最多取 10 页 = 200 条）
        if page >= 10:
            break

        time.sleep(0.5)  # 礼貌延时，避免被封

    return all_results


def main():
    print("=" * 50)
    print("🍜 重庆大学周边餐厅数据采集器")
    print(f"📍 坐标：({LAT}, {LNG})，半径：{RADIUS}米")
    print("=" * 50)

    data = search_all_restaurants()

    if not data:
        print("❌ 没有获取到任何数据，请检查 API Key 或网络连接")
        return

    # 转成 DataFrame
    df = pd.DataFrame(data)

    # 打印统计信息
    print(f"\n📊 共获取到 {len(df)} 家餐厅/美食点")
    print(f"⭐ 有评分的数量：{df['评分'].notna().sum()}")
    print(f"💰 有人均价格的数量：{(df['人均价格'].notna() & (df['人均价格'] != '')).sum()}")

    # 保存到 Excel
    filename = "重庆大学周边餐厅数据.xlsx"
    df.to_excel(filename, index=False, engine="openpyxl")
    print(f"\n✅ 数据已保存到：{filename}")

    # 打印前10条预览
    print("\n📋 前10条预览：")
    print(df[["名称", "评分", "人均价格", "地址"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
