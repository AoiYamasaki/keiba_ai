import ephem
from datetime import datetime, timedelta

def calculate_solar_ecliptic_coordinates(date, sunrise, elapsed_time):
    """
    日の出時刻からの経過時間を基に、その時点での太陽の黄道座標を計算する。

    :param date: レースの日付（datetimeオブジェクト）
    :param sunrise: 日の出時刻（datetimeオブジェクト）
    :param elapsed_time: 日の出からの経過時間（分）
    :return: 黄道座標（黄経と黄緯）
    """
    observer = ephem.Observer()
    observer.date = date

    # 日の出時刻から経過時間を加算して、観測時刻を設定
    observer.date += ephem.minute * elapsed_time

    sun = ephem.Sun(observer)
    ecliptic = ephem.Ecliptic(sun)

    return ecliptic.lon, ecliptic.lat

# # 使用例
# date = datetime(2023, 7, 22)
# sunrise = datetime(2023, 7, 22, 6, 0, 0)  # 仮の日の出時刻
# elapsed_time = 120  # 日の出から2時間後

# lon, lat = calculate_solar_ecliptic_coordinates(date, sunrise, elapsed_time)
# print(f"黄経: {lon}, 黄緯: {lat}")
