import unittest
import openapi_getter


class MyTestCase(unittest.TestCase):
    def test_get_house_cooling_openapi_request_contents(self):
        ai_request = "my zip code is 60005"
        contents_block = openapi_getter._get_house_cooling_openapi_request_contents(ai_request)
        expected_contents_block = '{\
    "contents": {\
      "role": "user",\
      "parts": {\
        "text": "' + ai_request + '"\
    }\
  },\
  "tools": [\
    {\
      "function_declarations": [\
        {\
          "name": "window_opening_forecast",\
          "description": "Given a zip code, returns information on if the user should open their windows in their house.",\
          "parameters": {\
            "type": "object",\
            "properties": {\
              "location": {\
                "type": "string",\
                "description": "a zip code e.g. 95616"\
              }\
            },\
            "required": [\
              "location"\
            ]\
          }\
        }\
      ]\
    }\
  ]\
}'
        self.assertEqual(contents_block, expected_contents_block)


if __name__ == '__main__':
    unittest.main()
