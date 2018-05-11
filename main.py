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

version = '0.2 alpha'

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

# declares a dictionary of the last, and second to the last messages
last_msg = {'channel': 'id'}
next_msg = {'channel': 'id'}
privChan = {'user_id': 'channel_id'}


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
    if msgID is None:
        msgID = next_msg[ctx.message.channel.id]

    log.action('Handling `..react`...', dt.getComplete())
    if para == 'str':
        if charstr:
            msgchannel = ctx.message.channel
            target_msg = await bot.get_message(channel=msgchannel, id=msgID)
            await bot.delete_message(ctx.message)
            last_msg[ctx.message.channel.id] = next_msg[ctx.message.channel.id]
            for char in charstr.lower():
                log.action('Reacting to ' + msgID, dt.getComplete())
                await bot.add_reaction(message=target_msg,
                                       emoji=emoji.chrs[char])
        else:
            await bot.send_message(ctx.message.channel,
                                   'Please specify a **message!** Do ..rhelp\
for more information.')
    elif para == 'set':
        if charstr:
            msgchannel = ctx.message.channel
            target_msg = await bot.get_message(channel=msgchannel, id=msgID)
            await bot.delete_message(ctx.message)
            if charstr in emoji.sets:
                for reaction in emoji.sets[charstr]:
                    await bot.add_reaction(message=target_msg, emoji=reaction)
            else:
                await bot.send_message(ctx.message.channel,
                                       'That set does not exist! Do ..rhelp\
for more information.')
        else:
            await bot.send_message(ctx.message.channel,
                                   'Please specify a **set!**')
    else:
        await bot.send_message(ctx.message.channel,
                               "Please specify a **parameter!** (str, set)")


# sethelp, shows available sets
@bot.command(pass_context=True)
async def rhelp(ctx):
    await bot.send_message(ctx.message.channel,
                           '**How** `..react` **works:** \n \
`..react (str/set) (message/set)`\n `str` makes ' + bot.user.name + ' react \
with the following `message`. **Repeated letters do not count.** \n \
`set` makes ' + bot.user.name + ' react with a following premade set.\
Sets include:\n`hearts` - emojis of hearts')


# handles on member join stuff
@bot.event
async def on_member_join(member):
    log.log("New user joined! User ID: "+member.id, dt.getComplete())
    askforVerif_str = (mtn(member.id)+"\n**Hello!** I am **"+bot.user.name+"**\
, **" + member.server.name+"'s** homemade security and moderat\
ion bot, developed by none other than "+mtn(userIDs['owner'])+" himself! \n\n\
I am required to ask if you have **read the server #rules** in " +
                       "**"+member.server.name+"**.\n\n"
                       + "Please reply with `yes` if you have, and you will \
be *given permissions*  to access the server's public channels. Thank you.")
    await bot.send_message(member, askforVerif_str)

    for ch in bot.private_channels:
        log.log('Retrieving channel...', dt.getComplete())
        log.log('Channel recipients: '+str(len(ch.recipients)),
                dt.getComplete())
        if member in ch.recipients and len(ch.recipients) == 1:
            log.log('New member successfully registered PM Channel.',
                    dt.getComplete())
            privChan[member.id] = ch.id
            break


# handles on message stuff
@bot.event
async def on_message(message):

    authorID = message.author.id

    # handles verification in private messages
    # passed by on_member_join()
    if message.content == 'yes' and message.channel.id == privChan[authorID]:
        await bot.send_message(bot.get_channel(privChan[authorID]),
                               'received')

    # this registers last and second to the last messages, on each channel.
    global last_msg
    global next_msg
    if message.channel.id in last_msg:
        if message.id != last_msg[message.channel.id]:
            next_msg[message.channel.id] = last_msg[message.channel.id]
    last_msg[message.channel.id] = message.id

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
        if greet == message.content.lower() and authorID != botID:
            greeting = 'Good morning, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in day_greetings:
        if greet == message.content.lower() and authorID != botID:
            greeting = 'Good day, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in evening_greetings:
        if greet == message.content.lower() and authorID != botID:
            greeting = 'Good evening, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in afternoon_greetings:
        if greet == message.content.lower() and authorID != botID:
            greeting = 'Good afternoon, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in night_greetings:
        if greet == message.content.lower() and authorID != botID:
            greeting = 'Good night, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in hello_greetings:
        if greet == message.content.lower() and authorID != botID:
            greeting = 'Greetings, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    for greet in bye_greetings:
        if greet == message.content.lower() and authorID != botID:
            greeting = 'Godspeed, young master ' + mtn(authorID)
            await bot.send_message(message.channel, greeting)
            break

    await bot.process_commands(message)


# change token to your bot's token.
bot.run('NDQ0MTUzMzM2MjY3MTQ1MjE2.DdbQhg.7fQWe59TSBgicbzOp26d2b1mGvU')
