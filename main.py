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
bot.remove_command('help')
botID = '442722388757446671'
dt = DateSerializer()
cmdNum = 0  # total number of commands in instance

version = '1.0 stable release'

strikes = {'id': 0}
userIDs = {'owner': '319285994253975553', 'self': '442722388757446671'}
imgs = {'avatar': 'https://avatars0.githubusercontent.com/u/14945942?s=400&u=\
563ecf361e3cc4d40074868152d10951ca5e85b2&v=4',
        'sebas_profile': 'https://cdn.discordapp.com/attachments/44414784649363\
4560/444744084830289921/Sebas_Profile.png'}

log = Logger()
emoji = EmojiHandler()
dbh = dbhelper.DBHelper()

# dictionary provides text files to look for
txt_f = {'splash': 'txt/splash.txt',
         'help': 'txt/help.txt',
         'verify': 'txt/verify.txt',
         'rhelp': 'txt/rhelp.txt',
         'vrfres': 'txt/verify_response.txt',
         'vrfres_m': 'txt/verify_response_manual.txt',
         'v_chan_err': 'txt/verify_channel_set_error.txt',
         'v_chan_success': 'txt/verify_channel_set_success.txt'}

# default help string
helpstr = " Type `..help` for more information."

# declares a dictionary of the last, and second to the last messages
last_msg = {'channel': 'id'}
next_msg = {'channel': 'id'}
mbr_role = {}

admins_all = ()
mods_all = ()


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

        # changes presence
        await bot.change_presence(game=discord.Game(name='..help for help'))

        # checks if member has admin perms
        for mbr in svr.members:
            mbr_has_perms = False
            for adminRoleName in ['admin', 'administrator', 'Admin',
                                  'Administrator', 'owner', 'Owner']:
                if get(mbr.roles, name=adminRoleName):
                    mbr_has_perms = True
                    try:
                        dbh.insertAdmin(mbr.id, svr.id)
                        log.log(mbr.name+' registered as admin.',
                                dt.getComplete())
                    except sqlite3.IntegrityError:
                        log.log(mbr.name+' is already registered as admin.',
                                dt.getComplete())
                    break
            if mbr_has_perms is False:
                dbh.dropAdmin(mbr.id, svr.id)

        # checks if member has mod perms
        for mbr in svr.members:
            mbr_has_perms = False
            for modRoleName in ['mod', 'moderator', 'Mod',
                                'Moderator', 'helper', 'help']:
                if get(mbr.roles, name=modRoleName):
                    mbr_has_perms = True
                    try:
                        dbh.insertMod(mbr.id, svr.id)
                        log.log(mbr.name+' registered as mod.',
                                dt.getComplete())
                    except sqlite3.IntegrityError:
                        log.log(mbr.name+' is already registered as mod.',
                                dt.getComplete())
                    break
            if mbr_has_perms is False:
                dbh.dropMod(mbr.id, svr.id)

        global admins_all
        admins_all = dbh.fetchallAdmins()
        global mods_all
        mods_all = dbh.fetchallMods()


# kill command
@bot.command(pass_context=True)
async def leave(ctx):
    if isAdmin():
        await bot.send_message(ctx.message.channel, 'I shall take my leave. \
Thank you.')
    await bot.close()


# shows help
@bot.command(pass_context=True)
async def help(ctx):
    cmdCount()
    await bot.send_message(ctx.message.author, master_help)


@bot.command(pass_context=True)
async def info(ctx):
    # Prints developer info
    log.action('Info method called.', dt.getComplete())
    cmdCount()
    e = discord.Embed(color=0xf8f8f8)
    e.add_field(name='Developer', value=mtn(userIDs['owner']), inline=False)
    e.add_field(name='Version', value=version, inline=False)
    gitLink = 'https://github.com/lickorice/sebas-bot'
    e.add_field(name='GitHub Link', value=gitLink, inline=False)
    e.add_field(name='Number of commands since startup:', value=str(cmdNum),
                inline=True)
    e.set_footer(text="developed by lickorice, May 2018",
                 icon_url=imgs['avatar'])
    e.set_image(url=imgs['sebas_profile'])
    await bot.send_message(ctx.message.channel, embed=e)


@bot.command(pass_context=True)
async def add(ctx, a, b):
    cmdCount()
    log.action('Adding numbers...', dt.getComplete())
    await bot.send_message(ctx.message.channel, str(int(a)+int(b)))


@bot.command(pass_context=True)
async def multiply(ctx, a, b):
    cmdCount()
    log.action('Multiplying numbers...', dt.getComplete())
    await bot.send_message(ctx.message.channel, str(int(a)*int(b)))


@bot.command(pass_context=True)
async def divide(ctx, a, b):
    cmdCount()
    log.action('Dividing numbers...', dt.getComplete())
    await bot.send_message(ctx.message.channel, str(int(a)/int(b)))


@bot.command(pass_context=True)
async def subtract(ctx, a, b):
    cmdCount()
    log.action('Subtracting numbers...', dt.getComplete())
    await bot.send_message(ctx.message.channel, str(int(a)-int(b)))


# block react command
@bot.command(pass_context=True)
async def react(ctx, para=None, charstr=None, msgID=None):
    cmdCount()
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
    cmdCount()
    await bot.send_message(ctx.message.channel, rhelpSTR.format(bot.user.name,
                                                                bot.user.name
                                                                ))


# manual verification command, special perms
@bot.command(pass_context=True)
async def verifyme(ctx):
    cmdCount()
    chn = ctx.message.channel
    svr = chn.server
    mbr = ctx.message.author

    if (svr.id, chn.id,) in dbh.fetchallVChannels():
        if get(mbr.roles, name='Member'):
            await bot.send_message(chn, "<@{}>, you're \
already **verified**.".format(mbr.id))
        else:
            await verify_response(mbr.id, ctx.message, type='manual')


# BEYOND THIS POINT:
# Moderator commands
def isMod(ctx):
    if ctx.message.author.id == userIDs['owner'] or\
       (ctx.message.author.id, ctx.message.channel.server.id,) in admins_all\
       or (ctx.message.author.id, ctx.message.channel.server.id,) in mods_all:
        return True
    else:
        return False


@bot.command(pass_context=True)
async def verifyuser(ctx):
    cmdCount()

    async def verify_through_DM(userID):
        # checks if raw user ID is not invalid
        if get(ctx.message.channel.server.members, id=userID):
            mbr = get(ctx.message.channel.server.members, id=userID)
            # checks if user is a member
            if get(mbr.roles, name="Member"):
                await bot.send_message(ctx.message.channel,
                                       '<@{}> is already \
**verified.**'.format(userID))
                return
            # verifies if not member
            else:
                await verifyMember(mbr)
                await bot.send_message(ctx.message.channel, 'Sending a **verif\
ication message** to {} .'.format(mbr.name))
        # alerts that the user does not exist.
        else:
            await bot.send_message(ctx.message.channel,
                                   'Invalid user **ID.**')

    if isMod(ctx):
        if ctx.message.mentions[0]:
            await verify_through_DM(ctx.message.mentions[0].id)
        else:
            await bot.send_message(ctx.message.channel,
                                   "Please mention user." + helpstr)
    else:
        await bot.send_message(ctx.message.channel,
                               "You aren't **authorized** to do that.")


# BEYOND THIS POINT:
# Admin commands
def isAdmin(ctx):
    if ctx.message.author.id == userIDs['owner'] or\
       (ctx.message.author.id, ctx.message.channel.server.id,) in admins_all:
        return True
    else:
        return False


# DM all feature
@bot.command(pass_context=True)
async def dmall(ctx, string):
    cmdCount()
    if isAdmin(ctx):
        await bot.send_message(ctx.message.channel, 'Sending message to all.')
        for mbr in ctx.message.channel.server.members:
            if mbr.id == userIDs['self']:
                continue
            try:
                log.log('Sending message to '+mbr.name, dt.getComplete())
                await bot.send_message(mbr, string+"\n\n*This message is sent \
by*  <@{}>".format(ctx.message.author.id))
            except discord.errors.Forbidden:
                pass
    else:
        await bot.send_message(ctx.message.channel,
                               "You aren't **authorized** to do that.")


# command to refresh the roles in case of role change
@bot.command(pass_context=True)
async def consolidateroles(ctx):
    cmdCount()
    if isAdmin(ctx):
        svr = ctx.message.channel.server
        for mbr in svr.members:
            mbr_has_perms = False
            for modRoleName in ['mod', 'moderator', 'Mod',
                                'Moderator', 'helper', 'help']:
                if get(mbr.roles, name=modRoleName):
                    mbr_has_perms = True
                    try:
                        dbh.insertMod(mbr.id, svr.id)
                        log.log(mbr.name+' registered as mod.',
                                dt.getComplete())
                    except sqlite3.IntegrityError:
                        log.log(mbr.name+' is already registered as mod.',
                                dt.getComplete())
                    break
            if mbr_has_perms is False:
                dbh.dropMod(mbr.id, svr.id)

        global admins_all
        admins_all = dbh.fetchallAdmins()
        global mods_all
        mods_all = dbh.fetchallMods()

        await bot.send_message(ctx.message.channel,
                               'Roles successfully **consolidated**.')
    else:
        await bot.send_message(ctx.message.channel,
                               "You aren't **authorized** to do that.")


# sets the manual verification channel
@bot.command(pass_context=True)
async def setvrfchannel(ctx):
    cmdCount()
    svr = ctx.message.channel.server
    chn = ctx.message.channel
    if isAdmin(ctx):
        try:
            if chn == bot.get_channel(dbh.fetchVerifyChannel(svr.id)):
                await bot.send_message(chn, '`#{}` is already a \
**verification** channel.'.format(chn.name))
                return
        except TypeError:
            pass

        try:
            dbh.insertVerifChannel(svr.id, chn.id)
            await bot.send_message(chn, v_chan_set.format(chn.name))
        except sqlite3.IntegrityError:
            cur_chn = bot.get_channel(dbh.fetchVerifyChannel(svr.id))
            await bot.send_message(chn, v_chan_error.format(cur_chn.name))
    else:
        await bot.send_message(ctx.message.channel,
                               "You aren't **authorized** to do that.")


# removes the manual verification channel
@bot.command(pass_context=True)
async def rmvrfchannel(ctx):
    cmdCount()
    svr = ctx.message.channel.server
    chn = ctx.message.channel
    cur_chn = bot.get_channel(dbh.fetchVerifyChannel(svr.id))
    if isAdmin(ctx) and cur_chn == chn:
        await bot.send_message(chn, "`#{}` is no longer a \
**verification** channel.".format(chn.name))
        dbh.dropVerifyChannel(svr.id, chn.id)
    else:
        await bot.send_message(ctx.message.channel,
                               "You aren't **authorized** to do that.")


# manual verification of ALL members. use with discretion.
@bot.command(pass_context=True)
async def verifyall(ctx):
    cmdCount()
    if isAdmin(ctx):
        for mmbr in ctx.message.server.members:
            if ctx.message.author.id == userIDs['self']:
                continue

            async def if_member_role(member_pending):
                # this is to continue a nested for loop
                for rle in member_pending.roles:
                    if rle == get(ctx.message.server.roles, name="Member"):
                        log.log('This is a member!', dt.getComplete())
                        return
                try:
                    await verifyMember(member_pending)
                except discord.errors.Forbidden:
                    return  # this means the bot can't send the message.

            await if_member_role(member_pending=mmbr)

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
                try:
                    dbh.insertDMList(member.id, ch.id)
                except sqlite3.IntegrityError:
                    pass
                log.log(member.name+' successfully registered a PM Channel.',
                        dt.getComplete())
            except sqlite3.IntegrityError:
                log.log('Member already pending. ', dt.getComplete())
            break


# this is the verification response function
async def verify_response(authorID, message, type='onMessage'):
    role = mbr_role[dbh.fetchPendingServerID(authorID)]
    svr = bot.get_server(dbh.fetchPendingServerID(authorID))
    mbr = get(svr.members, id=authorID)

    # bot responds to verification depending on verif type
    if type == 'onMessage':
        await bot.send_message(message.channel,
                               vrf_response.format(role.name))
        log.log('User: ' + message.author.name + ' has been verified.',
                dt.getComplete())
    elif type == 'manual':
        await bot.send_message(message.channel,
                               vrf_response_manual.format(message.author.id,
                                                          message.server.name))
        log.log('User: ' + message.author.name + ' has been verified.',
                dt.getComplete())
    else:
        log.log('Invalid verification type.', dt.getComplete())
        return

    # bot assigns member role
    await bot.add_roles(mbr, role)
    log.log(role.name + ' has been assigned to ' + message.author.name,
            dt.getComplete())

    # bot drops pending case
    log.log(message.author.name+"'s pending case has been dropped.",
            dt.getComplete())
    dbh.dropPending(authorID)


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
            await verify_response(authorID, message)
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
master_help = fIO(txt_f['help'])
vrfSTR = fIO(txt_f['verify'])
rhelpSTR = fIO(txt_f['rhelp'])
vrf_response = fIO(txt_f['vrfres'])
vrf_response_manual = fIO(txt_f['vrfres_m'])
v_chan_error = fIO(txt_f['v_chan_err'])
v_chan_set = fIO(txt_f['v_chan_success'])

# initializes database upon start
dbh.init()
# change token to your bot's token.
bot.run(input("Enter token : "))
