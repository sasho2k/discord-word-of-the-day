# Word Of The Day
*Welcome to the ReadME of Word Of The Day Bot, written in Python for Discord using [discord.py](https://github.com/Rapptz/discord.py)!*

*Directly below is a quickstart to setting up and running the bot. Start here unless you want to find out some more about the project and how it will look in Discord!*
*[Get Started!](#getting-started)*

**Please note this is a work in progress and there might be errors. Feel free to reach out to me if you find any issues.**

<img src="https://i.giphy.com/media/3orifg4eeMqIhe66uk/200.webp" width="600" height="500"/>

# Contents

- [Getting Started](#getting-started)
- [Commands](#commands)
- [Settings JSON](#settings-json)
- [How It Works](#how-it-works)
- [TODO](#todo)
- [Contact](#contact)

# About This Project

Word of the Day is a discord.py bot that I originally wrote for fun. I wanted to learn the advanced side of py with classes and states, while also working with the discord library, to create something I would actually use on a day to day basis. Along the way, I decided it would be good to share it for the purpose of open-source software. 

*I would like to first and formally thank Wordnik for their services, their easy-to-use link system to navigate archives, and for not cluttering the HTML with random tags and links.*

This is an example of what a standard message from the bot would be like on a daily basis.
> - `Word of the Day` followed by the current date.
> - Actual `word of the day` pulled from [wordnik](https://www.wordnik.com/word-of-the-day/).
> - `Numbered collection of definitions` along with their respective part of speech.
> - `Numbered collection of examples` along with their respective sources and links.
>   - Sometimes there will be no examples. This is not an issue with the bot but with the site not having any examples available.
>   - Links provided formatted to save space at the bottom of the message.
> - `Link to webpage` that was scraped to retrieve the information along with a shout-out to Wordnik.

<img src="https://i.ibb.co/pZhVxdZ/wotdJPG.jpg" height="600"/>

> **This is what the bot help embed would display upon request.**

<img src="https://i.ibb.co/8cy8F1r/help.jpg" width="700" height="400">

>*Sound interesting? More information below.*

# Getting Started

<img src="https://media2.giphy.com/media/S8ToH7Zt8gZ4u2iClh/giphy.gif?cid=790b7611c6abe40f441eaae2e8ecde692aefbe4a433ecb0e&rid=giphy.gif&ct=g" width="400" height="400">

Getting the bot running is fairly simple. It just requires you to have python and the discord.py library downloaded to your environment. From there, you can clone/download the repository and get your own version working! It will also require you to make a `settings.json` file to hold all the info your bot will need. More information can be found at [settings.json](#settings-json).

> To be able to fill in the required JSON to your needs and to launch the bot, you need a token, a Discord channel id *(or even multiple if you want!)* to send our word to, a bot prefix, and a desired time to send your word of the day.
> 
> If you aren't sure where to get a token for your bot from, please see [this](https://discord.com/developers).
> You will be prompted to login into Discord and setup an application. Please feel free to look around [here](https://discord.com/developers/docs/intro) if you are unfamiliar with any of this.
> 
> Also, you can grab channel ID's by right-clicking over a Discord channel and copying it's ID. *(Be mindful you must have developer mode turned on in Discord.)*
> 
> The bot prefix is how you will use the bot commands so make sure you dedicate a prefix you will remember and will not interfere with other bots or chat messages.

After you've setup your application on the Discord Developer side, you'll want to generate an invite for your bot.
I would recommend using [this](https://discordapi.com/permissions.html) site to do so, and setting the permissions to admin. 

> **NOTE**: *You can set your specific permissions if you would like but I am very lazy. Sorry.*

Once the bot is in the Discord server, you can run the main file from your local environment, or via a server, to launch the bot.
Running the bot is as simple as a one line command.
```bash
py main.py
```
*This might not be a 100% step by step explanation so feel free to google your way around some things. Otherwise, you should be good to go after these steps.*

Now that the bot is in the server, and you ran it, the status of the bot should go from offline to online.

<img src="https://i.ibb.co/mtLZ3tG/wotdonline-JPG.jpg">

There you go! You've got the bot setup in your server.

If you want to see all the cool features, check out the list of [commands](#commands) for the bot.

*If you're interested in a list of future features in more detail, be sure read all the way to [TODO](#TODO) section and also **star** the repository!*

#### *A simple test-run of the program!*

<img src="https://i.ibb.co/zGpTMp4/running.jpg" width="600" height="150"/>

# Commands
The bot can accept commands through the channel in accordance with your bot prefix:

> **BOT_PREFIX** = $
> 
> *Realistically, the bot prefix can be anything you want. It can be #, &, -, _, <, >, /, ?, :, ;, etc...
In our case, for the sake of examples, we can set it to $.*
>
> **Commands**
> - $help
> - $getword DATE
> - $signup

`getword` will access the archive and search for the word of the day on your requested date.

> *Regarding the date formatting when using `getword`...*
> 
> Date format for getword is [2000/6/5] or [2000/08/02]. 
>
>The year must be 4 digits long, but month and date can be double digit if single (i.e 08 for 8). 
> 
>Regular rules apply for double digit days (14).

`help` will return an embed that will remind you of the list of commands and how to access them. 
*It will also include the bot prefix, that you have assigned via the settings, behind every command so users know EXACTLY how to access them.*

`signup` will sign the current user up to receive daily messages from the bot at the desired time set by the server.

*This is because our client can only hold one desired time, and cannot hold desired times for separate users.* 

**Possible update?**

# Settings JSON
The settings file is where your bot will hold its sensitive info upon launch.
It is very important to be familiar with what to insert into the JSON's values and how it will affect the program.

This is what your settings.json should look like when you are preparing to run the bot.

```json
{
  "token": "your_token!",
  "channels": ["12345","2131","421421"],
  "time": "12:00",
  "bot_prefix": "$"
}
```
Or something like this.

```json
{
  "token": "your_other_token!",
  "channels": "12345",
  "time": "09:05",
  "bot_prefix": "-"
}
```

**Key's and their Designated Values**
- `Token` - *Holds the token associated with your bot's login.*
- `Channels` - *Can hold either a list of channels or a single channel.*
- `Time` - *Holds a military-standard time.*
- `Bot_Prefix` - *Holds the prefix the bot will use.*

> These are the **Rules** for how the file should be structured.
> - All keys must be in lowercase.
>   - e.g... `token`, `channels`, `time` and not `Token`, `TIME`, or `ChAnNeLs`.
> - `token` field must be a string value. *Preferably containing the token field so we can login.*
> - `channels` field can be a list or a single int.
>   - If of type list, then it must be structured like ['123','456','789'].
> - `time` field **MUST** be a string of format "HH:MM".
> - `bot_prefix` field must contain some type of character sequence. ('$', '-', '&', '@', '#')

**THIS IS WHAT YOUR SETTINGS.JSON SHOULD NOT LOOK LIKE!**
```json
{
  "Token": "your_token!",
  "channels": [12345,2131,421421],
  "TIME": "9",
  "botprefix": " "
}
```

*And if you are unsure why, please scroll back [up](#settings-json).*

# How It Works
This is a general explanation for the processes and thoughts behind each file in the program.

*More can be found in the comments of the program.*

## Structure

The folder names portray the task/s of the file/s in them.

>'Internals' holds files pertaining to the user manipulation of the internal state of the program through JSON.
> 
>  📁 = [internals](https://github.com/sasho2k/discord-word-of-the-day/tree/master/internals)
>
>  📁 -> [internal.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/internals/internal.py)
>
>  📁 -> [settings.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/example_settings.json)

> 'Server' holds files that contain functions and classes for the automation of the Discord client and server.
>
> 📁 = [server](https://github.com/sasho2k/discord-word-of-the-day/tree/master/server)
>
> 📁 -> [client.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/server/client.py)
>
> 📁 -> [run.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/server/run.py)

> 'Workers' holds all data retrieval and packaging functions and classes relevant to the word of the day. 
>
> 📁 = [workers](https://github.com/sasho2k/discord-word-of-the-day/tree/master/workers)
> 
> 📁 -> [job.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/server/job.py)
>
> 📁 -> [word_of_the_day.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/workers/word_of_the_day.py)

## Files

#### [Internal.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/internals/internal.py)
> Internal works to check the settings file that is required for the bot.
> 
> It specifically checks for the existence of a [settings.json file](https://github.com/sasho2k/discord-word-of-the-day/blob/master/example_settings.json) 
> in either the 📁 internal directory, or the actual project directory.
>
> If there are any errors with the settings file, such as missing or unformatted values, we need to inform our user and quit running. The same is true if the file is missing. 
>
> We check the file specifically for the ['time'], ['channels'], ['token'], and ['bot_prefix'] values. 
>
> We can then return the values to our client and setup an instance with the settings.

#### [Client.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/server/client.py)
> Client holds all the functions that help the bot work at a server level without crashing on errors. 
> [Run.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/server/run.py) will hold the process to start running the client.
>
> Specifically, client will hold the MyClient class. The class is initialized after a run through internal and has its variables set to the settings.
> These variables would be `today_date`, `desired_time`, `daily_sent`, and `desired_channel`.
>
> `Today_date` is set automatically when the bot is ran, there is no setting this variable. 
> The same will go for `daily_sent`, and this is because these two variables work to help the bot know when to send off a daily message.
> 
> On the ready of the bot, we can launch our two tasks `check_date()` and `grab_daily_word()`. `check_date()` will work to loop every 30 minutes to check the current date versus the date saved in the Client class, and will let us know if today is a new day by setting `daily_sent` to false. `grab_daily_word()` will check every 15 seconds if the `daily_sent` has is false **AND** if the time is equal to the `desired_time`, and if both are true, we can send our message across our channels.
> 
> We will also handle for three types of messages coming from the chat: 1. `signup`, 2. `help`, and 3. `getword`. The `BOT_PREFIX` will be the predecessor to all these message types. `signup` will add the user to the bot user DM list to receive DM's at the desired time with the Word of the Day. `help` will hold all info about the available functions. `getword` will be used to access the Word of the Day archive and request previous words.
#### [Job.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/workers/job.py)
> Job holds functions needed to scrape and retrieve the word of the day from the target website. 
> [Word_of_the_day.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/workers/word_of_the_day.py) holds the data object needed for our functions.
>
> The task of `word_of_the_day()` is to retrieve the word of the day via helper functions, `return_wotd_objectt()` being the main one, and return one of two things; A error code or a `word_of_the_day` object (Also declared here in job.py).
> This function also takes in a date, which is normally set to the current date in order to get the current word of the day. Users are able to request a previous word of the day via the chat *(if they supply a valid date of course)*.
> 
> The request made in `word_of_the_day()` to the wordnik website has custom headers to spoof the request. 
> ```
> headers = {
>        "Accept": "*/*",
>        "Accept-Language": "en-US,en;q=0.5",
>        "Connection": "keep-alive",
>        "Host": "www.wordnik.com",
>        "Referer": url,
>        "Sec-Fetch-Dest": "empty",
>        "Sec-Fetch-Mode": "cors",
>        "Sec-Fetch-Site": "same-origin",
>        "TE": "trailers",
>        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
>    }
> ```
> *I honestly believe they added this after I pinged their API an excessive amount, so they're taking measures to secure the request.
> This was solved by adding a few headers. We'll see what else they have to come.*
>
> *Error codes*
> - 200 =  Did not receive 200 response from request.
> - 201 =  Did not find the 'Word' section of Word Of The Day.
> - 202 =  Did not find the 'Definition' and 'Part Of Speech' section/s of Word Of The Day
>
> `handle_and_send()` serves to build the message/messages we want to return to our client to send. Sometimes the length of a message is greater than 2000, which is the standard length for discord, so we must split the message in a way that is visually appealing. That is where the handle_long_message function will come in and will return us a list of messages to send.
>
> `wotd_flow(date)` serves to make the entire process of receiving a date, checking its return value when passed to `word_of_the_day()`, and returning a message, *or list of messages*, to send to the channel/user, easier by holding all the error checks and parameters needed for these separate processes.
> 
> *Very rarely, there is an error where it will return None because we have ran into a message with a length greater than 4000, or two messages. This is honestly because I got lazy and just limited the number of examples to be 5.*
 
# TODO
**Current TODO List.**
```
... -> Add ability to set desired time from chat 
       [This requires use of roles].
... -> Add ability to set sending channels 
       [This requires use of roles].
... -> Add ability to sign users up for DMs at a specific time. 
       [This could be a possible memory/time issue if the list is too big, may require searching algorithms]
... -> Add ability to send a dynamic and visually appealing message that is over 4000 characters long.
       [This will be per request. Too much time for something so pointless.]
```

# Contact
> If you run into any issues, have any questions, or just want to chat. 
> Discord: `sasho2k#1600`

##### So What Now?
> No clue. Thanks for getting this far though. Hopefully you enjoyed reading this and learned a lot.
