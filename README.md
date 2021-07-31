# Word Of The Day ReadME! [DISCORD.PY]
Welcome to my Word Of The Day Bot ReadME, written in Python for Discord. [DISCORD.PY](https://github.com/Rapptz/discord.py)
Right below is a quickstart to setting up and running the bot. [QUICKSTART](#quickstart)
Under that is all the technical info. [TECH INFO](#how-it-works)
<img src="https://play-lh.googleusercontent.com/BYoyK1fiFfpH8JTutWAlG_Tqo-Ati-7tLcdYijU-8_L7SQxpuYBo7tzxrzDGXk8JC4hv" width="250" height="250"/>

# Quickstart
To run the bot. Do this.

Settings.json should look like this.
```
{
  "token": "your_token!",
  "channels": "12345,2131,421421",
  "time": "12:00"
}
```
Or something like this.
```
{
  "token": "your_other_token!",
  "channels": "12345",
  "time": "09:05"
}
```
**ANYTHING ELSE WILL NOT WORK!**

## About This

Word of the Day is a discord.py bot that I originally wrote for fun. 
I wanted to learn the advanced side of py with classes and states, while also working with the discord library, to create something I would actually use.
Along the way, I decided it would be good to share it.

<img src="https://i.ibb.co/CBFBDdm/wotdpic.jpg">

*Sound interesting? More information below.*

## Contents

- [How It Works](#how-it-works)
- [How To Launch](#how-to-launch)
- [TODO](#todo)

## How It Works
#### Internal.py
> - Internal works to check the settings file that is required for the bot.
> - If there are any errors with the settings file, we need to inform our user and quit running. 
> - Specifically, we check the file for ['time'], ['channels'], and ['token'] values. If we're missing those or they aren't formatted right, quit.
#### Client.py
> - 


## How To Launch
#### Settings.json
This is what your settings.json should look like.


## TODO
#### What's Next?
So you've made it this far and want to know what's next.
> Truth be told... I don't know either.
