from datetime import datetime

def calculate_age(birth_date, current_date):
    """
    誕生日と現在日時から、経過日数と平均太陽時による年数を計算する。

    :param birth_date: 誕生日（datetimeオブジェクト）
    :param current_date: 現在の日時（datetimeオブジェクト）
    :return: 経過日数と平均太陽時による年数
    """
    elapsed_days = (current_date - birth_date).days
    solar_years = elapsed_days / 365.25  # 平均太陽年を考慮

    return elapsed_days, solar_years

# # 使用例
# birth_date = datetime(1990, 1, 1)
# current_date = datetime(2023, 7, 22)

# days, years = calculate_age(birth_date, current_date)
# print(f"経過日数: {days}, 平均太陽時による年数: {years}")


# birth_dateがオブジェクトの場合↑を使用
# Stringの場合は↓を使用

# from datetime import datetime

# def calculate_elapsed_days_and_solar_years(birth_date, race_date):
#     """
#     誕生日とレース日時から経過日数と平均太陽時による年数を計算する。

#     :param birth_date: 誕生日（文字列、例: '1990-01-01'）
#     :param race_date: レース日時（datetimeオブジェクト）
#     :return: 経過日数、平均太陽時による年数
#     """
#     birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
#     elapsed_days = (race_date - birth_date).days
#     solar_years = elapsed_days / 365.25  # 平均太陽年を考慮

#     return elapsed_days, solar_years

# # テスト用のコード
# if __name__ == "__main__":
#     # テスト用のデータ
#     test_birth_date = '1990-01-01'
#     test_race_date = datetime(2023, 7, 22)

#     elapsed_days, solar_years = calculate_elapsed_days_and_solar_years(test_birth_date, test_race_date)
#     print("Elapsed days:", elapsed_days)
#     print("Solar years:", solar_years)
