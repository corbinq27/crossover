import unittest
import os
import json
import helper

import main
import openapi_getter
import alerter_loop

API_KEY = os.environ.get("API_KEY")

class MyTestCase(unittest.TestCase):
    def test_get_house_cooling_utilizing_genai_to_extract_zip_code(self):
        ai_request = "my zip code is 60005"
        response = openapi_getter.house_cooling_openapi_request(ai_request, API_KEY)
        zip_code_response = json.loads(response)
        zip_code = zip_code_response['candidates'][0]['content']['parts'][0]['functionCall']['args']['location']
        raw = helper.get_weather_forcast_raw(zip_code)
        print(main.print_hi(raw, zip_code))

    def test_hourly_run(self):
        alerter_loop.set_condition(0, alerter_loop.WeatherVariable.DEWPOINT, ("<", 60))
        actualforecastraw = helper.get_weather_forcast_raw("60005")
        actualforecast = json.loads(actualforecastraw)
        alerter_loop.hourly_run()
