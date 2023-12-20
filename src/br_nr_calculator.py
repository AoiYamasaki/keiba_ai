import datetime
import random

def calculate_br_nr(race_datetime, birth_date, latitude, longitude, race_time):
    """
    レース日時、騎手の生年月日、緯度経度、出走時刻から BR と NR を計算する。

    :param race_datetime: レースの日時（datetimeオブジェクト）
    :param birth_date: 騎手の生年月日（datetimeオブジェクト）
    :param latitude: 緯度
    :param longitude: 経度
    :param race_time: 出走時刻（HH:MM 形式の文字列）
    :return: BR と NR の値
    """
    # BRの計算（生年月日からの経過日数）
    br = (race_datetime.date() - birth_date.date()).days

    # NRの計算（乱数を使用）
    # 出走時刻を時間と分に分割
    race_hour, race_minute = map(int, race_time.split(':'))
    # 緯度経度と時間を基にNRを計算
    nr = random.random() / (latitude + longitude + race_hour + race_minute / 60)

    return br, nr
