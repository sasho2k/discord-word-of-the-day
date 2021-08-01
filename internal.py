import os
import json
import re


"""" # This file contains the inner checks for the settings file. """


# This grabs the token and channel from the settings json file but not before parsing and checking them.
# If there is no settings.json file, then throw a fatal error since these are essential to our bot.
def get_settings():
    if not os.path.exists('settings.json'):
        print('FATAL: No settings.json file found in your directory.\n')
        exit(0)

    with open('settings.json') as f:
        json_data = json.load(f)
    f.close()

    token = check_token(json_data)
    channels = check_channels(json_data)
    time = check_time(json_data)
    if (token is not None) and (channels is not None) and (time is not None):
        print("\t[Send message to channels [{0}] at time {1}.]\n".format(channels, time))
        return token, channels, time
    else:
        exit(0)


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
        if json_data.get('token') != "":
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

        if isinstance(json_data.get('channels'), list):
            channels = json_data.get('channels')
            _channels = []
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
                return channel
            except:
                print("FATAL: Invalid value in 'channel' json.")
                return None
    else:
        print("FATAL: Missing channel value from settings.json.")
        return None
