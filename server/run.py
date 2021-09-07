from internals.internal import *
from server.client import *

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
    client.today_date = datetime.now(tz=client.timezone).strftime("%d")
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
