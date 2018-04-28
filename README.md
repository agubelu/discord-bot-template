

# Discord bot template
## tl;dr
This is a code template that will help you build a Discord bot in a quick and elegant way. You just have to tweak a few settings to your liking, add your commands, and you'll be ready to go.

Adding new commands or temporal events is as simple as inheriting from an abstract class, which helps to keeping everything clean and simple.

Check [example_command.py](https://github.com/agubelu/discord-bot-template/blob/master/commands/example_command.py) and [example_event.py](https://github.com/agubelu/discord-bot-template/blob/master/events/example_event.py) for an example on how to implement commands and events, or keep reading for more detailed info.

## Pre-requisites
- Python >= 3.6 (though you can use 3.5 if you remove the [f-strings](https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep498))
- You need to [register your bot and get a Discord API token](https://discordapp.com/developers/applications/me).
- You should be at least familiar with Python 3 and with the basics of the [discord.py](https://github.com/Rapptz/discord.py) [(docs)](https://discordpy.readthedocs.io/en/latest/) library.
- You should also have some basic knowledge about what asynchronous programming is and [how it works in Python](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/), but to be fairly honest you don't really have to in order to make this thing work. You can just throw in `async` or `await` whenever Python complains.
- You should know what a `virtualenv` is and how to set up one. Check [this](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) out if the file name `requirements.txt` doesn't speak to you.


# Basic settings
You can edit the following parameters in the `settings.py` file:
- **COMMAND_PREFIX**: The prefix that will be used for all commands. It's a `!` by default, but you can change it to anything else. It doesn't have to be a single-character prefix.
- **BOT_TOKEN**: The private token for your bot. Make sure to keep it secret. I usually put it in an environment variable, but whatever works for you.
- **NOW_PLAYING**: The text that the bot will display as its now playing status. You can set it to anything *falsy* (`""`, `None`, `False`, ...) to disable it.
- **BASE_DIR**: This isn't really a setting, but you can use to build relative paths inside your code. It points to the directory where the settings file itself is stored.

# Running your bot
Just run `python your_bot.py` and everything should work just fine if all dependencies are met. Of course, you can rename `your_bot.py` to anything you want.

# Adding commands
Having all of your commands in a single file (or maybe even a single *switch*) gets ugly quickly as you start adding commands. We all know it makes for messy, often redundant code.

However, this template aims to simplify that process by letting you add new commands to your bot by just creating new files in the `commands` directory. It keeps everything simple and modularized, and allows you to focus in whatever you want your bot to do, without having to worry about the pre-processing steps needed to parse commands.
## How to add a new command
Let's say you want to create a `!random` command that allows your users to roll a random number between a lower and an upper bound. We'll see how:

### 1. Add a new file to the `commands` directory
You can name it any way you want, but you probably want to give it a meaningful name. So, we'll start by adding a `random_number.py` file.

### 2. Define a new command class in that file
Now that you've created a file for the new command, you have to create a new class **that inherits from BaseCommand**, just like this:
```python
from commands.base_command import BaseCommand

class Random(BaseCommand):
    def __init__(self):
        ...  # TO-DO

    async def handle(self, params, message, client):
        ...  # TO-DO
```
Please note that, unlike the name for the file itself, **THE CLASS NAME MATTERS**. Every class name will generate a command named after it, but in lowercase. So, our `Random` class will generate a `random` command.

### 3. Implement `__init__`
The BaseCommand class requires a description and a list of parameters that your command will accept as input. You can pass them just like this:
```python
from commands.base_command import BaseCommand

class Random(BaseCommand):
    def __init__(self):
        description = "Generates a random number between two given numbers"
        params = ["lower", "upper"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        ...  # TO-DO
```
In fact, you can use the exact same code for all your commands, just changing the value for `description` and `params`.

The command description will be displayed if someone uses `!commands`. The list of required parameters will be displayed too as well, but it also helps for ensuring that your command will always get at least as many parameters as it requires.

For instance, if you define `params` the same way we just did, your command will **never** run if someone calls `!random` with less than two parameters, and you don't even have to worry about that.

If your command doesn't require any parameters, you can set `params` to anything *falsy* (an empty list or `None` will do).

### 4. Implement `handle()`
The `handle` method will contain the actual logic for your command. It must accept the following parameters:
- **params**: A list containing the parameters provided by the user. For example, if someone sends `!random 1 10`, *params* will be `["1", "10"]`. This list is guaranteed to contain **at least** as many parameters as specified in `__init__`.
- **message**: The [discord.py Message object](https://discordpy.readthedocs.io/en/latest/api.html#message) for the message that caused the command to execute.
- **client**: The [discord.py Client object](https://discordpy.readthedocs.io/en/latest/api.html#client) for your bot, required to reply to a message, among other things.

Let's see a **very naïve** implementation for the `!random` command, without performing any proper checks:
```python
from commands.base_command import BaseCommand
from random import randint

class Random(BaseCommand):
    def __init__(self):
        description = "Generates a random number between two given numbers"
        params = ["lower", "upper"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        lower_bound = int(params[0])
        upper_bound = int(params[1])
        rolled = randint(lower_bound, upper_bound)

        msg = f"{message.author.mention}, you rolled a {rolled}!"
        await client.send_message(message.channel, msg)
```

Of course, it might fail if the user provides something other than a number, or if lower_bound > upper_bound, but this is enough for the command to work.

That's it, you don't have to do anything else. Dropping a python file with that content in the `commands` folder will cause the new command to be recognized by the bot (a restart is needed, though).

Have a look at [commands/example_command.py](https://github.com/agubelu/discord-bot-template/blob/master/commands/example_command.py) for a more fool-proof implementation for `!random`.

### Isn't this a bit overkill?
Depends. If you have to implement a single, simple command, practicality beats purity. 

But if you want your bot to have many commands with minimal effort, keeping everything organized and tidy, plus a self-updating help command, it is definitely worth it. Don't do spaghetti code.

# Adding events
This template also allows you to define temporal events for your bot that will run every X minutes. You can configure a different interval for each event.

Adding a new event is very similar to adding a command:

### 1. Add a new file to the `events` directory
Again, you can name the new file as you desire. For instance:`the_time.py`.

### 2. Define a new event class in that file
In this case, your event class should inherit from BaseEvent:
```python
from events.base_event import BaseEvent

class TheTime(BaseEvent):
    def __init__(self):
        ...  # TO-DO

    async def run(self, client):
        ...  # TO-DO
```
The class name doesn't matter at all for events.

### 3. Implement `__init__`
For events, the only parameter you need to pass to BaseEvent is the interval in minutes:
```python
from events.base_event import BaseEvent

class TheTime(BaseEvent):
    def __init__(self):
        interval_minutes = 60  # Set the interval for this event
        super().__init__(interval_minutes)

    async def run(self, client):
        ...  # TO-DO
```

### 4. Implement `run()`
The `run` method will be executed every time the event is fired. Since it isn't caused by a user, only the `client` parameter is provided:
- **client**: The [discord.py Client object](https://discordpy.readthedocs.io/en/latest/api.html#client) for your bot, required to send a message, among other things.
```python
from events.base_event import BaseEvent
from utils import get_channel
from datetime import datetime

class TheTime(BaseEvent):
    def __init__(self):
        interval_minutes = 60  # Set the interval for this event
        super().__init__(interval_minutes)

    async def run(self, client):
        now = datetime.now()

        if now.hour == 12:
            msg = "It's high noon!"
        else:
            msg = f"It is {now.hour}:{now.minute}"

        channel = get_channel(client, "general")
        await client.send_message(channel, msg)
```
Wondering what `get_channel()` does? Keep reading!

# Aditional utilities
The `utils` package contains a few methods that you might find useful:

## `get_rel_path`
Returns the absolute path for a path relative to the folder the bot is located in.

Parameters:
- **rel_path**: The relative path.

Example:
- If your bot is located in `/home/agu/mybot`, calling `get_rel_path("storage")` will return `/home/agu/mybot/storage`.

## `get_emoji`
Sadly, discord.py doesn't allow you to send emojis by writing their aliases in the message. Instead, you have to send the actual emoji character in the message, which isn't very convenient.

If you need to *emojize* multiple emojis in one string at once, check the [emoji package](https://pypi.org/project/emoji/) out.

This method allows you to obtain an emoji character for an alias.
Parameters:
- **emoji_name**: Name for the emoji you want to send, as defined in discord, with or without colons.
- **fail_silently**: If true, it will return `emoji_name` if such an emoji does not exist. If false, it will raise `ValueError` if the emoji cannot be found. Defaults to false.

Example:
- `get_emoji(":ok_hand:")` will return `👌`.
- `get_emoji("ok_hand")` will return `👌` as well.
- `get_emoji(":afafaff:")` will raise `ValueError`.
- `get_emoji(":afafaff:", fail_silently=True)` will return `":afafaff:"`.

## `get_channel`
You can use this method to quickly search for a channel by one of its attributes. For example, if your bot will reside in only one server, looking for a channel by name is more clear than doing so by its ID (though you'll have to update your code if the channel name changes).

Will raise `ValueError` if no such channel can be found.

Parameters:
- **client**: The discord.py client for your bot.
- **value**: The desired value for the attribute you're searching for. For instance, the channel name or ID.
- **attribute**: The name of the search attribute, for instance, `"name"` or `"id"`. You can use any attribute a [discord.py Channel object](https://discordpy.readthedocs.io/en/latest/api.html#channel) has. Defaults to `"name"`.

Examples:
- `get_channel(client, "general")` will return the first found channel with name `general`.
- `get_channel(client, "123456", "id")` will return the channel with ID 123456, if it exists.
- `get_channel(client, "non-existing-channel")` will raise `ValueError` if no channel that your bot has access to has that name.

## `send_in_channel`
This method is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

It allows you to quickly send a message in a channel with a certain name. It's particularly useful if your bot is located in a single server and you can access channels directly by name.

You can pass it any positional arguments that you would normally pass to `client.send_message()`.

Since it uses `get_channel` it will also raise `ValueError` if no such channel can be found.

Parameters:
- **client**: The discord.py client for your bot.
- **channel_name**: The name of the channel you want to send a message in.
- **\*args**: Other positional arguments to pass to `client.send_message()`

Examples:
- `await send_in_channel(client, "general", "Hey")` will send `Hey` to channel `#general`.

## `try_upload_file`
This method is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Likewise, it is also likely that you will need to upload a picture or a file to some channel. This method allows you to do it with a single line of code, sending an error message if it fails to do it for any reason.

Parameters:
- **client**: The discord.py client for your bot.
- **channel**: The discord.py channel object to send the file to.
- **file_path**: The absolute path for the file you want to send.
- **content**: The aditional message string to send alongside the file. Defaults to `None`.
- **delete_after_send**: Whether or not to delete the file specified in `file_path` after sending it. It will be deleted even if the file cannot be successfully sent. Defaults to `False`.
- **retries**: Number of times to retry sending the file if an error is encountered before giving up and sending an error message. Defaults to `3`.

Examples:
- `await try_upload_file(client, channel, "/home/agu/file.jpg", "My picture")` will send `file.jpg` to channel `channel` with the additional text `My picture`, and without deleting it afterwards,.

- `await try_upload_file(client, channel, "/home/agu/file.jpg", delete_after_send=True)` will send `file.jpg` to channel `channel` without any caption and deleting the file afterwards.

# License
GPL-3.0