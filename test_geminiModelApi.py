import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import geminiModelApi
import unittest



class MyTestCase(unittest.TestCase):
    def test_get_zip_code_correct(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  tools=[geminiModelApi.set_zip_code], safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,

    })
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message('My zip code is 60005.  Please include my zip code in the reply.')
        # for part in response.parts:
        #     if fn := part.function_call:
        #         args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
        #         self.assertEquals(f"{fn.name}({args})", "set_zip_code(zipcode=60005.0)")
        self.assertTrue("zipcode" not in response.text)

    def test_get_pushover_api_keys_correct(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  tools=[geminiModelApi.set_pushover_api_keys])
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message('Here are my keys: ABCD12345 and AAVDSF123123.')
        # for part in response.parts:
        #     if fn := part.function_call:
        #         args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
        #         self.assertEquals(f"{fn.name}({args})", "set_pushover_api_keys(PUSHOVER_API_KEY=ABCD12345, USER_API_KEY=AAVDSF123123)")
        response_text = response.text
        self.assertFalse("ABCD12345" in response_text, "response was " + response_text)
        self.assertFalse("AAVDSF123123" in response_text,  "response was " + response_text)

    def test_get_pushover_api_keys_missing_one_key(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  tools=[geminiModelApi.set_pushover_api_keys])
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message('Here is my new key: ASDSERSD124.')
        for part in response.parts:
            if fn := part.function_call:
                args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
                self.fail("the response was incomplete so the function should not be called.")
        print(str(response.text))

    def test_get_condition_correct(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  tools=[geminiModelApi.set_conditional])
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message("I'm like to be notified when dewpoint goes below 60 degrees fahreneit")
        for part in response.parts:
            if fn := part.function_call:
                args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
                self.assertEquals(f"{fn.name}({args})", "set_conditional(less_than_or_greater_than=<, target_temperature=60.0, weather_condition=dewpoint)")
        print(str(response.text))

    def test_get_condition_missing_one_condition(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  tools=[geminiModelApi.set_conditional])
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message("I'd like to be notified when the dewpoint is equal to 60 degrees fahreneit")
        for part in response.parts:
            if fn := part.function_call:
                args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
                self.fail("expected no gt or lt symbol based on chat: " + f"{fn.name}({args})")
        print(str(response.text))

    def test_get_what_conditions_remain_unfilled(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                  tools=[geminiModelApi.set_conditional, geminiModelApi.set_pushover_api_keys, geminiModelApi.set_zip_code])
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message("What are all of the remaining unfilled values?  Be sure to consider set_conditional, set_pushover_api_keys and set_zip_code.  Start your response with: 'These are the missing values:' ")
        print(str(response.text))

    # def test_end_to_end_chat_single_shot(self):
