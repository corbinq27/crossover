import timezonedata
import zipcodedata
import requests
import json
import logging
from datetime import datetime
import pytz

zipcodes = zipcodedata.zipcodes

USER_AGENT = "corbinjohnson@me.com"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def interpolate_lat_lon(zipcode, zipcodes):
    valid_zip_codes_with_matching_prefix = []
    for each_zipcode in zipcodes.keys():
        if each_zipcode[0:3] == zipcode[0:3]:
            print("each zipcode %s" % each_zipcode)
            valid_zip_codes_with_matching_prefix.append(int(each_zipcode))
    valid_zip_codes_with_matching_prefix.append(int(zipcode))
    valid_zip_codes_with_matching_prefix = list(set(valid_zip_codes_with_matching_prefix))
    print("valid_zip_codes_with_matching_prefix: %s" % valid_zip_codes_with_matching_prefix)
    valid_zip_codes_with_matching_prefix.sort()
    print("valid_zip_codes_with_matching_prefix: %s" % valid_zip_codes_with_matching_prefix)
    if len(valid_zip_codes_with_matching_prefix) == (valid_zip_codes_with_matching_prefix.index(int(zipcode)) + 1):
        return (zipcodes["%05d" % valid_zip_codes_with_matching_prefix[-2]][0], zipcodes["%05d" % valid_zip_codes_with_matching_prefix[-2]][1])
    if valid_zip_codes_with_matching_prefix.index(int(zipcode)) == 0:
        return (zipcodes["%05d" % valid_zip_codes_with_matching_prefix[1]][0], zipcodes["%05d" % valid_zip_codes_with_matching_prefix[1]][1])
    else:
        index_of_current_zip_code = valid_zip_codes_with_matching_prefix.index(int(zipcode))
        previous_zipcode = valid_zip_codes_with_matching_prefix[index_of_current_zip_code - 1]
        next_zipcode = valid_zip_codes_with_matching_prefix[index_of_current_zip_code + 1]
        print("valid_zip_codes_with_matching_prefix: %s" % valid_zip_codes_with_matching_prefix)
        previous_lat = zipcodes["%05d" % previous_zipcode][0]
        previous_lon = zipcodes["%05d" % previous_zipcode][1]
        next_lat     = zipcodes["%05d" % next_zipcode][0]
        next_lon     = zipcodes["%05d" % next_zipcode][1]
        avg_lat      = (previous_lat + next_lat) / 2
        avg_lon      = (previous_lon + next_lon) / 2
        return (avg_lat, avg_lon)

def get_weather_forcast_raw(zipcode):
    if zipcode not in zipcodes.keys():
        lat, lon = interpolate_lat_lon(zipcode)
    else:
        lat = zipcodes[zipcode][0]
        lon = zipcodes[zipcode][1]
    weather_data_urls_url = "https://api.weather.gov/points/%s,%s" % (lat, lon)
    logger.info("weather data URL: %s" % weather_data_urls_url)
    headers = {"User-agent": USER_AGENT}
    weather_data_url_raw = requests.get(weather_data_urls_url, headers=headers).text
    logger.info("weather_data_url_raw: %s" % weather_data_url_raw)
    weather_data_url = json.loads(weather_data_url_raw)["properties"]["forecast"]
    logger.info("weather_data_url: %s" % weather_data_url)
    raw_forecast_data_url = weather_data_url[:-9]
    logger.info("raw_forecast_data_url %s" % raw_forecast_data_url)
    raw_forecast_data = requests.get(raw_forecast_data_url, headers=headers).text
    logger.info("broken:::::::::: %s" % raw_forecast_data)
    return raw_forecast_data

def get_weather_api_glossary():
    weather_data_urls_url = "https://api.weather.gov/glossary/"
    logger.info("weather data URL: %s" % weather_data_urls_url)
    headers = {"User-agent": USER_AGENT}
    weather_data_url_raw = requests.get(weather_data_urls_url, headers=headers).text
    logger.info("weather_data_url_raw: %s" % weather_data_url_raw)
    return weather_data_url_raw

def get_most_current_timestamp(list_of_json_objects, current_timestamp):
    """
    for example, if the current_timestamp equals
         2018-09-04T02
    and the list_of_json_objects is:
    [
    {
    "validTime": "2018-09-03T20:00:00+00:00/PT1H",
    "value": 22.222222222222285
    },
    {
    "validTime": "2018-09-03T21:00:00+00:00/PT2H",
    "value": 21.666666666666742
    },
    {
    "validTime": "2018-09-03T23:00:00+00:00/PT1H",
    "value": 21.1111111111112
    },
    {
    "validTime": "2018-09-04T00:00:00+00:00/PT1H",
    "value": 21.666666666666742
    }
    ]

    then give me
    {
    "validTime": "2018-09-03T21:00:00+00:00/PT2H",
    "value": 21.666666666666742
    }
    """
    value_to_return = None
    for each_item in list_of_json_objects:
        if is_timestamp_a_before_b(current_timestamp, each_item["validTime"]):
            value_to_return = each_item
    return value_to_return

def next_dewpoint_lower_than_60(dewpoint_tree, current_timestamp):
    for each_dewpoint in dewpoint_tree:
        each_dewpoint_f = each_dewpoint["value"] * 1.8 + 32
        if each_dewpoint_f <= 60 and not is_timestamp_a_before_b(current_timestamp, each_dewpoint["validTime"]):
            return each_dewpoint
    return None

def is_timestamp_a_before_b(timestamp_a, timestamp_b):
    if seconds_since_the_epoch(timestamp_a) >= seconds_since_the_epoch(timestamp_b):
        return True
    return False

def seconds_since_the_epoch(timestamp):
    if ":" in timestamp:
        timestamp = timestamp.split(":")[0]
    return (datetime.strptime(timestamp, "%Y-%m-%dT%H") - datetime(1970,1, 1)).total_seconds()

def get_proper_dewpoint_output(temp_outside, dewpoint_outside, next_low_dewpoint_object, temperature_tree, zipcode, dewpoint_tree):
    """
    dewpoint object example:
    {
    "validTime": "2018-09-04T00:00:00+00:00/PT1H",
    "value": 21.666666666666742
    }
    """
    if next_low_dewpoint_object:
        next_low_dewpoint_time = next_low_dewpoint_object["validTime"].split(":")[0]
    else:
        next_low_dewpoint_time = None

    to_return = ""
    if temp_outside <= 60:
        return "It may be too cold outside to open the windows. "
    if next_low_dewpoint_object == None:
        return "No moderate humidity days are in the forcast for the next few days.  Try again in a few days to see when you can open your windows. "
    elif dewpoint_outside > 60:
        to_return += "Due to high humidity in your area, it is not advisable to open the windows. "
        if next_low_dewpoint_object != None:
            to_return += "However, by %s " % (get_speakable_time(next_low_dewpoint_time, zipcode))
            temperature_to_return = temperature_at_timestamp(temperature_tree,
                                                             next_low_dewpoint_time, temp_outside)
            to_return += "if your home is hotter than %s degrees Fahrenheit, opening the windows will cool your home. " % int(temperature_to_return)
            next_dewpoint_object_greater_than_60 = next_dewpoint_higher_than_60_after_timestamp(dewpoint_tree, next_low_dewpoint_time)
            if next_dewpoint_object_greater_than_60 != None:
                next_high_dewpoint_timestamp = next_dewpoint_object_greater_than_60["validTime"].split(":")[0]
                speakable_next_high_dewpoint = get_speakable_time(next_high_dewpoint_timestamp, zipcode)
                to_return += "Additionally, on %s, humidity will reach uncomfortable levels.  Consider closing your windows on or before %s. " % (speakable_next_high_dewpoint, speakable_next_high_dewpoint)
    elif dewpoint_outside <= 60:
        temperature_to_return = temperature_at_timestamp(temperature_tree,
                                                         next_low_dewpoint_time, temp_outside)
        to_return += "if your home is hotter than %s degrees Fahrenheit, opening the windows will cool your home. " % int(
            temperature_to_return)
        next_dewpoint_object_greater_than_60 = next_dewpoint_higher_than_60_after_timestamp(dewpoint_tree,
                                                                                            next_low_dewpoint_time)
        if next_dewpoint_object_greater_than_60 != None:
            next_high_dewpoint_timestamp = next_dewpoint_object_greater_than_60["validTime"].split(":")[0]
            speakable_next_high_dewpoint = get_speakable_time(next_high_dewpoint_timestamp, zipcode)
            to_return += "Additionally, at %s, humidity will reach uncomfortable levels.  Consider closing your windows at or before %s. " % (
            speakable_next_high_dewpoint, speakable_next_high_dewpoint)
    to_return += ""
    return to_return

def temperature_at_timestamp(temperature_tree, timestamp, fallback_temp):
    closest_temp = 0
    for each_temperature_object in temperature_tree:
        if not is_timestamp_a_before_b(timestamp, each_temperature_object["validTime"]):
            return closest_temp
        else:
            closest_temp = each_temperature_object["value"] * 1.8 + 32

    return fallback_temp

def get_speakable_time(timestamp_in_utc, zipcode):
    dt = datetime.strptime(timestamp_in_utc.split(":")[0], "%Y-%m-%dT%H")
    datetime_at_timezone = datetime.astimezone(dt.replace(tzinfo=pytz.utc), _get_timezone_from_zipcode(zipcode))
    to_return = datetime_at_timezone.strftime("%A, %B %d at %I %p").split(" at ")[0] + " at " + datetime_at_timezone.strftime("%A, %B %d at %I %p").split(" at ")[1].lstrip("0")
    return to_return

def next_dewpoint_higher_than_60_after_timestamp(dewpoint_tree, timestamp):
    for each_dewpoint in dewpoint_tree:
        each_dewpoint_f = each_dewpoint["value"] * 1.8 + 32
        if each_dewpoint_f >= 61 and not is_timestamp_a_before_b(timestamp, each_dewpoint["validTime"]):
            return each_dewpoint
    return None

def next_dewpoint_lower_than_60(dewpoint_tree, current_timestamp):
    for each_dewpoint in dewpoint_tree:
        each_dewpoint_f = each_dewpoint["value"] * 1.8 + 32
        if each_dewpoint_f <= 60 and not is_timestamp_a_before_b(current_timestamp, each_dewpoint["validTime"]):
            return each_dewpoint
    return None

def _get_timezone_from_zipcode(zipcode):
    for each_item in timezonedata.timezone_map:
        if each_item["zipcode"] == zipcode:
            return pytz.timezone(each_item["tz"])