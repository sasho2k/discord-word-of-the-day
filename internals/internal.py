import os
from os.path import exists
import json
import re

"""" # This file contains the inner checks for the settings file. Also contains helpers."""


# This grabs the token and channel from the settings json file but not before parsing and checking them.
# If there is no settings.json file, then throw a fatal error since these are essential to our bot.
def get_settings():
    path = ""

    if exists("internals/settings.json"):
        path = 'internals/settings.json'
    elif exists(os.getcwd() + "/settings.json"):
        path = os.getcwd() + "/settings.json"
    else:
        print('FATAL: No settings.json file found.\n')
        if exists("example_settings.json"):
            print('FATAL : Replace the example_settings.json with a settings.json file, then fill it with your info.')
        exit(0)

    with open(path) as f:
        json_data = json.load(f)
    f.close()

    token = check_token(json_data)
    channels = check_channels(json_data)
    time = check_time(json_data)
    prefix = check_bot_prefix(json_data)
    if (token is not None) and (channels is not None) and (time is not None) and (prefix is not None):
        print("\t[Send message to channels {0} at time {1}.]\n".format(channels, time))
        return token, channels, time, prefix
    else:
        exit(0)


def check_bot_prefix(json_data):
    if 'bot_prefix' in json_data:
        print("Bot Prefix:", json_data.get('bot_prefix'))

        if json_data.get('bot_prefix').strip() != "":
            return json_data['bot_prefix']
        else:
            print("FATAL: Empty bot prefix value.")
            return None
    else:
        print("FATAL: Missing bot prefix value from settings.json.")
        return None


# Check and see if there is an existing json value for time, then check to see if it empty or not.
# If we run into errors, we shall throw a fatal error.
def check_time(json_data):
    if 'time' in json_data:
        print("Time:", json_data.get('time'))

        if json_data.get('time') != "":
            try:
                if re.search(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$', json_data.get('time')):
                    return json_data['time']
                else:
                    print("FATAL: Error with time value format. Please use 'HH:MM'.")
                    return None
            except:
                print("FATAL: Error with time value format. Please use 'HH:MM'.")
                return None
        else:
            print("FATAL: Empty time value.")
            return None
    else:
        print("FATAL: Missing time value from settings.json.")
        return None


# Check and see if there is an existing json value for token, then check to see if it empty or not.
# If we run into errors, we shall throw a fatal error.
def check_token(json_data):
    if 'token' in json_data:
        print("Token:", json_data.get('token'))
        if json_data.get('token').strip() != "":
            return json_data['token']
        else:
            print("FATAL: Empty token value.")
            return None
    else:
        print("FATAL: Missing token value from settings.json.")
        return None


# Check and see if there is an existing json value for channels. If there is, we need to see if its empty, and
# then we have split it by comma. Then we can begin to parse each 'channel' and see if it is valid. We are solely
# focusing on the format of the strings.
# If we run into errors, we shall throw a fatal error.
def check_channels(json_data):
    if 'channels' in json_data:
        if json_data.get('channels') == "":
            print("FATAL: Empty channel value.")
            return None

        _channels = []

        if isinstance(json_data.get('channels'), list):
            channels = json_data.get('channels')
            for channel in channels:
                try:
                    if channel == "":
                        print("FATAL: Invalid string in 'channel' json.")
                        return None
                    else:
                        _channels.append(int(channel))
                except:
                    print("FATAL: Invalid value in 'channel' json.")
                    return None
            if len(channels) > 1:
                print("Channels:", _channels)
                return _channels
            else:
                return None
        elif isinstance(json_data.get('channels'), str):
            try:
                channel = int(json_data.get('channels'))
                print("Channel:", channel)
                _channels.append(channel)
                return _channels
            except:
                print("FATAL: Invalid value in 'channel' json.")
                return None
    else:
        print("FATAL: Missing channel value from settings.json.")
        return None
