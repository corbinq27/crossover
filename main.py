import helper
import logging
import json
import pushover
import alerter_loop
import uuid
import functions_framework
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import geminiModelApi
import unittest
import time
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)

GLOBAL_SESSION = ""

def print_hi(raw_forecast_data, zipcode):
    zip_code_forecast = json.loads(raw_forecast_data)
    update_time = zip_code_forecast["properties"]["updateTime"]
    # Example update_time: 2018-09-09T21:17:08+00:00
    current_time = update_time
    dewpoint_tree = zip_code_forecast["properties"]["dewpoint"]["values"]
    # add an entry for all of the missing dewpoints
    most_current_timestamp = helper.get_most_current_timestamp(dewpoint_tree, current_time)
    current_dewpoint_c = int(most_current_timestamp["value"])
    current_dewpoint_f = int(current_dewpoint_c * 1.8 + 32)
    current_dewpoint_t = most_current_timestamp["validTime"]

    temperature_tree = zip_code_forecast["properties"]["temperature"]["values"]
    most_current_temperature_timestamp = helper.get_most_current_timestamp(temperature_tree, current_time)
    current_temperature_c = int(most_current_temperature_timestamp["value"])
    current_temperature_f = int(current_temperature_c * 1.8 + 32)
    current_temperature_t = most_current_temperature_timestamp["validTime"]

    logger.info("zip code: %s" % zipcode)
    logger.info("current time: %s" % current_time)
    logger.info("Current Dewpoint in C: %s" % current_dewpoint_c)
    logger.info("Current Dewpoint in F: %s" % current_dewpoint_f)
    logger.info("Current time for dewpoint: %s" % current_dewpoint_t)
    dp_obj = helper.next_dewpoint_lower_than_60(dewpoint_tree, current_time)
    #logger.info("Next time dewpoint is less than 60d: %s dewpoint: %s" % (dp_obj["validTime"], dp_obj["value"] * 1.8 + 32))
    logger.info("Update Time: %s" % update_time)
    logger.info("Current Tempera    ture in C: %s" % current_temperature_c)
    logger.info("Current Temperature in F: %s" % current_temperature_f)
    logger.info("Current time for Temperature: %s" % current_temperature_t)

    dp_speech_output = helper.get_proper_dewpoint_output(current_temperature_f, current_dewpoint_f, dp_obj, temperature_tree, zipcode, dewpoint_tree)
    pushover.alert_pushover("Open Windows?", dp_speech_output)

    return dp_speech_output

def ai(request_as_dict):
    global GLOBAL_SESSION
    if "SESSION" not in request_as_dict:
        new_session_value = str(uuid.uuid4())
        alerter_loop.create_user(new_session_value)
        return {"response_message": "here is your new session id: %s.  "
                                    "If you believe you have received this"
                                    " message in error, please be sure to always "
                                    "include your SESSION as a request parameter"
                                    " in every call." % new_session_value, "SESSION": new_session_value}
    if "SESSION" in request_as_dict:
        if None == alerter_loop.get_user_data_for_given_SESSION(request_as_dict["SESSION"]):
            return {"response_message": "The SESSION value did not correspond with any known user. You can "
                                        "request a new SESSION value by sending a response without the 'SESSION' "
                                        "parameter."}
        #### At this point, we know the user has a valid session. We're just not sure if we've talked in the last 2 minutes.
        current_user_data = alerter_loop.get_user_data_for_given_SESSION(request_as_dict["SESSION"])
        GLOBAL_SESSION = request_as_dict["SESSION"]
        if "chat" in request_as_dict:
            epoch_time = int(time.time())
            if (int(epoch_time)) - int(current_user_data["session_epoch"]) > 120: #seconds
                for each_index in range(len(alerter_loop.user)):
                    if "SESSION" in alerter_loop.user[each_index]:
                        if alerter_loop.user[each_index]["SESSION"] == request_as_dict["SESSION"]:
                            alerter_loop.user[each_index]["session_epoch"] = epoch_time
                return {"response_message": "here's the values I'm still looking to get filled"
                                                " in: %s \nIf you haven't filled out zip code yet, just chat to me saying "
                                                "something like 'my zip code is 94040. \nIf you haven't filled in condition yet, just chat to me "
                                                "saying something like 'I'd like to be notified when the dewpoint (or temperature) goes above 60 degrees fahrenheit."
                                                "\n If you haven't filled in the pushover API keys, go grab your pushover user key and pushover api key.  Then chat me "
                                                "saying something like 'my User API Key is abcd1234 and my Pushover API Key is efgh5678.  \nOnce I have all of the "
                                                "data, I'll let start alerting you about the weather to pushover! " % (alerter_loop.values_still_remaining(request_as_dict["SESSION"]))}
            else: # Since we've talked within the last two minutes
                if "test" in request_as_dict["chat"]:
                    alerter_loop.hourly_run_for_a_single_user(SESSION=request_as_dict["SESSION"])
                    return {"response_message": "You should be getting a pushover notification with the weather data.  Thanks for using Crossover!"}
                else:
                    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
                    model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                                  tools=[geminiModelApi.set_conditional,
                                                         geminiModelApi.set_pushover_api_keys,
                                                         geminiModelApi.set_zip_code])
                    chat = model.start_chat(enable_automatic_function_calling=True)
                    response_old = chat.send_message(request_as_dict["chat"])
                    if alerter_loop.is_user_filled_in(request_as_dict["SESSION"]):
                        return {"response_message": "%s.  All fields are filled in.  You "
                                                    "will get a report twice a day pushed to Pushover detailing"
                                                    " the weather condition and when it will crossover! Thanks "
                                                    "for using Crossover.  If you wish to change something, "
                                                    "send a chat asking to change along with your SESSION." % str(response_old.text)}
                    else: #Find out what still needs to be filled in and request
                        return {"response_message": "%s Also, here's the values I'm still looking to get filled"
                                                    " in: %s \nIf you haven't filled out zip code yet, just chat to me saying "
                                                    "something like 'my zip code is 94040. \nIf you haven't filled in condition yet, just chat to me "
                                                    "saying something like 'I'd like to be notified when the dewpoint (or temperature) goes above 60 degrees fahrenheit."
                                                    "\n If you haven't filled in the pushover API keys, go grab your pushover user key and pushover api key.  Then chat me "
                                                    "saying something like 'my User API Key is abcd1234 and my Pushover API Key is efgh5678.  \nOnce I have all of the "
                                                    "data, I'll let start alerting you about the weather to pushover! " % (str(response_old.text), alerter_loop.values_still_remaining(request_as_dict["SESSION"]))}

def user_session(request):
    request_json = request.get_json(silent=True)
    #if request_json["SESSION"]:
    response = ai(request_json)
    return "%s " % response

def entry_method(stuff):
    alerter_loop.unpickle()
    alerter_loop.hourly_run()
    alerter_loop.repickle()
    return "stuff!"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
