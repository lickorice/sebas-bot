"""
Copyright (c) 2018, Carlos Panganiban

MIT License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import discord
from discord.ext import commands
import asyncio
from dateserializer import DateSerializer
from logger import Logger
from emoji import EmojiHandler


bot = commands.Bot(command_prefix='..')
botID = '442722388757446671'
dt = DateSerializer()
cmdNum = 0  # total number of commands in instance

version = '0.1 alpha'

strikes = {'id': 0}
userIDs = {'owner': '319285994253975553'}
imgs = {'avatar': 'https://avatars0.githubusercontent.com/u/14945942?s=400&u=\
563ecf361e3cc4d40074868152d10951ca5e85b2&v=4'}

log = Logger()
emoji = EmojiHandler()

morning_greetings = ['good morning', 'ohayou', 'ohaiyou', 'ohayo', 'gm']
afternoon_greetings = ['good afternoon', 'good pm']
evening_greetings = ['good evening', 'evening']
day_greetings = ['good day']
night_greetings = ['good night', 'gn']
bye_greetings = ['i gtg']
hello_greetings = ['hello', 'hi', 'herro']


# mention function
def mtn(id_string):
    return '<@{}>'.format(id_string)


# function to count commands since started
def cmdCount():
    global cmdNum
    cmdNum += 1


@bot.event
@asyncio.coroutine
async def on_ready():
    # Sebas' welcome message :)
    with open('splash.txt', 'r') as file:
        file_contents = file.read()
        print(file_contents)
    print('\rInitialzing {}...'.format(bot.user.name))
    print('{} is up and running.'.format(bot.user.name))
    print('This bot is created by Carlos Panganiban (lickorice)')
    print('developed using discord.py under the MIT License')
    print('█████████████████████████████████████████████████████')
    print('Today is {} {}, {}'.format(dt.getMonth(),
          dt.getDay(), dt.getYear()))
    print(bot.user.name, 'has been started at ' + dt.getComplete())


# kill command
@bot.command(pass_context=True)
async def leave(ctx):
    await bot.send_message(ctx.message.channel, 'I shall take my leave. \
Thank you.')
    await bot.close()


@bot.command(pass_context=True)
async def info(ctx):
    # Prints developer info
    log.action('Info method called.', dt.getComplete())
    cmdCount()
    e = discord.Embed()
    e.add_field(name='Developer', value=mtn(userIDs['owner']), inline=False)
    e.add_field(name='Version', value=version, inline=False)
    e.add_field(name='Number of commands since startup:', value=str(cmdNum),
                inline=True)
    e.set_footer(text="developed by lickorice, May 2018",
                 icon_url=imgs['avatar'])
    await bot.send_message(ctx.message.channel, embed=e)


@bot.command(pass_context=True)
async def add(ctx, a, b):
    log.action('Adding numbers...', dt.getComplete())
    await bot.send_message(ctx.message.channel, str(int(a)+int(b)))


@bot.command(pass_context=True)
async def multiply(ctx, a, b):
    log.action('Multiplying numbers...', dt.getComplete())
    await bot.send_message(ctx.message.channel, str(int(a)*int(b)))


@bot.command(pass_context=True)
async def divide(ctx, a, b):
    log.action('Dividing numbers...', dt.getComplete())
    await bot.send_message(ctx.message.channel, str(int(a)/int(b)))


@bot.command(pass_context=True)
async def subtract(ctx, a, b):
    log.action('Subtracting numbers...', dt.getComplete())
    await bot.send_message(ctx.message.channel, str(int(a)-int(b)))


# block react command
@bot.command(pass_context=True)
async def react(ctx, para=None, charstr=None, msgID=None):
    if para == 'str':
        msgchannel = ctx.message.channel
        target_msg = await bot.get_message(channel=msgchannel, id=msgID)
        await bot.delete_message(ctx.message)
        for char in charstr.lower():
            await bot.add_reaction(message=target_msg, emoji=emoji.chrs[char])


# handles on message stuff
@bot.event
async def on_message(message):
    authorID = message.author.id

    # handles advertising discord links
    if 'discord.gg' in message.content:
        if authorID in strikes:
            strikes[authorID] += 1
        else:
            strikes[authorID] = 1

        if strikes[authorID] == 2:
            await bot.ban(message.author)
        else:
            await bot.send_message(message.channel,
                                   '**WARNING!**\n' + u"\u26A0" + u"\u26A0" +
                                   u"\u26A0" + mtn(authorID) + ", Advertising in\
 public channels is **a bannable offense!** \n ***This will be\
 your last warning!***")

    # handles greetings
    for greet in morning_greetings:
        if greet in message.content.lower() and authorID != botID:
            greeting = 'Good morning, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in day_greetings:
        if greet in message.content.lower() and authorID != botID:
            greeting = 'Good day, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in evening_greetings:
        if greet in message.content.lower() and authorID != botID:
            greeting = 'Good evening, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in afternoon_greetings:
        if greet in message.content.lower() and authorID != botID:
            greeting = 'Good afternoon, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in night_greetings:
        if greet in message.content.lower() and authorID != botID:
            greeting = 'Good night, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in hello_greetings:
        if greet in message.content.lower() and authorID != botID:
            greeting = 'Greetings, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in bye_greetings:
        if greet in message.content.lower() and authorID != botID:
            greeting = 'Godspeed, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    await bot.process_commands(message)


# change token to your bot's token.
bot.run('NDQyNzIyMzg4NzU3NDQ2Njcx.DdDFWQ.rLHEmKpSwJSzm-QqA45H1ZqHL6I')
