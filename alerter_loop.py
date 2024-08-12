from enum import Enum

import alerter_loop
import helper
import pushover
import json
import pickle
from google.cloud import storage, secretmanager
from google.oauth2 import service_account
import time


class WeatherVariable(Enum):
    DEWPOINT = 1
    TEMPERATURE = 2

user = {}

try:
    with open("/user_data/user-data", "rb") as fp:
        user = pickle.load(fp)
except FileNotFoundError as e:
    try:
        with open('/Users/corbinjohnson/Downloads/gemini-contest-project-32013d489983.json') as source:
            info = json.load(source)
            client = secretmanager.SecretManagerServiceClient(
                credentials=service_account.Credentials.from_service_account_info(info))
            name = f"projects/152352988465/secrets/user-data/versions/latest"
            # pickle_out = pickle.dumps(user)
            response = client.access_secret_version(name=name)
            user = pickle.loads(response.payload.data)
    except FileNotFoundError as e:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/152352988465/secrets/user-data/versions/latest"
        # pickle_out = pickle.dumps(user)
        response = client.access_secret_version(name=name)
        user = pickle.loads(response.payload.data)

def unpickle():
    try:
        with open("/user_data/user-data", "rb") as fp:
            user = pickle.load(fp)
    except FileNotFoundError as e:
        try:
            with open('/Users/corbinjohnson/Downloads/gemini-contest-project-32013d489983.json') as source:
                info = json.load(source)
                client = secretmanager.SecretManagerServiceClient(
                    credentials=service_account.Credentials.from_service_account_info(info))
                name = f"projects/152352988465/secrets/user-data/versions/latest"
                # pickle_out = pickle.dumps(user)
                response = client.access_secret_version(name=name)
                user = pickle.loads(response.payload.data)
        except FileNotFoundError as e:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/152352988465/secrets/user-data/versions/latest"
            # pickle_out = pickle.dumps(user)
            response = client.access_secret_version(name=name)
            user = pickle.loads(response.payload.data)

# def depickle():
#     with open('/Users/corbinjohnson/Downloads/gemini-contest-project-32013d489983.json') as source:
#         info = json.load(source)
#         client = secretmanager.SecretManagerServiceClient(
#             credentials=service_account.Credentials.from_service_account_info(info))
#
#         name = f"projects/152352988465/secrets/user-data/versions/latest"
#         # pickle_out = pickle.dumps(user)
#         response = client.access_secret_version(name=name)
#         user = pickle.loads(response.payload.data)

def repickle():
    try:
        with open('/Users/corbinjohnson/Downloads/gemini-contest-project-32013d489983.json') as source:
            info = json.load(source)
            client = secretmanager.SecretManagerServiceClient(credentials=service_account.Credentials.from_service_account_info(info))
            parent = f"projects/152352988465/secrets/user-data"
            for each_user in user:
                each_user["session_epoch"] = int(time.time())
            with open('temp.pickle', 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                pickle.dump(user, f, pickle.HIGHEST_PROTOCOL)
            with open('temp.pickle', 'rb') as f:
                # The protocol version used is detected automatically, so we do not
                # have to specify it.
                data = f.read()
                response = client.add_secret_version(
                    request={
                        "parent": parent,
                        "payload": {
                            "data": data,
                        },
                    }
                )
                # Print the new secret version name.
                print(f'Added secret version: {response.name}')
    except FileNotFoundError as e:
        client = secretmanager.SecretManagerServiceClient()

        parent = f"projects/152352988465/secrets/user-data"
        # pickle_out = pickle.dumps(user)
        with open('temp.pickle', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(user, f, pickle.HIGHEST_PROTOCOL)
        with open('temp.pickle', 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            data = f.read()
            response = client.add_secret_version(
                request={
                    "parent": parent,
                    "payload": {
                        "data": data,
                    },
                }
            )
            # Print the new secret version name.
            print(f'Added secret version: {response.name}')



hourly_log = []


textmap = {WeatherVariable.DEWPOINT: "dewpoint",
           WeatherVariable.TEMPERATURE: "temperature"}

forecastmap = {WeatherVariable.DEWPOINT: "dewpoint",
               WeatherVariable.TEMPERATURE: "temperature"}

titleReadable = {WeatherVariable.DEWPOINT: "Dewpoint",
                 WeatherVariable.TEMPERATURE: "Temperature"}


def reset_alert(user_index):
    user[user_index]["should_alert"] = True

def should_alert(user_index):
    """Sets should_alert to False after this is called.
     Returns state before settings"""
    should_alert_before = user[user_index]["should_alert"]
    user[user_index]["should_alert"] = False
    return should_alert_before

def set_condition(user_index, condition, conditional):
    user[user_index]["condition"][condition] = conditional

def loop_runner(user_index, current_time, forecast=None):
    if forecast:
        for each_key in user[user_index]["condition"].keys():
            condition = each_key
            conditional = user[user_index]["condition"][each_key][0]
            target_value = user[user_index]["condition"][each_key][1]
            for each_forecast_key in forecast.keys():
                each_forecast_condition = each_forecast_key
                if condition == each_forecast_condition:
                    condition_met = _compare_a_and_b_with_string_comparator(forecast[each_forecast_condition], conditional, target_value)
                    if not condition_met:
                        return False
    return True

def alert_response_generator(user_index, forecast=None):
    to_return = ""
    for each_condition in user[user_index]["condition"].keys():
        conditional = user[user_index]["condition"][each_condition][0]
        target_value = user[user_index]["condition"][each_condition][1]
        to_return += "The current " + textmap[each_condition] + " is %sF.  " % forecast[each_condition]
    return to_return

# def get_forecasted_end_timestamp(user_index, forecast=None):
#    forecast["properties"]

def _get_forecasted_end_timestamp_for_conditional(user_index, conditional_object, forecast=None):
    """
    example temperature (at forecast["properties"]["temperature"]:
        "temperature": {
        "uom": "wmoUnit:degC",
        "values": [
            {
                "validTime": "2024-07-25T18:00:00+00:00/PT1H",
                "value": 25
            },
            ...
    """
    raw_forecast = forecast["properties"]
    condition = list(conditional_object.keys())[0]
    conditional_inequality = conditional_object[condition][0]
    conditional_temperature = conditional_object[condition][1]
    for each_value in raw_forecast[forecastmap[condition]]["values"]:
        if _compare_a_and_b_with_inverse_string_comparator(_get_farenheit(float(each_value["value"])), conditional_inequality, conditional_temperature):
            return each_value["validTime"]

def get_forecasted_end_timestamps(user_index, conditional_timestamp_objects, forecast=None):
    to_return = [] # [(conditional, timestamp)]
    for each_conditional_timestamp in conditional_timestamp_objects:
        timestamp = _get_forecasted_end_timestamp_for_conditional(user_index, each_conditional_timestamp, forecast=forecast)
        to_return.append((list(each_conditional_timestamp.keys())[0], timestamp))
    return to_return

def get_forecasted_timestamps_for_condition(condition, forecast=None):
    forecast_key = forecastmap[condition]
    return forecast["properties"][forecast_key]["values"]

def is_threshold_met(threshold, previous_value, current_value):
    if previous_value <= threshold and current_value >= threshold:
        return True
    if previous_value >= threshold and current_value <= threshold:
        return True
    return False

def get_directionality(previous, current):
    if previous <= current:
        return "next_is_higher"
    else:
        return "next_is_lower"

def get_crossover_timestamps(user_index, forecast=None):
    to_return = []
    forecast_key = list(user[user_index]["condition"].keys())[0]
    condition_temperature = user[user_index]["condition"][forecast_key][1]
    if forecast == None:
        return ""
    timestamps_for_condition = get_forecasted_timestamps_for_condition(forecast_key, forecast=forecast)
    for each_timestamp_index in range(len(timestamps_for_condition)):
        if each_timestamp_index > 1 and each_timestamp_index < (len(timestamps_for_condition) - 1):
            #back_value = _get_farenheit(timestamps_for_condition[each_timestamp_index - 1]["value"])
            current_timestamp = timestamps_for_condition[each_timestamp_index]["validTime"]
            current_value = _get_farenheit(timestamps_for_condition[each_timestamp_index]["value"])
            next_value = _get_farenheit(timestamps_for_condition[each_timestamp_index + 1]["value"])
            if is_threshold_met(condition_temperature, current_value, next_value):
                if len(to_return) == 0:
                    to_return.append((current_timestamp, get_directionality(current_value, next_value)))
                if len(to_return) > 0:
                    latest_directionality = to_return[-1][1]
                    if latest_directionality != get_directionality(current_value, next_value):
                        to_return.append((current_timestamp, get_directionality(current_value, next_value)))
    return to_return

def get_current_condition_value(user_index, forecast=None):
    forecast_key = list(user[user_index]["condition"].keys())[0]
    return _get_farenheit(get_forecasted_timestamps_for_condition(forecast_key, forecast=forecast)[0]["value"])

def next_forecast_notification_message_for_condition(user_index, forecast=None):
    crossover_timestamps = get_crossover_timestamps(user_index, forecast)
    forecast_key = list(user[user_index]["condition"].keys())[0]
    condition_temperature = user[user_index]["condition"][forecast_key][1]
    conditional = user[user_index]["condition"][forecast_key][0]
    conditional_key_in_english = forecastmap[forecast_key]
    if crossover_timestamps == "":
        return "The %s condition of %s %sF will not be met in the current forecast. You will be notified when this changes." \
            % (conditional_key_in_english,
               conditional,
               condition_temperature)
    crossover_timestamps = get_crossover_timestamps(user_index, forecast)
    to_return = ""
    above_or_below = ""
    for each_timestamp_index in range(len(crossover_timestamps)):
        timestamp = crossover_timestamps[each_timestamp_index][0]
        above_or_below_raw = crossover_timestamps[each_timestamp_index][1]
        if above_or_below_raw == "next_is_higher":
            above_or_below = "above"
        else:
            above_or_below = "below"
        speakable_timestamp_timezone_adjusted = helper.get_speakable_time(timestamp, user[user_index]["zipcode"])
        to_return += "On %s, %s will go %s %s degrees fahrenheit. \n" % (speakable_timestamp_timezone_adjusted,
                                                                      conditional_key_in_english,
                                                                      above_or_below,
                                                                      condition_temperature)
    return to_return

def hourly_run(forecast=None):
    print("we are running the hourly run now.")
    for each_user in range(len(user)):
        print("user %s is running" % each_user)
        if len(alerter_loop.user[each_user]["condition"]) > 0:
            if forecast is None:
                print("No forecast was passed in. grabbing forecast now for user %s" % each_user)
                forecastraw = helper.get_weather_forcast_raw(user[each_user]["zipcode"])
                forecast = json.loads(forecastraw)
                print("Forecast was loaded for user %s" % each_user)
            actual_forecast = alerter_loop.next_forecast_notification_message_for_condition(each_user, forecast=forecast)
            forecast_key = list(user[each_user]["condition"].keys())[0]
            conditional_key_in_english = titleReadable[forecast_key]
            #if should_alert(each_user):
            print("Pushover is being sent forecast data for user %s" % each_user)
            pushover.alert_pushover("Crossover - %s Forecast" % conditional_key_in_english, actual_forecast, PUSHOVER_API_KEY=user[each_user]["PUSHOVER_API_KEY"], USER_API_KEY=user[each_user]["USER_API_KEY"])
            hourly_log.append({"message": actual_forecast})
            print("The hourly log was updated for user %s" % each_user)

def hourly_run_for_a_single_user(forecast=None, SESSION=None):
    print("we are running the hourly run now for a single user.")
    for each_user in range(len(user)):
        if "SESSION" in user[each_user]:
            if user[each_user]["SESSION"] == SESSION:
                print("user %s is running" % each_user)
                if len(alerter_loop.user[each_user]["condition"]) > 0:
                    if forecast is None:
                        print("No forecast was passed in. grabbing forecast now for user %s" % each_user)
                        forecastraw = helper.get_weather_forcast_raw(user[each_user]["zipcode"])
                        forecast = json.loads(forecastraw)
                        print("Forecast was loaded for user %s" % each_user)
                    actual_forecast = alerter_loop.next_forecast_notification_message_for_condition(each_user, forecast=forecast)
                    forecast_key = list(user[each_user]["condition"].keys())[0]
                    conditional_key_in_english = titleReadable[forecast_key]
                    #if should_alert(each_user):
                    print("Pushover is being sent forecast data for user %s" % each_user)
                    pushover.alert_pushover("Crossover - %s Forecast" % conditional_key_in_english, actual_forecast, PUSHOVER_API_KEY=user[each_user]["PUSHOVER_API_KEY"], USER_API_KEY=user[each_user]["USER_API_KEY"])
                    hourly_log.append({"message": actual_forecast})
                    print("The hourly log was updated for user %s" % each_user)


def get_user_data_for_given_SESSION(SESSION):
    for each_user in user:
        if "SESSION" in each_user:
            if each_user["SESSION"] == SESSION:
                return each_user

def create_user(SESSION):
    for user_index in range(len(user)):
        if "SESSION" in user[user_index]:
            if user[user_index]["SESSION"] == SESSION:
                userkeys = user[user_index].keys()
                user[user_index] = {"should_alert":True,
                 "condition": {},
                 "zipcode":"",
                 "PUSHOVER_API_KEY":"",
                 "USER_API_KEY":"",
                 "SESSION":"%s" % SESSION,
                 "session_epoch": "%s" % (int(time.time()) -121)
                 }
        else:
            user.append({"should_alert":True,
                 "condition": {},
                 "zipcode":"",
                 "PUSHOVER_API_KEY":"",
                 "USER_API_KEY":"",
                 "SESSION":"%s" % SESSION,
                 "session_epoch": "%s" % (int(time.time()) -121)
                 })

def is_user_filled_in(SESSION):
    user_data = get_user_data_for_given_SESSION(SESSION)
    if user_data["condition"] == {}:
        return False
    if user_data["zipcode"] == "":
        return False
    if user_data["PUSHOVER_API_KEY"] == "":
        return False
    if user_data["USER_API_KEY"] == "":
        return False
    return True

def get_hourly_log(forecast=None):
    return hourly_log

def values_still_remaining(SESSION):
    to_return = []
    for each_user_index in range(len(user)):
        if "SESSION" in user[each_user_index]:
            if user[each_user_index]["SESSION"] == SESSION:
                if user[each_user_index]["condition"] == {}:
                    to_return.append("condition")
                if user[each_user_index]["zipcode"] == "":
                    to_return.append("zipcode")
                if user[each_user_index]["PUSHOVER_API_KEY"] == "":
                    to_return.append("PUSHOVER_API_KEY")
                if user[each_user_index]["USER_API_KEY"] == "":
                    to_return.append("USER_API_KEY")
                return to_return

# def alert_forecasted_end_response(user_index, forecast=None):
#     if forecast:
#         return "On %s, one or more conditionals will no longer be met." % helper.get_speakable_time(forecast["next_conditional_timestamp"], user[user_index]["zipcode"])

def _compare_a_and_b_with_string_comparator(a, comparator, b):
    if comparator == "<":
        return a < b
    if comparator == "<=":
        return a <= b
    if comparator == ">":
        return a > b
    if comparator == ">=":
        return a >= b

def _compare_a_and_b_with_inverse_string_comparator(a, comparator, b):
    if comparator == "<":
        return a >= b
    if comparator == "<=":
        return a > b
    if comparator == ">":
        return a <= b
    if comparator == ">=":
        return a < b

def _get_farenheit(c):
    return c * (9.0/5.0) +32.0
