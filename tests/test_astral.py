from astral import LocationInfo
from astral.sun import sun
import pytz
from datetime import datetime

def calculate_sunrise_elapsed_time(latitude, longitude, race_date_str, race_time_str):
    # 緯度と経度を浮動小数点数に変換
    latitude = float(latitude)
    longitude = float(longitude)

    # 日付と時間を組み合わせてdatetimeオブジェクトを作成
    race_datetime_str = f"{race_date_str} {race_time_str}"
    race_datetime = datetime.strptime(race_datetime_str, '%Y年%m月%d日 %H:%M')
    race_datetime = pytz.timezone('Asia/Tokyo').localize(race_datetime)

    # 競馬場の位置情報を設定
    location = LocationInfo(latitude=latitude, longitude=longitude)

    # 日の出時刻を計算
    s = sun(location.observer, date=race_datetime.date(), tzinfo=pytz.timezone('Asia/Tokyo'))
    sunrise = s['sunrise']

    # 日の出からの経過時間を計算（分単位）
    elapsed_time = (race_datetime - sunrise).total_seconds() / 60

    return elapsed_time

# 例：札幌の緯度経度と特定の日時を使用
latitude = 43.0152
longitude = 141.4133
race_date_str = "2023年7月22日"
race_time_str = "09:50"

# 日の出からの経過時間を計算
elapsed_time = calculate_sunrise_elapsed_time(latitude, longitude, race_date_str, race_time_str)
print(f"日の出からの経過時間: {elapsed_time} 分")
