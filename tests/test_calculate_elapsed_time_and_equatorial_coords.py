import pytz
from datetime import datetime
from astral import LocationInfo
from astral.sun import sun

def calculate_elapsed_time_and_equatorial_coords(race_datetime, latitude, longitude):
    # 競馬場の位置情報を設定
    location = LocationInfo(latitude=latitude, longitude=longitude)

    # タイムゾーンを設定
    timezone = pytz.timezone('Asia/Tokyo')
    race_datetime = race_datetime.replace(tzinfo=timezone)

    # 日の出時刻を計算
    s = sun(location.observer, date=race_datetime.date(), tzinfo=timezone)
    sunrise = s['sunrise']

    # 日の出からの経過時間を計算
    elapsed_time = (race_datetime - sunrise).total_seconds() / 60

    # 東の地平線の赤道座標を計算（仮の計算）
    equatorial_ra = longitude
    equatorial_dec = 0

    return elapsed_time, (equatorial_ra, equatorial_dec)

# テスト用のデータ
latitude = 33.8709  # 指定された緯度
longitude = 130.8202  # 指定された経度
race_datetime = datetime(2023, 9, 3, 16, 15, 0, tzinfo=pytz.timezone('Asia/Tokyo'))  # 指定された日時

# 関数の実行と結果の出力
try:
    elapsed_time, equatorial_coords = calculate_elapsed_time_and_equatorial_coords(race_datetime, latitude, longitude)
    print(f"Elapsed time: {elapsed_time} minutes")
    print(f"Equatorial coordinates: {equatorial_coords}")
except Exception as e:
    print(f"Error occurred: {e}")
