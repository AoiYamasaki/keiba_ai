import sys
import os

# プロジェクトのルートディレクトリを取得し、Pythonの実行パスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from src.data_fetcher import fetch_race_data
from src.config import year_start

def test_fetch_5_races():
    fetch_race_data(year_start, test_mode=True)

if __name__ == "__main__":
    test_fetch_5_races()
