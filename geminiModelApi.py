import alerter_loop


def set_zip_code(zipcode:int):
    """Given a chat prompt, retrieve the ZIP code.  Do not guess at the zip code! find it within the given response.

    Args:
        zipcode: A standard 5-digit zip code for the united states as an integer.

    Returns:
        A dictionary containing the set ZIP code.
    """
    from main import GLOBAL_SESSION
    user_list = alerter_loop.user
    for each_index in range(len(user_list)):
        if "SESSION" in user_list[each_index]:
            if user_list[each_index]["SESSION"] == GLOBAL_SESSION:
                user_list[each_index]["zipcode"] = str(int(zipcode))
    return {
        "zipcode": zipcode
    }

def set_pushover_api_keys(PUSHOVER_API_KEY:str, USER_API_KEY:str):
    """Given a chat prompt, retrieve the PUSHOVER_API_KEY and the USER_API_KEY both necessary for the usage of the
    pushover API. Do not guess at the PUSHOVER_API_KEY or the  USER_API_KEY! find it within the given response.

    Args:
        PUSHOVER_API_KEY: A string of the Pushover API key needed to interact with the pushover API.  It will be about 30 characters in length and made up of lowecase letters and numbers.
        USER_API_KEY: A string of the user's pushover API key needed to interact with the pushover API. It will be about 30 characters in length and made up of lowecase letters and numbers.

    Returns:
        A dictionary containing the two values.
    """
    from main import GLOBAL_SESSION
    user_list = alerter_loop.user
    for each_index in range(len(user_list)):
        if "SESSION" in user_list[each_index]:
            if user_list[each_index]["SESSION"] == GLOBAL_SESSION:
                user_list[each_index]["PUSHOVER_API_KEY"] = str(PUSHOVER_API_KEY)
                user_list[each_index]["USER_API_KEY"] = str(USER_API_KEY)

    return {
        "PUSHOVER_API_KEY": PUSHOVER_API_KEY,
        "USER_API_KEY": USER_API_KEY
    }

def set_conditional(weather_condition:str, less_than_or_greater_than:str, target_temperature:int):
    """Given a chat prompt, retrieve the weather_condition, less_than_or_greater_than, and the target_temperature.
    The underlying program uses this to notifiy the user when the given weather condition is less than or greater than
    the target temperature.  Do not guess at the conditional!

    Args:
        weather_condition: This must either be the string "dewpoint" or "temperature". all other values are reprompted for.
        less_than_or_greater_than: must be either the ">" sign or the "<" sign.
        target_temperature: an integer number of degrees fahrenheit

    Returns:
        A dictionary containing all three values.
    """
    from main import GLOBAL_SESSION
    user_list = alerter_loop.user
    for each_index in range(len(user_list)):
        if "SESSION" in user_list[each_index]:
            if user_list[each_index]["SESSION"] == GLOBAL_SESSION:
                if weather_condition.lower() == "dewpoint":
                    if less_than_or_greater_than == "<" or less_than_or_greater_than == ">":
                        alerter_loop.set_condition(each_index, alerter_loop.WeatherVariable.DEWPOINT, (less_than_or_greater_than, int(target_temperature)))
                else:
                    if weather_condition.lower() == "temperature":
                        if less_than_or_greater_than == "<" or less_than_or_greater_than == ">":
                            alerter_loop.set_condition(each_index, alerter_loop.WeatherVariable.TEMPERATURE,
                                                       (less_than_or_greater_than, int(target_temperature)))

    return {
        "weather_condition": weather_condition,
        "less_than_or_greater_than": less_than_or_greater_than,
        "target_temperature": target_temperature

    }