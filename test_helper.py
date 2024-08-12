import unittest
import helper
import zipcodedata

class MyTestCase(unittest.TestCase):
    def test_interpolate_lat_long_50000(self):
        avg_lat, avg_long = helper.interpolate_lat_lon('50000', zipcodedata.zipcodes)
        self.assertEquals(avg_lat, 41.362724)
        self.assertEquals(avg_long, -93.433418)

    def test_interpolate_lat_long_60000(self):
        avg_lat, avg_long = helper.interpolate_lat_lon('60001', zipcodedata.zipcodes)
        self.assertEquals(avg_lat, 42.471741)
        self.assertEquals(avg_long, -88.084493)

    def test_get_weather_for_60005(self):
        print(helper.get_weather_forcast_raw("60005"))

    def test_get_glossary(self):
        self.assertTrue(len(helper.get_weather_api_glossary()) > 5000)

    def test_get_speakable_time(self):
        self.assertEquals("Thursday, July 25 at 1 PM", helper.get_speakable_time("2024-07-25T18:00:00+00:00/PT1H", "60005"))
        self.assertEquals("Saturday, July 27 at 4 AM", helper.get_speakable_time("2024-07-27T09:00:00+00:00/PT3H", "60005"))



if __name__ == '__main__':
    unittest.main()
