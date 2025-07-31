import argparse
from preprocessing import process as preprocessing_process
from feature_select import run_feature_selection
from conversion_analysis import main as conversion_analysis_main

def execute_pipeline(data_name):
    # 設定中介檔名
    paths_output = f"{data_name}_paths"
    classification_output = f"{data_name}_conversion"
    feature_output = f"{data_name}_top5_features"

    # Step 1: 預處理
    print(f"\n [Step 1] 預處理中：從 data/{data_name}.csv 輸出至 outputs/{paths_output}.csv")
    preprocessing_process(data_name, paths_output)

    # Step 2: 特徵選擇 + 建模 + Top 5
    print(f"\n [Step 2] 特徵選擇與建模中：從 outputs/{paths_output}.csv 產出")
    run_feature_selection(paths_output, classification_output, feature_output)

    # Step 3: 畫圖分析
    print(f"\n [Step 3] 多次點擊與轉換分析圖：使用 {paths_output}, {classification_output}, {feature_output}")
    conversion_analysis_main(paths_output, classification_output, feature_output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='data 資料夾內的原始 CSV 檔案（不含 .csv）')
    args = parser.parse_args()

    execute_pipeline(args.data)


# python execute.py --data=example
