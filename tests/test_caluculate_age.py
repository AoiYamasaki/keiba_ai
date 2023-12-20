import unittest
from datetime import datetime
from calculate_age import calculate_age

class TestCalculateAge(unittest.TestCase):
    def test_calculate_age(self):
        # テストケースの設定
        birth_date = datetime(1990, 1, 1)
        current_date = datetime(2023, 7, 22)
        expected_days = (current_date - birth_date).days
        expected_years = expected_days / 365.25

        # 関数の実行
        actual_days, actual_years = calculate_age(birth_date, current_date)

        # 検証
        self.assertEqual(actual_days, expected_days)
        self.assertAlmostEqual(actual_years, expected_years, places=2)

if __name__ == '__main__':
    unittest.main()
