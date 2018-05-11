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
import sqlite3
import dbhelper
from discord.ext import commands
from discord.utils import get
import asyncio
from dateserializer import DateSerializer
from logger import Logger
from emoji import EmojiHandler


bot = commands.Bot(command_prefix='..')
botID = '442722388757446671'
dt = DateSerializer()
cmdNum = 0  # total number of commands in instance

version = '0.4 beta'

strikes = {'id': 0}
userIDs = {'owner': '319285994253975553', 'self': '444153336267145216'}
imgs = {'avatar': 'https://avatars0.githubusercontent.com/u/14945942?s=400&u=\
563ecf361e3cc4d40074868152d10951ca5e85b2&v=4'}

log = Logger()
emoji = EmojiHandler()
dbh = dbhelper.DBHelper()

# dictionary provides text files to look for
txt_f = {'splash': 'txt/splash.txt',
         'help': 'txt/help.txt',
         'verify': 'txt/verify.txt',
         'rhelp': 'txt/rhelp.txt',
         'vrfres': 'txt/verify_response.txt'}

# declares a dictionary of the last, and second to the last messages
last_msg = {'channel': 'id'}
next_msg = {'channel': 'id'}
privChan = {'user_id': 'channel_id'}

pending_r = {'user_id': 'server_id'}
mbr_role = {}


# function to read .txt files
def fIO(file):
    with open(file, 'r') as file:
        file_contents = file.read()
        return file_contents


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
    print(fIO(txt_f['splash']))
    print('\rInitialzing {}...'.format(bot.user.name))
    print('{} is up and running.'.format(bot.user.name))
    print('This bot is created by Carlos Panganiban (lickorice)')
    print('developed using discord.py under the MIT License')
    print('█████████████████████████████████████████████████████')
    print('Today is {} {}, {}'.format(dt.getMonth(),
          dt.getDay(), dt.getYear()))
    print(bot.user.name, 'has been started at ' + dt.getComplete())

    for svr in bot.servers:
        log.log("Initialzing " + svr.name + "...", dt.getComplete())
        global mbr_role  # declares 'default member role list'
        role = get(svr.roles, name="Member")
        if role:
            mbr_role[svr.id] = role
            log.log("Fetching member role from " + svr.name + "...",
                    dt.getComplete())
        else:
            log.log("No member roles found for " + svr.name, dt.getComplete())
        log.log(svr.name + " has been initialized.", dt.getComplete())


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
                                       'That set does not exist! Do `..rhelp`\
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
    await bot.send_message(ctx.message.channel, rhelpSTR.format(bot.user.name,
                                                                bot.user.name
                                                                ))


# BEYOND THIS POINT:
# Admin commands
# sethelp, shows available sets
@bot.command(pass_context=True)
async def verifyall(ctx):
    if ctx.message.author.id == userIDs['owner']:
        for mbr in ctx.message.server.members:
            if ctx.message.author.id == userIDs['self']:
                continue
            try:
                await verifyMember(mbr)
            except discord.errors.Forbidden:
                continue

    else:
        bot.send_message(ctx.message.channel,
                         "You aren't **authorized** to use that command.")


# handles on member join stuff
@bot.event
async def on_member_join(member):
    log.log("New user joined! User ID: "+member.id, dt.getComplete())
    await verifyMember(member)


# handles verification
async def verifyMember(member):

    if member.id == userIDs['self']:
        return

    log.log('Verifying user: ' + member.name, dt.getComplete())
    askforVerif_str = vrfSTR.format(mtn(member.id),
                                    bot.user.name,
                                    member.server.name,
                                    mtn(userIDs['owner']),
                                    member.server.name)

    await bot.send_message(member, askforVerif_str)
    for ch in bot.private_channels:
        if member in ch.recipients and len(ch.recipients) == 1:
            try:
                log.log('Attempting to append...', dt.getComplete())
                dbh.insertPending(member.id, member.server.id, True)
                dbh.insertDMList(member.id, ch.id)
                log.log(member.name+' successfully registered a PM Channel.',
                        dt.getComplete())
            except sqlite3.IntegrityError:
                log.log('Member already pending. ', dt.getComplete())
            break


# handles on message stuff
@bot.event
async def on_message(message):
    # uncomment this part to turn on logging of messages in the console:
    # log.log('User : '+message.author.name+' Message : '+message.content +
    #         ' Channel : '+message.channel.id, dt.getComplete())

    authorID = message.author.id

    # handles verification in private messages
    # passed by verifyMember
    try:
        if message.content.lower() == 'yes' and \
           message.channel.id == dbh.fetchDMChannelID(authorID):
            role = mbr_role[dbh.fetchPendingServerID(authorID)]
            svr = bot.get_server(dbh.fetchPendingServerID(authorID))
            mbr = get(svr.members, id=authorID)

            # bot responds to verification
            await bot.send_message(message.channel,
                                   vrf_response.format(role.name))
            log.log('User: ' + message.author.name + ' has been verified.',
                    dt.getComplete())

            # bot assigns member role
            await bot.add_roles(mbr, role)
            log.log(role.name + ' has been assigned to ' + message.author.name,
                    dt.getComplete())

            # bot drops pending case
            dbh.dropPending(authorID)
    except TypeError:
        pass

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

    await bot.process_commands(message)


# passes file IOs to strings to avoid unhandled file IO errors
vrfSTR = fIO(txt_f['verify'])
rhelpSTR = fIO(txt_f['rhelp'])
vrf_response = fIO(txt_f['vrfres'])

# initializes database upon start
dbh.init()
# change token to your bot's token.
bot.run('NDQyNzIyMzg4NzU3NDQ2Njcx.Dddf2g.JuVezt19s5GRs6MDROQ0a5Go2a4')
