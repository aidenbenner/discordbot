import discord
import asyncio
import configparser
import sys
import random as r

config = configparser.ConfigParser()
config.read('config')
if not 'client_secret' in config['DEFAULT']:
    print("please add your client secret to the config file")
    sys.exit()
CLIENT_SECRET = config['DEFAULT']['client_secret']

client = discord.Client()

class Command():
    def __init__(self, trigger=None):
        self.trigger = trigger

    def call(self, message):
        return "?"

class Eightball(Command):
    messages = ["It is certain",
                    "It is decidedly so",
                    "Without a doubt",
                    "Yes definitely",
                    "You may rely on it",
                    "As I see it, yes",
                    "Most likely",
                    "Outlook good",
                    "Yes",
                    "Signs point to yes",
                    "Reply hazy try again",
                    "Ask again later",
                    "Better not tell you now",
                    "Cannot predict now",
                    "Concentrate and ask again",
                    "Don't count on it",
                    "My reply is no",
                    "My sources say no",
                    "Outlook not so good",
                    "Very doubtful"]
    def call(self, message):
        return Eightball.messages[r.randrange(0, len(Eightball.messages))]


class Dice(Command):
    def call(self, message):
        args = message.content.split()
        a = 1
        b = 6
        print(args)
        try:
            if len(args) == 2:
                b = int(args[1])
            elif len(args) >= 3:
                a = int(args[1])
                b = int(args[2])
        except Exception as e:
            print(str(e))
        mi = min(a,b)
        ma = max(a,b)
        return r.randint(mi,ma)

class Impersonate(Command):
    def call(self, message):
        args = message.content.split()
        name = args[1]

        member = message.server.get_member_named(name)
        msgs = []
        for m in client.logs_from(message.channel):
            print(m.clean_content)
            msgs.append(m.clean_content)
        return msgs[r.randrange(0,len(msgs))]


class TicTac():
    def __init__(self):
        pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

commands = []
commands.append(Eightball("8ball"))
commands.append(Dice("dice"))
commands.append(Impersonate("impersonate"))

delim = '!'

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if not message.content.startswith(delim):
        return

    c = Command()
    for x in commands:
        if message.content.startswith(delim + x.trigger):
            c = x
            break

    tmp = await client.send_message(message.channel, "loading...")
    val = c.call(message)
    await client.edit_message(tmp, val)
    return

client.run(CLIENT_SECRET)
