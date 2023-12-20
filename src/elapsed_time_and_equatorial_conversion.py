import pandas as pd
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import pytz

def calculate_elapsed_time_and_equatorial_coords(race_datetime, latitude, longitude):
    """
    レース日時と緯度経度から、日の出からの経過時間と東の地平線の赤道座標を計算する。

    :param race_datetime: レースの日時（datetimeオブジェクト）
    :param latitude: 緯度
    :param longitude: 経度
    :return: 日の出からの経過時間（分）、赤道座標（赤経、赤緯）（度）
    """
    # 競馬場の位置情報を設定
    location = LocationInfo(latitude=latitude, longitude=longitude)

    # タイムゾーンを設定
    timezone = pytz.timezone('Asia/Tokyo')  # ここでは日本のタイムゾーンを使用
    race_datetime = race_datetime.replace(tzinfo=timezone)

    # 日の出時刻を計算
    s = sun(location.observer, date=race_datetime.date(), tzinfo=timezone)
    sunrise = s['sunrise']

    # 日の出からの経過時間を計算
    elapsed_time = (race_datetime - sunrise).total_seconds() / 60  # 分単位

    # 東の地平線の赤道座標を計算（仮の計算）
    equatorial_ra = longitude  # 赤経
    equatorial_dec = 0  # 赤緯（地平線上なので0）

    return elapsed_time, (equatorial_ra, equatorial_dec)
