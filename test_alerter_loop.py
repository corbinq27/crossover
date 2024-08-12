import json
import unittest
import alerter_loop


class MyTestCase(unittest.TestCase):
    def test_first_user_should_be_alerted(self):
        alerter_loop.reset_alert(0)
        should_alert = alerter_loop.user[0]["should_alert"]
        self.assertEqual(should_alert, True)  # add assertion here

    def test_first_user_should_not_be_alerted_after_getting(self):
        alerter_loop.reset_alert(0)
        should_alert = alerter_loop.should_alert(0)
        self.assertEqual(should_alert, True)
        should_alert_now = alerter_loop.should_alert(0)
        self.assertEqual(should_alert_now, False)

    def test_simple_dewpoint_loop_morning(self):
        """app runs off of central time
           so we pass in central time to the loop_runner
           but if the user is in a different time zone
           the loop_runner translates to local time before
           doing anything.

           All temps are in F and are integers"""
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        should_alert = alerter_loop.loop_runner(0, 900, forecast={alerter_loop.WeatherVariable.DEWPOINT: 59})
        self.assertEqual(should_alert, True)


    def test_simple_dewpoint_loop_morning_negative(self):
        """app runs off of central time
           so we pass in central time to the loop_runner
           but if the user is in a different time zone
           the loop_runner translates to local time before
           doing anything.

           All temps are in F and are integers"""
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        should_alert = alerter_loop.loop_runner(0, 900, forecast={alerter_loop.WeatherVariable.DEWPOINT: 60})
        self.assertEqual(should_alert, False)

    def test_simple_dewpoint_loop_morning_two_variables(self):
        """app runs off of central time
           so we pass in central time to the loop_runner
           but if the user is in a different time zone
           the loop_runner translates to local time before
           doing anything.

           All temps are in F and are integers"""
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.TEMPERATURE, ("<", 72))
        should_alert = alerter_loop.loop_runner(0, 900, forecast={alerter_loop.WeatherVariable.DEWPOINT: 59,
                                                              alerter_loop.WeatherVariable.TEMPERATURE: 71})
        self.assertEqual(should_alert, True)


    def test_simple_dewpoint_loop_morning_two_variables_single_negative(self):
        """app runs off of central time
           so we pass in central time to the loop_runner
           but if the user is in a different time zone
           the loop_runner translates to local time before
           doing anything.

           All temps are in F and are integers"""
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.TEMPERATURE, ("<", 72))
        should_alert = alerter_loop.loop_runner(0, 900, forecast={alerter_loop.WeatherVariable.DEWPOINT: 60,
                                                              alerter_loop.WeatherVariable.TEMPERATURE: 71})
        self.assertEqual(should_alert, False)

    def test_simple_dewpoint_loop_morning_two_variables_different_single_negative(self):
        """app runs off of central time
           so we pass in central time to the loop_runner
           but if the user is in a different time zone
           the loop_runner translates to local time before
           doing anything.

           All temps are in F and are integers"""
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.TEMPERATURE, ("<", 72))
        should_alert = alerter_loop.loop_runner(0, 900, forecast={alerter_loop.WeatherVariable.DEWPOINT: 59,
                                                              alerter_loop.WeatherVariable.TEMPERATURE: 72})
        self.assertEqual(should_alert, False)


    def test_simple_dewpoint_loop_morning_two_variables_both_negative(self):
        """app runs off of central time
           so we pass in central time to the loop_runner
           but if the user is in a different time zone
           the loop_runner translates to local time before
           doing anything.

           All temps are in F and are integers"""
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.TEMPERATURE, ("<", 72))
        should_alert = alerter_loop.loop_runner(0, 900, forecast={alerter_loop.WeatherVariable.DEWPOINT: 60,
                                                              alerter_loop.WeatherVariable.TEMPERATURE: 72})
        self.assertEqual(should_alert, False)



    # def test_simple_dewpoint_loop_morning_afternoon(self):
    #     alerter_loop.set_condition(0, (alerter_loop.WeatherVariable.DEWPOINT, "<", 60))
    #     should_alert = alerter_loop.loop_runner(0, 900, forecast=[(alerter_loop.WeatherVariable.DEWPOINT, 59)])
    #     self.assertEqual(should_alert, True)
    #     should_alert = alerter_loop.loop_runner(0, 1100, forecast=[(alerter_loop.WeatherVariable.DEWPOINT, 59)])
    #     self.assertEqual(should_alert, False)
    #     should_alert = alerter_loop.loop_runner(0, 1200, forecast=[(alerter_loop.WeatherVariable.DEWPOINT, 60)])
    #     self.assertEqual(should_alert, True)

    def test_comparator_less_than(self):
        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(1,"<",2)
        self.assertEqual(a_less_than_b, True)

        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(2, "<", 2)
        self.assertEqual(a_less_than_b, False)

        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(3, "<", 2)
        self.assertEqual(a_less_than_b, False)

        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(1.0,"<",2)
        self.assertEqual(a_less_than_b, True)

        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(2.0, "<", 2)
        self.assertEqual(a_less_than_b, False)

        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(3.0, "<", 2)
        self.assertEqual(a_less_than_b, False)

        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(1.0, "<", 2.0)
        self.assertEqual(a_less_than_b, True)

        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(2.0, "<", 2.0)
        self.assertEqual(a_less_than_b, False)

        a_less_than_b = alerter_loop._compare_a_and_b_with_string_comparator(3.0, "<", 2.0)
        self.assertEqual(a_less_than_b, False)

    def test_comparator_less_than_or_equal(self):
        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(1,"<=", 2)
        self.assertEqual(a_less_than_or_equal_to_b, True)

        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(2, "<=", 2)
        self.assertEqual(a_less_than_or_equal_to_b, True)

        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(3, "<=", 2)
        self.assertEqual(a_less_than_or_equal_to_b, False)

        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(1.0,"<=",2)
        self.assertEqual(a_less_than_or_equal_to_b, True)

        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(2.0, "<=", 2)
        self.assertEqual(a_less_than_or_equal_to_b, True)

        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(3.0, "<=", 2)
        self.assertEqual(a_less_than_or_equal_to_b, False)

        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(1.0, "<=", 2.0)
        self.assertEqual(a_less_than_or_equal_to_b, True)

        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(2.0, "<=", 2.0)
        self.assertEqual(a_less_than_or_equal_to_b, True)

        a_less_than_or_equal_to_b = alerter_loop._compare_a_and_b_with_string_comparator(3.0, "<=", 2.0)
        self.assertEqual(a_less_than_or_equal_to_b, False)


    def test_comparator_greater_than(self):
        a_greater_than_b = alerter_loop._compare_a_and_b_with_string_comparator(1,">",2)
        self.assertEqual(a_greater_than_b, False)

        a_greater_than_b = alerter_loop._compare_a_and_b_with_string_comparator(2, ">", 2)
        self.assertEqual(a_greater_than_b, False)

        a_greater_than_b = alerter_loop._compare_a_and_b_with_string_comparator(3, ">", 2)
        self.assertEqual(a_greater_than_b, True)

    def test_comparator_greater_than_or_equal_to(self):
        a_greater_than_b = alerter_loop._compare_a_and_b_with_string_comparator(1,">=",2)
        self.assertEqual(a_greater_than_b, False)

        a_greater_than_b = alerter_loop._compare_a_and_b_with_string_comparator(2, ">=", 2)
        self.assertEqual(a_greater_than_b, True)

        a_greater_than_b = alerter_loop._compare_a_and_b_with_string_comparator(3, ">=", 2)
        self.assertEqual(a_greater_than_b, True)

    def test_alert_response_generator(self):
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.TEMPERATURE, ("<", 72))
        alert_response = alerter_loop.alert_response_generator(0, forecast={alerter_loop.WeatherVariable.DEWPOINT: 60,
                                                       alerter_loop.WeatherVariable.TEMPERATURE: 72})

        self.assertEqual("The current dewpoint is 60F.  The current temperature is 72F.  ", alert_response)

    # def test_alert_response_forcasted_end(self):
    #     alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
    #     alerter_loop.set_condition(0, alerter_loop.WeatherVariable.TEMPERATURE, ("<", 72))
    #     forcasted_end_response = alerter_loop.alert_forecasted_end_response(0, forecast={"next_conditional_timestamp": "2018-09-04T00:00:00+00:00/PT1H"})
    #     self.assertEqual("On Monday, September 03 at 7 PM, one or more conditionals will no longer be met.", forcasted_end_response)

    def test_get_forecasted_end_timestamp_for_conditional(self):
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))

        with open("testforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            conditional_object = {alerter_loop.WeatherVariable.DEWPOINT: ("<", 60)}
            timestamp = alerter_loop._get_forecasted_end_timestamp_for_conditional(0, conditional_object, forecast=testforecast)
            expected_next_higher_dewpoint_timestamp = "2024-07-27T03:00:00+00:00/PT1H"
            self.assertEquals(expected_next_higher_dewpoint_timestamp, timestamp)

    def test_get_forecasted_end_timestamp(self):
        with open("testforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.TEMPERATURE, ("<", 72))
            dewpoint_conditional_object = {alerter_loop.WeatherVariable.DEWPOINT: ("<", 60)}
            temperature_conditional_object = {alerter_loop.WeatherVariable.TEMPERATURE: ("<", 72)}
            expected_next_higher_dewpoint_timestamp = '2024-07-27T03:00:00+00:00/PT1H'
            expected_next_higher_temperature_timestamp = '2024-07-25T18:00:00+00:00/PT1H'
            expected_returned_value = [(alerter_loop.WeatherVariable.DEWPOINT, expected_next_higher_dewpoint_timestamp),
             (alerter_loop.WeatherVariable.TEMPERATURE, expected_next_higher_temperature_timestamp)]
            actual_return_value = alerter_loop.get_forecasted_end_timestamps(0, [dewpoint_conditional_object, temperature_conditional_object], forecast=testforecast)
            self.assertEqual(expected_returned_value, actual_return_value)

    def test_get_forecasted_timestamps_for_condition(self):
        with open("testforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
            all_forecasted_timestamps = alerter_loop.get_forecasted_timestamps_for_condition(alerter_loop.WeatherVariable.DEWPOINT, forecast=testforecast)
            expected_first_value = {
                    "validTime": "2024-07-25T18:00:00+00:00/PT1H",
                    "value": 13.888888888888889
                }
            expected_last_value = {
                    "validTime": "2024-08-01T17:00:00+00:00/PT8H",
                    "value": 22.777777777777779
                }
            self.assertEqual(all_forecasted_timestamps[0], expected_first_value)
            self.assertEqual(all_forecasted_timestamps[-1], expected_last_value)

    def test_is_threshold_met(self):
        self.assertTrue(alerter_loop.is_threshold_met(60, 59, 60))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60, 59))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60, 60))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60.0, 59))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60, 59.0))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60.01, 59))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60, 58.99))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60.00, 58.99))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60.00, 59.0))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60.01, 59.0))
        self.assertTrue(alerter_loop.is_threshold_met(60, 60.00, 59.01))
        self.assertFalse(alerter_loop.is_threshold_met(60, 60.02, 60.01))
        self.assertFalse(alerter_loop.is_threshold_met(60, 61, 60.01))
        self.assertFalse(alerter_loop.is_threshold_met(60, 60.02, 61))

    def test_get_directionality(self):
        self.assertEquals("next_is_higher",alerter_loop.get_directionality(60, 61))
        self.assertEquals("next_is_higher",alerter_loop.get_directionality(60, 60))
        self.assertEquals("next_is_lower",alerter_loop.get_directionality(60, 59))

    def test_empty_get_crossover_timestamps(self):
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        actual_crossover_timestamps = alerter_loop.get_crossover_timestamps(0, forecast=None)
        self.assertEquals("", actual_crossover_timestamps)

    def test_get_crossover_timestamps(self):
        with open("testforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
            expected_crossover_timestamps = [("2024-07-27T02:00:00+00:00/PT1H", "next_is_higher"), ("2024-07-27T06:00:00+00:00/PT2H", "next_is_lower"), ("2024-07-27T12:00:00+00:00/PT2H", "next_is_higher")]
            actual_crossover_timestamps = alerter_loop.get_crossover_timestamps(0, forecast=testforecast)
            self.assertEqual(expected_crossover_timestamps, actual_crossover_timestamps)

    def test_get_crossover_timestamps_fickle(self):
        with open("ficklerawforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
            expected_crossover_timestamps = [('2024-08-08T06:00:00+00:00/PT2H', 'next_is_lower'),
                ('2024-08-08T08:00:00+00:00/PT5H', 'next_is_higher'),
                ('2024-08-08T13:00:00+00:00/PT3H', 'next_is_lower'),
                ('2024-08-08T19:00:00+00:00/PT2H', 'next_is_higher'),
                ('2024-08-09T03:00:00+00:00/PT1H', 'next_is_lower'),
                ('2024-08-13T00:00:00+00:00/PT12H', 'next_is_higher')]
            actual_crossover_timestamps = alerter_loop.get_crossover_timestamps(0, forecast=testforecast)
            self.assertEqual(expected_crossover_timestamps, actual_crossover_timestamps)

    def test_get_empty_next_forecast_for_condition(self):
        expected_next_forecast_notification_message = "The dewpoint condition of < 60F will not be met in the current forecast. You will be notified when this changes."
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        actual_next_forecast_notification_message = alerter_loop.next_forecast_notification_message_for_condition(0, forecast=None)
        self.assertEqual(expected_next_forecast_notification_message, actual_next_forecast_notification_message)

    def test_get_current_condition_value(self):
        with open("testforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
            current_condition_value = alerter_loop.get_current_condition_value(0, forecast=testforecast)
            self.assertEquals(57.0, current_condition_value)

    def test_get_next_forecast_for_condition(self):
        with open("testforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
            expected_crossover_timestamps = ["2024-07-27T03:00:00+00:00/PT1H", "2024-07-27T08:00:00+00:00/PT1H",
                                             "2024-07-27T14:00:00+00:00/PT3H"]
            expected_forecast = "On Friday, July 26 at 9 PM, dewpoint will go above 60 degrees fahrenheit. \nOn Saturday, July 27 at 1 AM, dewpoint will go below 60 degrees fahrenheit. \nOn Saturday, July 27 at 7 AM, dewpoint will go above 60 degrees fahrenheit. \n"
            actual_forecast = alerter_loop.next_forecast_notification_message_for_condition(0, forecast=testforecast)
            self.assertEqual(expected_forecast, actual_forecast)

    def test_get_next_forecast_for_condition_different(self):
        with open("testforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, (">", 60))
            expected_forecast = "On Friday, July 26 at 9 PM, dewpoint will go above 60 degrees fahrenheit. \nOn Saturday, July 27 at 1 AM, dewpoint will go below 60 degrees fahrenheit. \nOn Saturday, July 27 at 7 AM, dewpoint will go above 60 degrees fahrenheit. \n"
            actual_forecast = alerter_loop.next_forecast_notification_message_for_condition(0, forecast=testforecast)
            self.assertEqual(expected_forecast, actual_forecast)

    def test_alert_looper_for_one_user(self):
        with open("testforecast.json", "r") as fp:
            testforecast = json.loads(fp.read())
            alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
            alerter_loop.hourly_run(forecast=testforecast)
            hourly_log = alerter_loop.get_hourly_log()[0]["message"]
            expected_forecast = "On Friday, July 26 at 9 PM, dewpoint will go above 60 degrees fahrenheit. \nOn Saturday, July 27 at 1 AM, dewpoint will go below 60 degrees fahrenheit. \nOn Saturday, July 27 at 7 AM, dewpoint will go above 60 degrees fahrenheit. \n"
            self.assertEqual(hourly_log, expected_forecast)

    def test_get_user_data_for_given_SESSION(self):
        SESSION = "1234abcd"
        alerter_loop.create_user(SESSION)
        user_data = alerter_loop.get_user_data_for_given_SESSION(SESSION)
        self.assertTrue("PUSHOVER_API_KEY" in user_data)

    def test_clear_user(self):
        SESSION = "ded9bb62-964e-4e92-8358-1547b5ecce17"
        alerter_loop.create_user(SESSION)
        user_data = alerter_loop.get_user_data_for_given_SESSION(SESSION)
        self.assertTrue(user_data["PUSHOVER_API_KEY"] == "")

    def test_is_clear_user_filled_in(self):
        SESSION = "ded9bb62-964e-4e92-8358-1547b5ecce17"
        alerter_loop.create_user(SESSION)
        self.assertFalse(alerter_loop.is_user_filled_in(SESSION))

    def test_is_filled_user_filled_in(self):
        SESSION = "filledintestuser"
        self.assertTrue(alerter_loop.is_user_filled_in(SESSION))

    def test_all_values_still_missing(self):
        SESSION = "ded9bb62-964e-4e92-8358-1547b5ecce17"
        alerter_loop.create_user(SESSION)
        values_not_filled_in = alerter_loop.values_still_remaining(SESSION)
        expected_values_not_filled_in = ['condition', 'zipcode', 'PUSHOVER_API_KEY', 'USER_API_KEY']
        self.assertEqual(values_not_filled_in, expected_values_not_filled_in)

    def test_less_values_still_missing(self):
        SESSION = "ded9bb62-964e-4e92-8358-1547b5ecce17"
        alerter_loop.create_user(SESSION)
        user_list = alerter_loop.user
        for each_index in range(len(user_list)):
            if "SESSION" in user_list[each_index]:
                if user_list[each_index]["SESSION"] == SESSION:
                    user_list[each_index]["PUSHOVER_API_KEY"] = str("12345")
                    user_list[each_index]["USER_API_KEY"] = str("ABCDE")
        values_not_filled_in = alerter_loop.values_still_remaining(SESSION)
        expected_values_not_filled_in = ['condition', 'zipcode']
        self.assertEqual(values_not_filled_in, expected_values_not_filled_in)

    # def test_create_user_for_given_session(self):
    #     SESSION =

    def test_repickle(self):
        alerter_loop.repickle()

if __name__ == '__main__':
    unittest.main()
