import unittest
from src.coordinate_conversion import ecliptic_to_equatorial, equatorial_to_ecliptic

class TestCoordinateConversion(unittest.TestCase):
    def test_ecliptic_to_equatorial(self):
        # テストケースの例
        ra, dec = ecliptic_to_equatorial(45, 45, 23.44)
        self.assertAlmostEqual(ra, 33.18, places=2)
        self.assertAlmostEqual(dec, 30.22, places=2)

    def test_equatorial_to_ecliptic(self):
        # テストケースの例
        ecl_lon, ecl_lat = equatorial_to_ecliptic(33.18, 30.22, 23.44)
        self.assertAlmostEqual(ecl_lon, 45, places=2)
        self.assertAlmostEqual(ecl_lat, 45, places=2)

if __name__ == '__main__':
    unittest.main()
