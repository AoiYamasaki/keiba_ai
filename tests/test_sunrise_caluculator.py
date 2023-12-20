import unittest
from datetime import datetime
from sunrise_calculator import calculate_sunrise_elapsed_time_and_equatorial_coords

class TestSunriseCalculator(unittest.TestCase):
    def test_calculate_sunrise_elapsed_time_and_equatorial_coords(self):
        # テストケースの設定
        latitude, longitude = 35.681236, 139.767125  # 東京駅の緯度経度
        race_date = datetime(2023, 7, 22)

        # 期待される結果（仮の値）
        expected_elapsed_time = 180  # 日の出から3時間後（秒）
        expected_ra = 90  # 仮の赤経
        expected_dec = 0   # 仮の赤緯

        # 関数の実行
        actual_elapsed_time, (actual_ra, actual_dec) = calculate_sunrise_elapsed_time_and_equatorial_coords(latitude, longitude, race_date)

        # 検証
        self.assertAlmostEqual(actual_elapsed_time, expected_elapsed_time, places=2)
        self.assertAlmostEqual(actual_ra, expected_ra, places=2)
        self.assertAlmostEqual(actual_dec, expected_dec, places=2)

if __name__ == '__main__':
    unittest.main()
