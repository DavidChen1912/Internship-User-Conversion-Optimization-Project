import pandas as pd
import plotly.graph_objects as go
import argparse
import os

def merge_by_order(paths: pd.DataFrame, conversion: pd.DataFrame) -> pd.DataFrame:
    """
    根據行數對齊 paths 與 conversion，直接水平拼接，不使用 UID 合併。
    假設 paths 與 conversion 的順序一一對應。
    """
    assert len(paths) == len(conversion), "兩份資料筆數不相等，無法直接拼接！"

    merged = pd.concat([
        paths[['UID', 'Path']],
        conversion[['y']]
    ], axis=1)

    return merged


def plot_conversion_rate_percent_labels(merged_data: pd.DataFrame, feature_df: pd.DataFrame, max_count: int = 8):
    """
    繪製每個特徵出現次數與轉換率的折線圖，並在圖上標示百分比 (%)
    使用 dropdown 選單切換觀察的特徵。
    """
    feature_list = feature_df['feature'].tolist()
    all_data = []

    for feat in feature_list:
        for count in range(0, max_count + 1):
            match = merged_data['Path'].apply(lambda x: x.count(feat) == count)
            total = match.sum()
            y1 = merged_data[match]['y'].sum()
            rate = (y1 / total) * 100 if total > 0 else 0
            all_data.append({
                'feature': feat,
                'count': count,
                'conversion_rate': rate,
                'sample_size': total
            })

    df = pd.DataFrame(all_data)

    fig = go.Figure()
    for i, feat in enumerate(feature_list):
        sub = df[df['feature'] == feat]
        fig.add_trace(go.Scatter(
            x=sub['count'],
            y=sub['conversion_rate'],
            mode='lines+markers+text',
            name=feat,
            text=[f"{r:.1f}%" for r in sub['conversion_rate']],
            textposition='top center',
            visible=(i == 0)
        ))

    buttons = []
    for i, feat in enumerate(feature_list):
        visibility = [False] * len(feature_list)
        visibility[i] = True
        buttons.append(dict(
            label=feat,
            method="update",
            args=[
                {"visible": visibility},
                {"title": f"Conversion Rate vs Click Count for '{feat}'"}
            ]
        ))

    fig.update_layout(
        title=f"Conversion Rate vs Click Count for '{feature_list[0]}'",
        xaxis_title="Click Count (Number of Times Feature Appears in Path)",
        yaxis_title="Conversion Rate (%)",
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.05,
            y=1.15,
            xanchor="left",
            yanchor="top"
        )],
        showlegend=False
    )

    return df, fig


def main(paths_data_name, classification_data_name, feature_data_name):
    feature = pd.read_csv(os.path.join("outputs", f"{feature_data_name}.csv"))
    paths = pd.read_csv(os.path.join("outputs", f"{paths_data_name}.csv"))
    conversion = pd.read_csv(os.path.join("outputs", f"{classification_data_name}.csv"))

    merged_data = merge_by_order(paths, conversion)
    df_summary, fig = plot_conversion_rate_percent_labels(merged_data, feature)
    fig.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--paths_data_name', required=True, help='paths資料集檔名（不含.csv）')
    parser.add_argument('--classification_data_name', required=True, help='轉換標記檔名（不含.csv）')
    parser.add_argument('--feature_data_name', required=True, help='特徵檔案名稱（不含.csv）')
    args = parser.parse_args()

    main(args.paths_data_name, args.classification_data_name, args.feature_data_name)

# python conversion_analysis.py --paths_data_name=paths --classification_data_name=conversion --feature_data_name=top5_features
