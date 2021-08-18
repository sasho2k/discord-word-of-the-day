from datetime import *
import discord
from discord.ext import tasks
from internals.internal import *
from workers.job import *

"""
# This file will be the top layer of our program. We can keep it simple with a single class and run() function.
# All supporting functions are imported from our other files.

"""


# This is our client class.
class MyClient(discord.Client):
    # Set the states on initialization.
    bot_prefix = ""
    today_date = ""
    daily_sent = False
    desired_time = ""
    desired_channels = []
    user_dm_list = []

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
            print('CLIENT: Changing self.today_date from {0} to {1}\n'.format(self.today_date,
                                                                              datetime.now().strftime("%d")))
            self.today_date = datetime.now().strftime("%d")
            if self.daily_sent:
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
        msg = wotd_flow(None)

        # This will be the flow for sending to desired_channels.
        for _channel in self.desired_channels:
            channel = self.get_channel(_channel)
            if not channel:
                print("FATAL: No channel found with ID {0} in settings.\n".format(_channel))
                continue
            if isinstance(msg, list):
                i = 1
                for message in msg:
                    await channel.send(message)
                    print("CLIENT : Message {1} sent to channel {0}.\n".format(channel, i))
                    i += 1
            else:
                print("CLIENT : Message sent to channel {0}.\n".format(channel))
                await channel.send(msg)

        # This is the user DM flow.
        for user_dm in self.user_dm_list:
            try:
                user = await self.fetch_user(user_dm)
            except:
                print("FATAL: No user found with ID {0} in settings.\n".format(user_dm))
                continue

            if isinstance(msg, list):
                i = 1
                for message in msg:
                    await user.send(message)
                    print("CLIENT : Message {1} sent to user {0}.\n".format(user_dm, i))
                    i += 1
            else:
                print("CLIENT : Message sent to user {0}.\n".format(user_dm))
                await user.send(msg)

        print('CLIENT : send_word complete.\n')

    # This will handle custom messages the user can send to the bot.
    # signup handles the event of a user joining the user DM list.
    # todo -> These implementations would require the use of a role system or something to make sure random people
    #  aren't able to change the time's and channels. This would be a little daunting though so we can keep these
    #  settings in the JSON file on launch. Sorry!
    # TODO : Implement a function to set the desired time through the channel.
    # TODO : Implement a function to set the sending channels. User will input (botprefix + "setchannel") and will add
    #        current channel to desired_channels list.
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(self.bot_prefix + "help"):
            embedVar = discord.Embed(title="Here to Help!",
                                     description="This is a current list of all available functions in the __Word of the Day__ bot.",
                                     color=0x607d8b)
            embedVar.set_author(name="Word of the Day Help.", url="https://github.com/sasho2k/discord-word-of-the-day.")
            embedVar.set_footer(text="If you have more questions, please visit the GitHub hyperlink at the top!")
            embedVar.set_thumbnail(url="https://i.ibb.co/GMbg90n/wotd.png")
            embedVar.add_field(name="{0}signup".format(self.bot_prefix),
                               value="Use this to sign-up for a DM from the bot at {0} everyday!\n"
                                     "*This will be customizable soon!*".format(self.desired_time), inline=False)
            embedVar.add_field(name="{0}getword YYYY/M/D".format(self.bot_prefix),
                               value="Use this to get an archive word from the day you request!\n"
                                     "The beginning of the archive is 2011/2/14.\n\n"
                                     "*Enter in date form [2000/6/5] or [2000/08/02]. The year must be "
                                     "4 digits long, but month and date can be double digit if single "
                                     "(i.e 08 for 8). Regular rules apply for double digit days (14).*", inline=False)
            await message.channel.send(embed=embedVar)

        if message.content.startswith(self.bot_prefix + "signup"):
            for user in self.user_dm_list:
                if message.author.id == user:
                    print("FATAL : User [id: {0}, name: {1}] is already signed up.\n".format(user, message.author.name))
                    await message.channel.send("```ERROR -> YOU HAVE ALREADY SIGNED UP```")
                    return
            self.user_dm_list.append(message.author.id)
            user = await self.fetch_user(message.author.id)

            embedVar = discord.Embed(title="DM Request Received!",
                                     description="",
                                     color=0x607d8b)
            embedVar.set_author(name="Word of the Day Signup.")
            embedVar.set_footer(text="If you have any concerns with the time, please contact the owner of the server."
                                     "They will be able to speak to whoever setup the time.")
            embedVar.set_thumbnail(url="https://i.ibb.co/GMbg90n/wotd.png")
            embedVar.add_field(name="{0}signup".format(self.bot_prefix),
                               value="Thank you for signing up Word of the Day DM's at {0} everyday!\n"
                               .format(self.desired_time), inline=False)
            await user.send(embed=embedVar)

            print("CLIENT : Sign up detected, User DM\'ed. New user DM list: {0}\n".format(self.user_dm_list))

        if message.content.startswith(self.bot_prefix + "getword"):
            try:
                r_date = message.content.split(self.bot_prefix + "getword")[1].strip().split('/')

                if (((int(r_date[0]) >= 2011) & (int(r_date[0]) <= int(datetime.now().strftime("%Y"))))
                        & ((int(r_date[1]) >= 1) & (int(r_date[1]) <= 12))
                        & ((int(r_date[2]) >= 1) & (int(r_date[2]) <= 31))):
                    print("Sending wotd request with date " + r_date[0] + '/' + r_date[1] + '/' + r_date[2] + '\n')
                    msg = wotd_flow(r_date)

                    if isinstance(msg, list):
                        i = 1
                        for message in msg:
                            await message.channel.send(message)
                            print("CLIENT : Message {1} sent to channel {0}.\n".format(message.channel, i))
                            i += 1
                    else:
                        print("CLIENT : Message sent to channel {0}.\n".format(message.channel))
                        await message.channel.send(msg)
                else:
                    await message.channel.send("```ERROR -> INVALID DATE CONSTRAINTS.```")
            except:
                print("FATAL : Error parsing message for getword.\n")
                return


# Our main function. We can initialize the client, grab our settings, and then run the bot.
# Token contains our token, channels contains a list/int depending on num of channels, time contains desired time.
# Today date is something we set on initialization of the bot. Wouldn't make sense to be able to init at a given date.
# Bot prefix is the prefix you would like to assign to your bot.
# If we run into any errors along the way, we can print them and exit the program.
def run():
    client = MyClient()
    print("\nStarting Process...\n")
    token, channels, bot_time, bot_prefix = get_settings()
    client.desired_channels = channels
    client.desired_time = bot_time  # datetime.now().strftime("%H:%M")
    client.today_date = datetime.now().strftime("%d")
    client.bot_prefix = bot_prefix

    try:
        print("CLIENT: Starting run process.\n")
        client.run(token)
    except discord.errors.HTTPException:
        print("FATAL: Invalid token.\n")
        exit(0)
    except discord.errors.LoginFailure:
        print("FATAL: Invalid token.\n")
        exit(0)
