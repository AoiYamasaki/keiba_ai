import ephem
from datetime import datetime

def calculate_sunrise_elapsed_time_and_equatorial_coords(latitude, longitude, race_date):
    observer = ephem.Observer()
    observer.lat, observer.lon = str(latitude), str(longitude)
    observer.date = race_date.strftime('%Y/%m/%d')

    sunrise = observer.previous_rising(ephem.Sun(), start=observer.date)
    sunset = observer.next_setting(ephem.Sun(), start=observer.date)

    # 日の出からの経過時間（秒）
    elapsed_time_since_sunrise = (observer.date - sunrise) * 86400  # ephemの日付は日数で表されるため、秒に変換

    # 東の地平線の赤道座標
    observer.horizon = '0'
    sun = ephem.Sun(observer)
    equatorial_coords = (sun.ra, sun.dec)

    return elapsed_time_since_sunrise, equatorial_coords

# 使用例
# latitude, longitude = 35.681236, 139.767125  # 東京駅の緯度経度
# race_date = datetime(2023, 7, 22)
# elapsed_time, equatorial_coords = calculate_sunrise_elapsed_time_and_equatorial_coords(latitude, longitude, race_date)
# print(elapsed_time, equatorial_coords)
