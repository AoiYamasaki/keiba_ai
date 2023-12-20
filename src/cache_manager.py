import json
import os

def save_to_cache(race_id, data, cache_file='cache/race_data_cache.json'):
    """キャッシュにデータを保存する"""
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            cache = json.load(file)
    else:
        cache = {}

    cache[race_id] = data

    with open(cache_file, 'w') as file:
        json.dump(cache, file)

    print(f"Saved to cache: {race_id}")

def load_from_cache(race_id, cache_file='cache/race_data_cache.json'):
    """キャッシュからデータを読み込む"""
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            cache = json.load(file)
            return cache.get(race_id)
    return None
