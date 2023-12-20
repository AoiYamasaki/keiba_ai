import unittest
from datetime import datetime
from sun_position_calculator import calculate_solar_ecliptic_coordinates

class TestSunPositionCalculator(unittest.TestCase):
    def test_calculate_solar_ecliptic_coordinates(self):
        # テストケースの設定
        date = datetime(2023, 7, 22)
        sunrise = datetime(2023, 7, 22, 6, 0, 0)  # 仮の日の出時刻
        elapsed_time = 120  # 日の出から2時間後

        # 期待される結果（仮の値）
        expected_lon = 90  # 仮の黄経
        expected_lat = 0   # 仮の黄緯

        # 関数の実行
        actual_lon, actual_lat = calculate_solar_ecliptic_coordinates(date, sunrise, elapsed_time)

        # 検証
        self.assertAlmostEqual(actual_lon, expected_lon, places=2)
        self.assertAlmostEqual(actual_lat, expected_lat, places=2)

if __name__ == '__main__':
    unittest.main()
