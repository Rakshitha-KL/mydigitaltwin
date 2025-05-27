import pandas as pd
import os
from datetime import datetime
def scan_directory(path):
    file_info = []
    if not os.path.exists(path):
        raise FileNotFoundError("Directory not found.")

    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                stats = os.stat(file_path)
                file_info.append({
                    'File Name': file,
                    'Size (KB)': round(stats.st_size / 1024, 2),
                    'Type': os.path.splitext(file)[1],
                    'Modified Time': datetime.fromtimestamp(stats.st_mtime),
                    'Path': file_path
                })
            except Exception as e:
                print(f"Error reading {file}: {e}")

    return pd.DataFrame(file_info)

def save_to_csv(df, filename='data/logs.csv'):
    df.to_csv(filename, index=False)
    print(f"Report saved to {filename}")