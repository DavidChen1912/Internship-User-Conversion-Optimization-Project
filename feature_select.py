import numpy as np
import pandas as pd
import os
import argparse

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    classification_report,
    precision_score, recall_score, f1_score
)
import matplotlib.pyplot as plt

def transform_paths_to_feature_table(paths):
    # 保留 UID、Path，刪除 Time
    paths = paths[['UID', 'Path']].copy()

    # 特徵欄位（25個）
    features = [
        'write-review-please', 'from=write', 'beauty-ranking-tour', 'discount_messages',
        'brand-events', 'brand_gift', 'coupons', 'events', 'offers', 'activities',
        'beauty-awards', 'beautynews', 'new-products', 'new-reviews', 'ranking', 'news',
        'category_list', 'categories', 'products', 'brands', 'series', 'tags', 'goodbuy', 'vip', 'reviews'
    ]

    # 與購買意圖有關的標籤（只用來決定 y）
    purchase_tags = ['channel=offline', 'channel=online', 'sell-channels', 'channel_details']

    # 初始化結果表
    result = pd.DataFrame()
    result['UID'] = paths['UID']

    # 為每個特徵欄位統計出現次數
    for feat in features:
        result[feat] = paths['Path'].apply(lambda lst: lst.count(feat))

    # y：只要出現任一購買意圖標籤就設為 1，否則 0
    result['y'] = paths['Path'].apply(
        lambda lst: int(any(tag in lst for tag in purchase_tags))
    )

    return result


def run_feature_selection(data_file, classification_data_name, feature_data_name):
    # 讀取資料
    paths = pd.read_csv(os.path.join('outputs', f'{data_file}.csv'))

    # 特徵轉換
    data = transform_paths_to_feature_table(paths)
    data.to_csv(os.path.join('outputs', f'{classification_data_name}.csv'), index=False)

    # 1. 拆 X 和 y（去掉 UID）
    X = data.drop(columns=['UID', 'y'])
    y = data['y']

    # 2. 分訓練集 & 測試集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)

    # 設定要嘗試的參數組合
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20],
        'min_samples_leaf': [1, 10]
    }

    # 設定 GridSearchCV（5-fold CV）
    grid = GridSearchCV(
        estimator=RandomForestClassifier(random_state=11),
        param_grid=param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )

    # 執行參數搜尋
    grid.fit(X_train, y_train)

    # 印出最佳參數與交叉驗證分數
    print("最佳參數組合：", grid.best_params_)
    print("最佳交叉驗證分數：", grid.best_score_)

    # 用最佳參數重新訓練模型
    best_model = grid.best_estimator_
    best_model.fit(X_train, y_train)

    # 預測測試集
    y_pred = best_model.predict(X_test)

    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')

    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1:.4f}")

    # 抓出特徵重要性
    feature_importance = pd.Series(best_model.feature_importances_, index=X.columns)
    top5_features = feature_importance.sort_values(ascending=False).head(5)

    print("\n Top 5 Most Important Features:")
    print(top5_features)

    # 儲存成 CSV 檔
    top5_df = top5_features.reset_index()
    top5_df.columns = ['feature', 'importance']
    top5_df.to_csv(os.path.join('outputs', f'{feature_data_name}.csv'), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='輸入檔名（outputs 資料夾內，去掉 .csv）')
    parser.add_argument('--classification_data_name', required=True, help='轉換後資料表名稱（將存入 outputs/*.csv）')
    parser.add_argument('--feature_data_name', required=True, help='特徵重要性輸出名稱（將存入 outputs/*.csv）')
    args = parser.parse_args()

    run_feature_selection(args.data, args.classification_data_name, args.feature_data_name)

# python feature_select.py --data=paths --classification_data_name=conversion --feature_data_name=top5_features
