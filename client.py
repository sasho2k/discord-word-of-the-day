import discord
from discord.ext import tasks
from internal import *
from job import *

"""
# This file will be the top layer of our program. We can keep it simple with a single class and run() function.
# All supporting functions are imported from our other files.

"""


# This is our client class.
class MyClient(discord.Client):
    # Set the states on initialization.
    today_date = ""
    daily_sent = False
    desired_time = ""
    desired_channels = []

    # The simple on-ready function where our tasks will live.
    async def on_ready(self):
        print('CLIENT: Logged on and running as {0}.\n'.format(self.user))
        self.check_date.start()
        self.grab_daily_word.start()

    # Check to see if the current date has changed. If it has, then we have not sent a daily word and we must
    # set our daily sent flag to False while replacing the self.date with the current date.
    @tasks.loop(minutes=30)
    async def check_date(self):
        if datetime.now().strftime("%d") != self.today_date:
            print('CLIENT: Changing self.today_date from {0} to {1}\n'.format(self.today_date, datetime.now().strftime("%d")))
            self.today_date = datetime.now().strftime("%d")
            if not self.daily_sent:
                self.daily_sent = False

    # Check if our daily message has been sent. If not, check to see if it is the required time.
    # [We check over the 15 second interval to have maximum 4 chances to match our current time and our desired time.]
    # If it is time to send off our message, call our helper function and set our sent_flag to True for the day.
    @tasks.loop(seconds=15)
    async def grab_daily_word(self):
        if not self.daily_sent:
            if datetime.now().strftime("%H:%M") == self.desired_time:
                await self.send_word()
                self.daily_sent = True

    # Grab our message from helper function then check if we must send to a list of channels or a single one. Depending
    # on the type, we have to loop through the list, but the process in each loop is the same as a single instance;
    # Grab the channel, check if it is empty, if not then check if we must send a single message or multiple, then send!
    async def send_word(self):
        msg = wotd_flow()

        if isinstance(self.desired_channels, int):
            channel = self.get_channel(self.desired_channels)
            if not channel:
                print("FATAL: No channel found with ID {0} in settings.\n".format(channel))
                return
            if isinstance(msg, list):
                for message in msg:
                    print("CLIENT : Message sent to channel {0}.\n".format(channel))
                    await channel.send(message)
            else:
                print("CLIENT : Message sent to channel {0}.\n".format(channel))
                await channel.send(msg)
        elif isinstance(self.desired_channels, list):
            for _channel in self.desired_channels:
                channel = self.get_channel(_channel)
                if not channel:
                    print("FATAL: No channel found with ID {0} in settings.\n".format(channel))
                    continue
                if isinstance(msg, list):
                    for message in msg:
                        print("CLIENT : Message sent to channel {0}.\n".format(channel))
                        await channel.send(message)
                else:
                    print("CLIENT : Message sent to channel {0}.\n".format(channel))
                    await channel.send(msg)
        print('CLIENT: send_word complete.\n')

    # This will handle custom messages the user can send to the bot.
    # TODO : Implement a function to request previous WOTD. (Must pass parameter to get request in job.py)
    # TODO : Implement a function to set the desired time
    # TODO : Implement a function to set the sending channel/s
    # TODO : Implement a function for users to sign up to be DM'ed.
    async def on_message(self, message):
        if message.author == self.user:
            return


# Function serves to simplify and beautify the send_word task in the MyClient class by performing word_of_the_day
# then collecting and checking its output to return the final msg that should be sent across the channels.
# Uses the current date for thr request.
# 200 = "`ERROR -> BAD REQUEST URL`"
# 201 = "`ERROR -> ERROR WITH WORD GRAB`"
# 202 = "`ERROR -> ERROR WITH DEFINITION/PART OF SPEECH GRAB`"
def wotd_flow():
    wotd = word_of_the_day([datetime.now().strftime("%Y"),
                            datetime.now().strftime("%m"),
                            datetime.now().strftime("%d")])
    if wotd == 200:
        msg = "`ERROR -> BAD REQUEST URL`"
    elif wotd == 201:
        msg = "`ERROR -> ERROR WITH WORD GRAB`"
    elif wotd == 202:
        msg = "`ERROR -> ERROR WITH DEFINITION/PART OF SPEECH GRAB`"
    elif isinstance(wotd, WordOfTheDay):
        msg = handle_and_send(wotd)
        if not msg:
            msg = "`ERROR -> LENGTH/METHOD ISSUE`"

    return msg


# Our main function. We can initialize the client, grab our settings, and then run the bot.
# Token contains our token, channels contains a list/int depending on num of channels, time contains desired time.
# Today date is something we set on initialization of the bot. Wouldn't make sense to be able to init at a given date.
# If we run into any errors along the way, we can print them and exit the program.
def run():
    client = MyClient()
    token, channels, time = get_settings()
    client.desired_channels = channels
    client.desired_time = datetime.now().strftime("%H:%M") # time
    client.today_date = datetime.now().strftime("%d")

    try:
        print("CLIENT: Starting run process.\n")
        client.run(token)
    except discord.errors.HTTPException:
        print("FATAL: Invalid token.\n")
        exit(0)
    except discord.errors.LoginFailure:
        print("FATAL: Invalid token.\n")
        exit(0)
