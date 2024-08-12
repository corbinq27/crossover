import requests
import os

url = "https://api.pushover.net/1/messages.json"

def alert_pushover(title, message, PUSHOVER_API_KEY=None, USER_API_KEY=None):
    if os.environ.get("PUSHOVER_API_KEY") is not None:
        PUSHOVER_API_KEY = os.environ.get("PUSHOVER_API_KEY")
    if os.environ.get("USER_API_KEY") is not None:
        PUSHOVER_USER_KEY = os.environ.get("USER_API_KEY")
    return requests.post(url, params=[("title", title), ("message", message), ("token", PUSHOVER_API_KEY), ("user", USER_API_KEY)])

