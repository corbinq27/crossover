import unittest
import zipcodedata

class MyTestCase(unittest.TestCase):
    def test_zipcode_has_lat_long_data(self):
        lat_long = zipcodedata.zipcodes["00501"]
        self.assertFalse(lat_long[0] is None)
        self.assertFalse(lat_long[1] is None)
        self.assertTrue(isinstance(lat_long[0], float), "latitude of zip code is not a float")
        self.assertTrue(isinstance(lat_long[1], float), "longitude of zip code is not a float")

    def test_all_zipcodes_have_lat_long_data(self):
        for each_zip in zipcodedata.zipcodes:
            latitude, longitude = zipcodedata.zipcodes[each_zip]
            self.assertFalse(latitude is None)
            self.assertFalse(longitude is None)
            self.assertTrue(isinstance(latitude, float), "latitude of zip code is not a float")
            self.assertTrue(isinstance(longitude, float), "longitude of zip code is not a float")


if __name__ == '__main__':
    unittest.main()
