# import unittest
# import pushover
# import os
#
# class MyTestCase(unittest.TestCase):
#     PUSHOVER_API_KEY = os.environ.get("PUSHOVER_API_KEY")
#
#     def test_alert_pushover(self):
#         title = "test pushover notification title"
#         message = "test pushover notification message"
#         response = pushover.alert_pushover(title, message)
#
#         self.assertEquals(200, response.status_code)  # add assertion here
#
#
# if __name__ == '__main__':
#     unittest.main()
