import unittest

import alerter_loop
import main
import helper
from uuid import UUID
import uuid

class MyTestCase(unittest.TestCase):
    def test_hi(self):
        raw = helper.get_weather_forcast_raw("60005")
        print(main.print_hi(raw, "60005"))

    def test_ai_return_new_session_value(self):
        request_as_dict = {"chat": "I'd like to set up a new user."}
        returned_response = main.ai(request_as_dict)
        returned_uuid = returned_response["SESSION"]
        try:
            uuid_obj = UUID(returned_response["SESSION"], version=4)
        except ValueError:
            self.fail("returned UUID is not a valid UUID: %s" % returned_uuid)
        self.assertEqual(str(uuid_obj), returned_uuid)

    def test_ai_returns_required_new_session_id(self):
        never_before_added_session_id = uuid.uuid4()
        request_as_dict = {"chat": "Time to set up my zip code! right?", "SESSION": never_before_added_session_id}
        returned_response = main.ai(request_as_dict)
        print(returned_response)
        self.assertTrue("The SESSION value did not correspond with any" in returned_response["response_message"])

    # def test_ai_went_idle(self):
    #     known_user_session_value = 'ded9bb62-964e-4e92-8358-1547b5ecce17'
    #     alerter_loop.create_user(known_user_session_value)
    #     request_as_dict = {"chat": "Time to set up my zip code! right?", "SESSION": known_user_session_value}
    #     returned_response = main.ai(request_as_dict)
    #     print(returned_response)
    #     self.assertTrue("It's been a while since we talked last." in returned_response["response_message"])
    #
    # def test_ai_zip_code_deep_branching(self):
    #     known_user_session_value = 'ded9bb62-964e-4e92-8358-1547b5ecce17'
    #     alerter_loop.create_user(known_user_session_value)
    #     request_as_dict = {"chat": "Time to set up my zip code! right? My Zip Code is 60005.", "SESSION": known_user_session_value}
    #     returned_response = main.ai(request_as_dict)
    #     print(returned_response)
    #     self.assertTrue("It's been a while since we talked last." in returned_response["response_message"])
    #     request_as_dict = {"chat": "My ZIP code is 60005", "SESSION": known_user_session_value}
    #     returned_response = main.ai(request_as_dict)
    #     self.assertTrue("60005" in returned_response["response_message"])

    def test_ai_zip_code_deep_branching(self):
        known_user_session_value = 'ded9bb62-964e-4e92-8358-1547b5ecce17'
        alerter_loop.create_user(known_user_session_value)
        request_as_dict = {"chat": "Time to set up my zip code! right? My Zip Code is 95050.", "SESSION": known_user_session_value}
        returned_response = main.ai(request_as_dict)
        print(returned_response)
        #self.assertTrue("It's been a while since we talked last." in returned_response["response_message"])
        request_as_dict = {"chat": "My ZIP code is 95040", "SESSION": known_user_session_value}
        main.ai(request_as_dict)
        user_list = alerter_loop.user
        for each_index in range(len(user_list)):
            if "SESSION" in user_list[each_index]:
                if user_list[each_index]["SESSION"] == known_user_session_value:
                    self.assertEqual(user_list[each_index]["zipcode"], "95040")

    def test_complete_setting(self):
        known_user_session_value = 'ded9bb62-964e-4e92-8358-1547b5ecce17'
        alerter_loop.create_user(known_user_session_value)
        request_as_dict = {"chat": "Time to set up my zip code! right? My Zip Code is 95050.", "SESSION": known_user_session_value}
        main.ai(request_as_dict)
        request_as_dict = {"chat": "My ZIP code is 95040", "SESSION": known_user_session_value}
        main.ai(request_as_dict)
        user_list = alerter_loop.user
        for each_index in range(len(user_list)):
            if "SESSION" in user_list[each_index]:
                if user_list[each_index]["SESSION"] == known_user_session_value:
                    self.assertEqual(user_list[each_index]["zipcode"], "95040")
        request_as_dict = {"chat": "I would like to be notified when the dewpoint is lower than 60 degrees fahrenheit", "SESSION": known_user_session_value}
        main.ai(request_as_dict)
        user_list = alerter_loop.user
        for each_index in range(len(user_list)):
            if "SESSION" in user_list[each_index]:
                if user_list[each_index]["SESSION"] == known_user_session_value:
                    self.assertEquals(list(user_list[each_index]["condition"].keys())[0], alerter_loop.WeatherVariable.DEWPOINT)
                    self.assertEquals(user_list[each_index]["condition"][alerter_loop.WeatherVariable.DEWPOINT][0], "<")
                    self.assertEquals(user_list[each_index]["condition"][alerter_loop.WeatherVariable.DEWPOINT][1], 60)
        request_as_dict = {"chat": "My pushover user API key is 12312312312345645678912345abcd and my Pushover API key is 12345678af123255489a12356498dd.",
                           "SESSION": known_user_session_value}
        main.ai(request_as_dict)
        for each_index in range(len(user_list)):
            if "SESSION" in user_list[each_index]:
                if user_list[each_index]["SESSION"] == known_user_session_value:
                    self.assertEqual(user_list[each_index]["PUSHOVER_API_KEY"], "12345678af123255489a12356498dd")
                    self.assertEqual(user_list[each_index]["USER_API_KEY"], "12312312312345645678912345abcd")



    # def test_ai_return_request_for_zip_code_with_new_session_id(self):
    #     request_as_dict = {"chat": "I'd like to set up a new user."}
    #     returned_response = main.ai(request_as_dict)
    #     returned_uuid = returned_response["SESSION"]
    #     next_request_as_dict = {"chat": "my zip code is 60005.", "SESSION": returned_uuid}
    #     next_returned_response = main.ai(next_request_as_dict)
    #     self.assertTrue(len(next_returned_response["repsonse_message"]) > 0)




if __name__ == '__main__':
    unittest.main()
