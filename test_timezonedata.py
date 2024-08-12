import unittest
import timezonedata

class MyTestCase(unittest.TestCase):
    def test_timezone_map(self):
        timezone_entry = timezonedata.timezone_map[0]
        self.assertEquals(timezone_entry["zipcode"],"00501")
        self.assertEquals(timezone_entry["tz"],"America/New_York" )
        self.assertTrue(isinstance(timezone_entry, dict))

    def test_entire_timezone_map(self):
        for each_timezone_entry in timezonedata.timezone_map:
            self.assertEquals(len(each_timezone_entry["zipcode"]),5)
            self.assertTrue("America" in each_timezone_entry["tz"] or "Honolulu" in each_timezone_entry["tz"], "America or Honolulu is not in " + each_timezone_entry["tz"])
            self.assertTrue(isinstance(each_timezone_entry, dict))

if __name__ == '__main__':
    unittest.main()
