import requests
import json

def _get_house_cooling_openapi_request_contents(ai_request):
    return '{\
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

def house_cooling_openapi_request(ai_request, api_key):
    URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    response = requests.post(URL,
                  json=json.loads(_get_house_cooling_openapi_request_contents(ai_request)),
                  params=[("key", api_key)])
    return response.text

