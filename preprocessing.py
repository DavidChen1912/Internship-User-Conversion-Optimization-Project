import pandas as pd
import argparse
import os

def label_cosme_dataframe(data):
    # 補上欄位名稱
    data.columns = ['UID', 'Time', 'URL']

    # 刪除「完全等於」官網網址的 row
    data = data[data['URL'] != 'https://www.cosme.net.tw/']

    # 29 個標籤，長的優先
    tags = [
        'write-review-please', 'from=write', 'beauty-ranking-tour', 'discount_messages',
        'brand-events', 'brand_gift', 'coupons', 'events', 'offers', 'activities',
        'beauty-awards', 'beautynews', 'new-products', 'new-reviews', 'ranking', 'news',
        'channel=offline', 'channel=online', 'sell-channels', 'channel_details',
        'category_list', 'categories', 'products', 'brands', 'series', 'tags', 'goodbuy',
        'vip', 'reviews'
    ]
    tags.sort(key=lambda x: -len(x))  # 長字優先

    # 建立 label
    labels = []
    for url in data['URL']:
        parts = str(url).strip('/').split('/')
        last_two_parts = parts[-2:] if len(parts) >= 2 else parts[-1:]

        found = None
        for tag in tags:
            if any(tag == part for part in last_two_parts):
                found = tag
                break
        labels.append(found)

    data['label'] = labels
    return data


def build_user_path_by_date(data: pd.DataFrame) -> pd.DataFrame:
    """
    將每個 UID 每一天的 label 瀏覽紀錄合併為一條 path。
    """
    data = data.drop(columns=['URL'])
    data['Time'] = pd.to_datetime(data['Time'])
    data['Date'] = data['Time'].dt.date  # datetime.date 物件

    path_df = (
        data.sort_values(by=['UID', 'Time'])
            .groupby(['UID', 'Date'])
            .agg({
                'label': lambda x: list(x)
            })
            .reset_index()
            .rename(columns={'label': 'Path'})
    )
    return path_df


def process(data_name: str, output_name: str):
    input_path = os.path.join('data', f'{data_name}.csv')
    output_path = os.path.join('outputs', f'{output_name}.csv')

    data = pd.read_csv(input_path)
    new_data = label_cosme_dataframe(data)
    new_data = new_data[~new_data['label'].isna()]
    new_data = new_data.reset_index(drop=True)

    paths = build_user_path_by_date(new_data)
    paths.to_csv(output_path, index=False)
    print(f"完成！輸出檔案：{output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="data 資料夾內的 CSV 檔名（不含 .csv）")
    parser.add_argument("--output", type=str, required=True, help="輸出 CSV 檔名（不含 .csv）")

    args = parser.parse_args()
    process(args.data, args.output)

# python preprocessing.py --data=example --output=paths
