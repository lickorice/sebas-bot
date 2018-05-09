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
dt = DateSerializer()
cmdNum = 0  # total number of commands in instance

version = '0.1 alpha'

strikes = {'id': 0}
userIDs = {'owner': '319285994253975553'}
imgs = {'avatar': 'https://avatars0.githubusercontent.com/u/14945942?s=400&u=\
563ecf361e3cc4d40074868152d10951ca5e85b2&v=4'}

log = Logger()
emoji = EmojiHandler()


# mention function
def mtn(id_string):
    return '<@{}>'.format(id_string)


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
    print(bot.user.name, 'has been started at {}:{}'.format(dt.getHour(),
          dt.getMin()))


@bot.command(pass_context=True)
async def info(ctx):
    # Prints developer info
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
    log.action('Adding numbers...')
    await bot.send_message(ctx.message.channel, str(int(a)+int(b)))


@bot.command(pass_context=True)
async def multiply(ctx, a, b):
    log.action('Multiplying numbers...')
    await bot.send_message(ctx.message.channel, str(int(a)*int(b)))


@bot.command(pass_context=True)
async def divide(ctx, a, b):
    log.action('Dividing numbers...')
    await bot.send_message(ctx.message.channel, str(int(a)/int(b)))


@bot.command(pass_context=True)
async def subtract(ctx, a, b):
    log.action('Subtracting numbers...')
    await bot.send_message(ctx.message.channel, str(int(a)-int(b)))


def isRepeating(string):
    for n in range(len(string) - 1):
        if n != 0:
            if string[n] == string[n-1]:
                return True


@bot.command(pass_context=True)
async def react(ctx, para=None, charstr=None, msgID=None):
    if para == 'str':
        msgchannel = ctx.message.channel
        target_msg = await bot.get_message(channel=msgchannel, id=msgID)
        await bot.delete_message(ctx.message)
        for char in charstr.lower():
            await bot.add_reaction(message=target_msg, emoji=emoji.chrs[char])


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

    await bot.process_commands(message)


# change token to your bot's token.
bot.run('NDQyNzIyMzg4NzU3NDQ2Njcx.DdDFWQ.rLHEmKpSwJSzm-QqA45H1ZqHL6I')
