# Word Of The Day
*Welcome to the ReadME of Word Of The Day Bot, written in Python for Discord. [DISCORD.PY](https://github.com/Rapptz/discord.py)*

*Directly below is a quickstart to setting up and running the bot. [GETTING STARTED](#getting-started)*

<img src="https://i.giphy.com/media/3orifg4eeMqIhe66uk/200.webp" width="600" height="500"/>

# Contents

- [About This Project](#about-this-project)
- [Getting Started](#getting-started)
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

<img src="https://i.ibb.co/CBFBDdm/wotdpic.jpg"/>

*Sound interesting? More information below.*

# Getting Started

<img src="https://media2.giphy.com/media/S8ToH7Zt8gZ4u2iClh/giphy.gif?cid=790b7611c6abe40f441eaae2e8ecde692aefbe4a433ecb0e&rid=giphy.gif&ct=g" width="400" height="400">

Getting the bot running is fairly simple. It just requires you to have python and the discord.py library downloaded to your machine. From there, you can clone/download the repository and get your own version working!.

*A simple test-run of the program!*

<img src="https://i.ibb.co/2skJCpy/Capture.jpg" width="600" height="150"/>

# Settings JSON
The settings file is where your bot will hold its sensitive info upon launch.
It is very important to be familiar with what to insert into the JSON's values and how it will affect the program.
This is what your settings.json should look like when you are preparing to run the bot.

```JSON
{
  "token": "your_token!",
  "channels": ["12345","2131","421421"],
  "time": "12:00"
}
```
Or something like this.
```JSON
{
  "token": "your_other_token!",
  "channels": "12345",
  "time": "09:05"
}
```

**Key's and their Designated Values**
- `Token` *Holds the token associated with your bot's login.*
- `Channels` *Can hold either a list of channels or a single channel.*
- `Time` *Holds a military-standard time.*

> These are the **Rules** for how the file should be structured.
> - All keys must be in lowercase.
>   - e.g... `token`, `channels`, `time` and not `Token`, `TIME`, or `ChAnNeLs`.
> - `token` field must be a string value. *Preferably containing the token field so we can login.*
> - `channels` field can be a list or a single int.
>   - If of type list, then it must be structured like ['123','456','789'].
> - `time` field **MUST** be a string of format "HH:MM".

**THIS IS WHAT YOUR SETTINGS.JSON SHOULD NOT LOOK LIKE!**
```JSON
{
  "Token": "your_token!",
  "channels": [12345,2131,421421],
  "TIME": "9"
}
```

*And if you are unsure why, please scroll back [up](#settings-json).*

# How It Works
This is a general explanation for the processes and thoughts behind each file in the program.
*More can be found in the comments of the program.*
#### [Internal.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/internal.py)
> Internal works to check the settings file that is required for the bot.
>
> If there are any errors with the settings file, such as missing or unformatted values, we need to inform our user and quit running. The same is true if the file is missing. 
>
> We check the file specifically for the ['time'], ['channels'], and ['token'] values. 
>
> We can then return the values to our client and setup an instance with the settings.

#### [Client.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/client.py)
> Client holds all the functions and classes that help the bot work at a server level without crashing on errors. 
>
> Specifically, client will hold the MyClient class. The class is initialized after a run through internal and has its variables set to the settings.
> These variables would be `today_date`, `desired_time`, `daily_sent`, and `desired_channel`.
>
> `Today_date` is set automatically when the bot is ran, there is no setting this variable. 
> The same will go for `daily_sent`, and this is because these two variables work to help the bot know when to send off a daily message.
> 
> On the ready of the bot, we can launch our two tasks `check_date()` and `grab_daily_word()`. `check_date()` will work to loop every 30 minutes to check the current date versus the date saved in the Client class, and will let us know if today is a new day by setting `daily_sent` to false. `grab_daily_word()` will check every 15 seconds if the `daily_sent` has is false **AND** if the time is equal to the `desired_time`, and if both are true, we can send our message across our channels.
#### [Job.py](https://github.com/sasho2k/discord-word-of-the-day/blob/master/job.py)
> Job holds functions and classes needed to scrape and retrieve the word of the day from the target website. *Wordnik daily word of the day vs. Wordnik word of the day archive.*
>
> The task of `word_of_the_day()` is to retrieve the word of the day via helper functions and return one of two things; A error code or a word_of_the_day object (Also declared here in job.py).
>
> *Error codes*
> - 200 =  Did not receive 200 response from request.
> - 201 =  Did not find the 'Word' section of Word Of The Day.
> - 202 =  Did not find the 'Definition' and 'Part Of Speech' section/s of Word Of The Day
>
> `handle_and_send()` serves to build the message/messages we want to return to our client to send. Sometimes the length of a message is greater than 2000, which is the standard length for discord, so we must split the message in a way that is visually appealing. That is where the handle_long_message function will come in and will return us a list of messages to send.
> *Very rarely, there is an error where it will return None because we have ran into a message with a length greater than 4000, or two messages. This is honestly because I got lazy and just limited the number of examples to be 5.*
 
# TODO
**Current TODO List.**
```
... 
```
#### What's Next?


### Contact
> If you run into any issues, have any questions, or just want to chat. 
> Discord: `sasho2k#1600`
