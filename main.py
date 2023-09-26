"""Lethera - 2020
A discord bot that honks, maintains a blacklist, sends goose gifs, and has an item-finding game.
"""
from keep_alive import keep_alive
import discord
from discord.ext import commands
from discord import Member
from manageFunctions import *
import asyncio
import time
import random
import os

lethId = 344218113497366528

commonItems = [
    'an old radio', 'a tree branch', 'a pencil', 'a leather book',
    'a seashell', 'a rose', 'a basketball', 'a fossil', 'a stone', 'soap',
    'a spoon', 'a toothbrush', 'a fork', 'a tableknife', 'a ribbon',
    'a chess piece', 'a video game cartridge', 'a flash drive', 'an empty mug',
    'a dusty feather', 'a clothes hanger', 'a hairbrush', 'a comb',
    'a bandage', 'a mask', 'a pair of scissors', 'a ruler', 'a whistle'
]
rareItems = ['three quarters of a horse', 'a gold coin']
legendaryItems = [
    'one quarter of a horse', 'the holy grail', 'the holy hand grenade'
]
duck_responses = [
    'GET THOSE DUCKS OUT OF HERE', 'There is no duck here, only ***ANGER***',
    'no.', 'i am going to eat your knees',
    'i have decided that it is time for you to die',
    'je ne suis pas un canard', 'I am a goose, please address me as such',
    'do i really look like a duck? :(', 'death time!',
    'i will pour cement into your ears.', 'I am not a duck, you ***egg***',
    '0w0 You egg! stabs uu ÙωÙ', 'Bite me!',
    'Kind fellow, it seems you may have mistaken me for a lowly duck. I must inform you that I am in fact a noble goose, please do not make this mistake again!'
]
egg_responses = [
    "*sad goose noises*\nLook what you've done, Honkers is having a crisis!",
    "ERROR: Honkers isn't that smart"
]
goose_attack_gifs = [
    'gooseAttack', 'gooseAttack1', 'gooseAttack2', 'gooseAttack3',
    'gooseAttack4'
]
goose_general_gifs = [
    'gooseGen', 'gooseGen1', 'gooseGen2', 'gooseGen3', 'gooseGen4',
    'gooseGen5', 'gooseGen6', 'gooseGen6', 'gooseGen7', 'gooseGen8',
    'gooseGen9', 'gooseGen11', 'gooseGen12', 'gooseGen13', 'gooseGen14',
    'gooseGen15', 'gooseGen16', 'gooseGen17'
]

bot = commands.Bot(command_prefix="b!", case_insensitive=True)
bot.remove_command('help')


#Error handler
@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Oops, looks like you forgot something in that command")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("You've given an invalid argument for this command")
    elif isinstance(error, TypeError):
        pass
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(
            "Hmm, looks like something's not right here. Please report the error using b!report and include which command you used to produce the error"
        )
    elif isinstance(error, commands.MissingPermissions):
        pass
    elif (error, commands.CommandOnCooldown):
        timeAmt = error.retry_after
        minutes = timeAmt % 3600 / 60
        seconds = timeAmt % 3600 % 60
        hours = timeAmt / 3600
        #Change output message depending on time values
        if hours < 1 and minutes > 1:
            message = 'This command is on cooldown. Please wait {0:.2f} minutes, {1:.0f} seconds.'.format(
                minutes, seconds)
        elif hours < 1 and seconds < 1 and minutes > 1:
            message = 'This command is on cooldown. Please wait {0:.2f} minutes.'.format(
                hminutes)
        elif minutes < 1 and hours > 1:
            message = 'This command is on cooldown. Please wait {0:.2f} hours, {1:.0f} seconds.'.format(
                hours, seconds)
        elif seconds < 1 and hours > 1 and minutes > 1:
            message = 'This command is on cooldown. Please wait {0:.2f} hours, {1:.0f} minutes.'.format(
                hours, minutes)
        else:
            message = 'This command is on cooldown. Please wait {0:.2f} hours, {1:.2f} minutes, {2:.0f} seconds.'.format(
                hours, minutes, seconds)
        await ctx.send(message)


#Help
@bot.command(name='help')
async def help(ctx):
    contents = [
        "HELP \n **Core Commands**\ngoose say - Honkers will say whatever you'd like them to!\n   goose say <message>\n   b!lastAuthor - Shows the last person to use goose say\n",
        "**Setup commands**\nsetChannel - Set the channel for Honkers to welcome members in, please only enter channel names, not tags/IDs!\nwelcOff - Turns off Honker's welcome messages, these are off by default\n welcOn - Turn on Honker's welcome messages\ninvite - Invite Honkers!\nserver - Get the link for the Honkers Information and Support Server (HISS) \n info - Shows basic information about Honkers\n stats - Shows some fun stats about Honkers",
        "**Game Commands**\nhonkStart - Starts the game!\nhonkDaily - Gives you a random amount of coins, has a 12 hour cooldown\nhonkFind - Honkers will find an object for you! Has a cooldown of 30 minutes\nhonkListItems - Lists the items in your inventory\nview - Shows any item\n  b!view <item> \nhonkSell - Sells whichever item you name\n    b!honkSell <item>\nhonkCheck - Checks your balance\nhonkAttack - Pay Honkers 100 coins to attack a user\n   b!honkAttack @<user>\nhonkDonate - Give money to someone\n    b!honkDonate <amount> <user>\nhonkRob - Rob a user of their hard earned coins! Honkers only has a 1/5 chance of succeeding and will give 200-800 coins on success. This command has a 2 minute cooldown regardless of success or failure.\n   b!honkRob <user>\nhonkGif - Sends a random goose gif! Doesn't require any coins to activate\n vote - Sends a voting link for Honkers, gives between 400 and 600 coins and has a 12 hour cooldown",
        "**Moderation Commands** These are all admin commands excluding blacklistLs. They all have to be executing by someone with an 'Admin' role\ngooseOff - Turn Honkers off in *all* channels(only turns off responding to goose, honk, and duck-the game will still work)\n   b!gooseOff\ngooseOn - Turn Honkers on if previously turned off\n    b!gooseOn\ngooseIgnore - Shushes goose in *only* the channel the message is sent in\n   b!gooseIgnore\nrmGooseIgnore - Un-shushes Honker's lovely messages *only* in the channel the message is sent in\n    b!rmGooseIgnore\nblacklistAdd - Creates a blacklist and adds a word to it\nblacklistRm - Removes a word from the blacklist\ndelBlacklist - Deletes the blacklist\nblacklistLs - Lists the blacklist"
    ]
    pages = 4
    cur_page = 1
    await ctx.send(
        "*Please use b!report <error> to report any bug that you may come across, thanks!*\n*Honkers' prefix is b!*\n"
    )
    message = await ctx.send(
        f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add",
                                                timeout=60,
                                                check=check)
            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(
                    content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}"
                )
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(
                    content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}"
                )
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.remove_reaction(reaction, user)
            break
            # ending the loop if user doesn't react after a minute


async def statusTask():
    while True:
        servers = len(bot.guilds)
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name="b!help | b!report"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(name='Goose Simulator')
                                  )
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.streaming, name="b!help | b!report"))
        await asyncio.sleep(60)
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name='{0} servers'.format(servers)))
        await asyncio.sleep(60)


@bot.event
async def on_ready():
    print("I'm in")
    print(bot.user)
    bot.loop.create_task(statusTask())


@bot.event
async def on_guild_join(guild):
    serverId = guild.id
    serverName = guild.name
    file = open(".//serverInfo//{0}".format(serverId), "w")
    file.write(
        "gooseMode = True\nwelcomeChannel = general\nwelcomeStatus = off\nlastAuthor = None\n, Ignored Channels = None"
    )
    print("Wrote info to new server doc,  {0}".format(serverName))


@bot.event
async def on_guild_remove(guild):
    serverId = guild.id
    try:
        print("Left server {0}, {1}".format(guild.id, guild.name))
        os.remove(".//serverInfo//{0}".format(serverId))
        os.remove(".//serverInfo//BL{0}.txt".format(serverId))
    except FileNotFoundError:
        pass


@bot.event
async def on_member_join(member):
    try:
        serverId = member.guild.id
        if "off" not in await findVal(
                ".//serverInfo//{0}".format(str(serverId)), "welcomeStatus"):
            memberId = "<@{0}>".format(member.id)
            channelName = await findVal(
                ".//serverInfo//{0}".format(str(serverId)), "welcomeChannel")
            channel = discord.utils.get(member.guild.text_channels, name=str(channelName.strip()))
            await channel.send("Everyone welcome {0} to {1}!".format(
                memberId, member.guild.name))
    except FileNotFoundError:
        serverId = member.guild.id
        file = open(".//serverInfo//{0}".format(serverId), "w")
        file.write(
            "gooseMode = True\nwelcomeChannel = general\nwelcomeStatus = off\nlastAuthor = None\n, Ignored Channels = None"
        )
        print("Wrote info to new server doc after shut off, {0}, {1}".format(serverId, member.guild.name))


#Sends invite link
@bot.command(name='invite')
async def invite(ctx):
    await ctx.send(
        "Here's the invite link: https://discord.com/api/oauth2/authorize?client_id=758421614592786495&permissions=1543760912&scope=bot"
    )


@bot.command(name='vote')
@commands.cooldown(1, 43200, commands.BucketType.user)
async def vote(ctx):
    await ctx.send(
        "Here's the voting link: https://top.gg/bot/758421614592786495/vote")
    amount = random.randrange(400, 600)
    await ctx.send("You've been given {0} coins in return!".format(amount))
    await addCoin(str(ctx.author), amount)


#Sends the invite link to the support server
@bot.command(name='server')
async def serverInvite(ctx):
    await ctx.send("HISS = https://discord.gg/XPBkdBDhqa")


#Shows basic info about the bot
@bot.command(name="info")
async def info(ctx):
    servers = bot.guilds
    members = 0
    for s in servers:
        members += s.member_count
    await ctx.send(
        "*Info*\n**Credits**\nHonkers was made by Lethera!\n**Help**\nYou can join the Honkers Information and Support Server(HISS) with this link:\n       https://discord.gg/XPBkdBDhqa\n**Users**\n Honkers is currently in {0} servers with {1} users total!\n All GIFs were taken from GIPHY and all sprites were drawn by me"
        .format(len(servers), members))


#Displays fun bot stats
@bot.command(name='stats')
async def stats(ctx):
    honkCount = await findVal(".//stats.txt", "honkCount")
    await ctx.send("Honkers has honked {0} times and is in {1} servers!".format(honkCount, len(bot.guilds)))


#Turn off welcome messages
@bot.command(name='welcOff', help='Turns the welcome messages off for the bot')
async def welcOff(ctx):
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    if role in ctx.author.roles:
        welcStatus = await findVal(
            ".//serverInfo//{0}".format(str(ctx.guild.id)), "welcomeStatus")
        if "on" in welcStatus:
            await replaceVal(".//serverInfo//{0}".format(str(ctx.guild.id)),
                             "welcomeStatus", "off")
            await ctx.send("Turned the welcome messages off")
        else:
            await ctx.send("The welcome messages are already off!")
    else:
        await ctx.send(
            "You don't have the correct role, only an admin can do that!")


@bot.command(name='welcOn')
async def welcOn(ctx):
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    if role in ctx.author.roles:
        welcStatus = await findVal(
            ".//serverInfo//{0}".format(str(ctx.guild.id)), "welcomeStatus")
        if "off" in welcStatus:
            await replaceVal(".//serverInfo//{0}".format(str(ctx.guild.id)),
                             "welcomeStatus", "on")
            welcChannel = await findVal(
                ".//serverInfo//{0}".format(str(ctx.guild.id)),
                "welcomeChannel")
            await ctx.send(
                "Turned the welcome messages on in {0}".format(welcChannel))
        else:
            await ctx.send("The welcome messages are already on!")
    else:
        await ctx.send(
            "You don't have the correct role, only an admin can do that!")


@bot.command(name='honkStart', help="Starts the item game!")
async def honkStart(ctx):
    if await findVal("userBal.txt", ctx.message.author.id) != None:
        await ctx.send(
            "You've already started the item game, do b!help for more info!")
    else:
        userData = open("userBal.txt", "a")
        userData.write("\n{0} = 0".format(str(ctx.message.author.id)))
        fileName = ".//userItems//{0}Items".format(ctx.message.author.id)
        userItems = open(fileName, "a")
        userItems.close()
        await ctx.send("You've started the game, do b!help for commands!")
        print("New person started the game!")


@bot.command(
    name='setChannel',
    help=
    'Admin command, changes the channel that the bot will put announcements in.'
)
async def setChannel(ctx, channel):
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    if role in ctx.author.roles or ctx.author.id == lethId:
        if any(c.isalpha() for c in channel):
          await replaceVal(".//serverInfo//{0}".format(ctx.guild.id),
                         "welcomeChannel", str(channel))
          await ctx.channel.send(
            "Changed the announcement channel to {0}".format(channel))
        else:
          await ctx.channel.send("Whoa! Looks like that's a channel ID/tag, please only enter channel names!")
    else:
        await ctx.send(
            "You don't have the correct role, only an admin can do that!")


@bot.command(name='report', help='Report any bugs that you may come across.')
async def reportBug(ctx):
    f = open("errors", "a")
    f.write("\n{0} - {1}".format(ctx.message.content[8:], ctx.message.author))
    await ctx.send("Recorded your report!")


@bot.command(name='honkDaily')
@commands.cooldown(1, 10800, commands.BucketType.user)
async def daily(ctx):
    amount = random.randrange(100, 500)
    await addCoin(str(ctx.author.id), amount)
    await ctx.send("You recieved {0} coins!".format(amount))


@bot.command(name='honkGif', help='Goose will give you a random goose-gif!')
async def honkGif(ctx):
    gifChoice = random.choice(goose_general_gifs)
    await ctx.send("Goose gif incoming...")
    time.sleep(1)
    await ctx.send(
        file=discord.File(".//GIFS//gooseGen//{0}.gif".format(gifChoice)))


#Honkers sends a gif to "attack" people
@bot.command(name='honkAttack', help='Pay Goose 100 coins to "attack" someone')
async def honkAttack(ctx, member: Member):
    authorId = "<@{0}>".format(ctx.author.id)
    victimId = "<@{0}>".format(member.id)
    balance = await findVal("userBal.txt", ctx.author.id)
    print(balance)
    if float(balance) < 50:
        await ctx.send("It looks like you don't have enough money!")
    else:
        await ctx.send("{0} has paid Goose 50 coins to attack {1}".format(
            authorId, victimId))
        await subCoin(str(ctx.author.id), 50)
        #Choose a random gif to send
        gifChoice = random.choice(goose_attack_gifs)
        await ctx.send(
            file=discord.File(".//GIFS//attackGifs//{0}.gif".format(gifChoice))
        )
        print("Sent {0} as an attack gif".format(gifChoice))
        time.sleep(1)
        await ctx.send("Goose has brutally anihilated {0}".format(victimId))


#Find Items
@bot.command(name='honkFind',
             help='Goose finds an object for you! Has a 30 min cooldown')
@commands.cooldown(1, 1800, commands.BucketType.user)
async def honkFind(ctx):
    #Randomly find an item in a random tier catergory
    rng = random.randrange(0, 1000)
    if rng < 600:
        foundItem = random.choice(commonItems)
        itemValue = await calculateValue(foundItem)
        message = "Goose found **{0}**, it's worth {1} coins".format(
            foundItem, itemValue)
    elif rng < 900:
        foundItem = random.choice(rareItems)
        itemValue = await calculateValue(foundItem)
        message = "Goose found **{0}**, it's worth {1} coins".format(
            foundItem, itemValue)
    elif rng == 999:
        founditem = "A Goose Child"
        message = "Goose has brought {0}, they must really trust you!!!".format(
            foundItem)
    else:
        foundItem = random.choice(legendaryItems)
        itemValue = await calculateValue(foundItem)
        message = "Goose found **{0}**, it's worth {1} coins".format(
            foundItem, itemValue)
    if os.path.isfile(".//userItems//{0}Items".format(ctx.message.author.id)):
        try:
            await ctx.send(message)
            await ctx.send(
                file=discord.File(".//itemSprites//{0}.png".format(foundItem)))
            fileName = ".//userItems//{0}Items".format(ctx.message.author.id)
            userItems = open(fileName, "a+")
            userItems.write("{0}\n".format(foundItem))
            await cleanFile(userItems)
        except TypeError:
            pass
    else:
        await ctx.send(
            "Looks like you haven't started the game yet, send b!honkStart!")


@bot.command(name='view')
async def viewItem(ctx, *args):
    item = " ".join(args[:])
    message = ''
    if os.path.isfile(".//itemDescriptions//{0}.txt".format(item)):
        itemDesc = open('.//itemDescriptions//{0}.txt'.format(item), 'r')
        if item in commonItems:
            message = ' \nThis is a *common* item.'
        elif item in rareItems:
            message = ' \nThis is a **rare** item.'
        elif item in legendaryItems:
            message = ' \nThis is a ***Legendary*** item!'
        await ctx.send("{0}{1}".format(itemDesc.read(), message))
        await ctx.send(
            file=discord.File(".//itemSprites//{0}.png".format(item)))
    else:
        await ctx.send("That's not an item!")


@bot.command(name='honkListItems',
             help='Lists all of the items in your inventory!')
async def listItems(ctx):
    fileName = ".//userItems//{0}Items".format(ctx.message.author.id)
    if os.path.isfile(fileName):
        userItems = open(fileName, "r+")
        data = userItems.read()
        await ctx.send(data)
        userItems.close()
    else:
        await ctx.send("You haven't started the game, do b!honkStart!")


@bot.command(name='honkSell', help='Sells an exact item in your inventory')
async def sellItem(ctx, *args):
    item = " ".join(args[:])
    userItems = open(".//userItems//{0}Items".format(ctx.message.author.id),
                     "r")
    data = userItems.read()
    lines = userItems.readlines()
    if item in data:
        if item != "A Goose Child":
            try:
                itemPrice = await calculateValue(item)
                await ctx.send("You sold **{0}** for {1} coins".format(
                    item, itemPrice))
                await addCoin(str(ctx.author.id), itemPrice)
                data = data.replace(item, "")
                userItems.close()
                with open(
                        ".//userItems//{0}Items".format(ctx.message.author.id),
                        "w") as f:
                    f.write(data)
                await cleanFile(userItems)
            except TypeError:
                pass
        else:
            await ctx.send(
                "You can't sell the Goose Child!! Honkers wouldn't be very happy!"
            )
    else:
        await ctx.send("You don't have that item in your inventory!")


@bot.command(
    name='honkRemove',
    help='Takes money from a user, format = b!honkRemove <amount> <user>')
async def honkRemove(ctx, amount, member: Member):
    if ctx.author.id == lethId:
        if await findVal("userBal.txt", ctx.author.id) != None:
            user = "{0}".format(member.id)
            userPing = "<@{0}>".format(member.id)
            prevAmt = float(await findVal("userBal.txt", user))
            await subCoin(user, amount)
            curAmt = float(await findVal("userBal.txt", user))
            await ctx.send(
                "The balance of {0} has been updated from {1} to {2}".format(
                    userPing, prevAmt, curAmt))
        else:
            userData = open("userBal.txt", "a")
            userData.write("\n{0} = 0".format(str(member.id)))
            user = "{0}".format(member.id)
            userPing = "<@{0}>".format(member.id)
            prevAmt = float(await findVal("userBal.txt", user))
            await subCoin(user, amount)
            curAmt = float(await findVal("userBal.txt", user))
            await ctx.send(
                "The balance of {0} has been updated from {1} to {2}".format(
                    userPing, prevAmt, curAmt))
    else:
        await ctx.send("You don't have the correct role!")


@bot.command(
    name='honkGive',
    help='Gives money to a user, format == b!honkGive <amount> @<user>')
async def honkGive(ctx, amount, member: Member):
    recId = "{0}".format(ctx.author.id)
    if ctx.author.id == lethId:
        if await findVal("userBal.txt", ctx.author) != None:
            recUser = "<@{0}>".format(member.id)
            balance = await findVal("userBal.txt", recId)
            prevAmt = float(balance)
            await addCoin(recId, float(amount))
            curAmt = float(await findVal("userBal.txt", recId))
            await ctx.send(
                "The balance of <@{0}> has been updated from {1} to {2}".
                format(recId, prevAmt, curAmt))
        else:
            userData = open("userBal.txt", "a")
            userData.write("\n{0} = 0".format(str(ctx.message.author)))
            userId = "{0}".format(member.id)
            prevAmt = float(await findVal("userBal.txt", userId))
            await addCoin(userId, amount)
            curAmt = float(await findVal("userBal.txt", userId))
            await ctx.send(
                "The balance of <@{0}> has been updated from {1} to {2}".
                format(userId, prevAmt, curAmt))
    else:
        await ctx.send("You don't have the correct role!")


#Turn goose off in only one channel
@bot.command(
    name='gooseIgnore',
    help=
    "An admin command, only turn goose off in the channel that the command is sent in"
)
async def goose_ignore(ctx):
    ignoredChannels = str(await findVal(
        ".//serverInfo//{0}".format(str(ctx.guild.id)), "Ignored Channels"))
    currChannel = str(ctx.message.channel.id)
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    noHonk = True
    if role in ctx.author.roles:
        if currChannel not in ignoredChannels:
            await replaceVal(
                ".//serverInfo//{0}".format(str(ctx.guild.id)),
                "Ignored Channels", "{0} {1}".format(
                    str(await
                        findVal(".//serverInfo//{0}".format(str(ctx.guild.id)),
                                "Ignored Channels")), currChannel))
        else:
            await ctx.send("This channel is already ignored!")
    else:
        await ctx.send("You don't have permission to do that!")


#Unignores a channel
@bot.command(name='rmGooseIgnore',
             help="And admin command, unignores a channel")
async def unignoreChannel(ctx):
    ignoredChannels = str(await findVal(
        ".//serverInfo//{0}".format(str(ctx.guild.id)), "Ignored Channels"))
    currChannel = str(ctx.message.channel.id)
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    if role in ctx.author.roles or ctx.author.id == lethId:
        if currChannel in ignoredChannels:
            newStrLen = len(ignoredChannels) - len(currChannel)
            await replaceVal(".//serverInfo//{0}".format(str(ctx.guild.id)),
                             "Ignored Channels",
                             str(ignoredChannels[0:newStrLen]))
        else:
            await ctx.send("This channel isn't ignored!")
    else:
        await ctx.send("You don't have permission to do that!")


#Turn Goose on or off
@bot.command(name='gooseOff', help='Admin command, turns Goose off')
async def goose_off(ctx):
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    if role in ctx.author.roles or ctx.author.id == lethId:
        await replaceVal(".//serverInfo//{0}".format(str(ctx.guild.id)),
                         "gooseMode", "False")
    else:
        await ctx.send(
            "You don't have the correct role, only an admin can do that!")


@bot.command(name='gooseOn', help='Admin command, turns Goose on')
async def goose_on(ctx):
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    if role in ctx.author.roles or ctx.author.id == lethId:
        await replaceVal(".//serverInfo//{0}".format(str(ctx.guild.id)),
                         "gooseMode", "True")
    else:
        await ctx.send(
            "You don't have the correct role, only an admin can do that!")


@bot.command(name='delBlacklist', help='Admin Command, deletes the blacklist')
async def rmBlacklist(ctx):
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    if role in ctx.author.roles or ctx.author.id == lethId:
        if os.path.isfile('.//serverInfo//BL{0}.txt'.format(ctx.guild.id)):
            os.remove('.//serverInfo//BL{0}.txt'.format(ctx.guild.id))
            await ctx.send("Removed your blacklist!")
        else:
            await ctx.send("You don't have a blacklist!")
    else:
        await ctx.send(
            "You don't have the correct role, only an admin can do that!")


@bot.command(name='blacklistAdd',
             help='Admin command, creates a blacklist and adds a word to it')
async def blacklist_add(ctx, message):
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    if role in ctx.author.roles or ctx.author.id == lethId:
        f = open(".//serverInfo//BL{0}.txt".format((ctx.guild.id)), "a")
        f.write("{0}\n".format(str(ctx.message.content)[15:]))
        await ctx.send('Placed {0} in the blacklist'.format(
            str(ctx.message.content)[15:]))
    else:
        await ctx.send(
            "You don't have the correct role, only an admin can do that!")


@bot.command(name='blacklistRm',
             help='Admin command, removes a word from the blacklist')
async def blacklist_remove(ctx, message):
    role = discord.utils.get(ctx.guild.roles, name='Admin')
    phrase = str(ctx.message.content)[14:]
    if role in ctx.author.roles or ctx.author.id == lethId:
        f = open(".//serverInfo//BL{0}.txt".format(ctx.guild.id), "r")
        data = f.readlines()
        file = open(".//serverInfo//BL{0}.txt".format(ctx.guild.id), "w")
        for line in data:
            if phrase not in line:
                file.write(line)
        await ctx.send('Removed {0} from the blacklist'.format(
            str(ctx.message.content)[14:]))
    else:
        await ctx.send(
            "You don't have the correct role, only an admin can do that!")


@bot.command(name='blacklistLs', help='Lists the blacklist')
async def blacklist_list(ctx):
    if os.path.isfile(".//serverInfo//BL{0}.txt".format(ctx.guild.id)):
        file = open(".//serverInfo//BL{0}.txt".format(ctx.guild.id), "r")
        await ctx.send(file.read())
    else:
        await ctx.send("You don't have a blacklist!")


@bot.command(name='honkCheck', help='Checks your balance')
async def honkCheck(ctx):
    balance = await findVal("userBal.txt", ctx.message.author.id)
    if float(balance) == None:
        await startError(ctx)
    else:
        await ctx.send("Your balance is {0} coins".format(float(balance)))


@bot.command(
    name='honkDonate',
    help='Give coins to another user, format = b!honkDonate <amount> <user>')
async def coinDonate(ctx, amount, member: Member):
    givingUser = "{0}".format(ctx.message.author.id)
    recUser = "{0}".format(member.id)
    rUserPing = "<@{0}>".format(member.id)
    await subCoin(givingUser, amount)
    await addCoin(recUser, amount)
    await ctx.send("You gave {0} coins to {1}".format(amount, rUserPing))


@bot.command(
    name='honkRob',
    help=
    'Robs another user, has a 1/5 chance to succeed, gives between 200 and 800 coins, or however many the user has if below the random amount'
)
@commands.cooldown(1, 60, commands.BucketType.user)
async def honkRob(ctx, member: Member):
    robbedUser = "{0}".format(member.name)
    robbedUserId = "{0}".format(member.id)
    thiefUserId = "{0}".format(ctx.author.id)
    users = open(".//userBal.txt".format(ctx.guild.id), "r")
    data = users.read()
    if robbedUserId in data and thiefUserId in data:
        #Chance of success
        randNum = random.randrange(0, 5)
        print("{0} = steal chance".format(randNum))
        #Success
        if randNum == 1:
            stealAmt = random.randrange(200, 800)
            robUserBal = float(await findVal("userBal.txt", robbedUserId))
            #There's not enough money
            if robUserBal < stealAmt:
                await ctx.send(
                    "{0} doesn't have {1} to be taken, but Goose took everything they had!"
                    .format(robbedUser, stealAmt))
                newAmt = float(await findVal("userBal.txt", robbedUserId))
                await addCoin(thiefUserId, newAmt)
                await subCoin(robbedUserId, newAmt)
            else:
                await addCoin(thiefUserId, stealAmt)
                await subCoin(robbedUserId, stealAmt)
                await ctx.send("You stole {0} from {1}".format(
                    stealAmt, robbedUser))
        #Failure
        else:
            await ctx.send("Oh no! Goose couldn't pull it off!")
    else:
        await ctx.send(
            "Oh no! Either you or the target haven't started the game and thus have no coins to steal! Do b!honkStart"
        )


@bot.command(name='lastAuthor', help='Shows the last person to use goose say')
async def lastAuthor(ctx):
    lastAuthor = await findVal(
        ".//serverInfo//{0}".format(str(ctx.message.guild.id)), "lastAuthor")
    await ctx.send(lastAuthor)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    channel = message.channel
    noHonk = False
    #Check if the message is a DM, will always honk if so (ignores gooseMode)
    if isinstance(message.channel, discord.channel.DMChannel):
        #Ignore own messages
        if (message.author.bot):
            return
        else:
            if (message.content.lower().startswith('goose say')):
                await channel.send(message.content[10:])
                await replaceVal(
                    ".//serverInfo//{0}".format(str(message.guild.id)),
                    "lastAuthor", str(message.author))
                await message.delete()
                noHonk = True
            if ('duck' in message.content.lower()):
                await channel.send(random.choice(duck_responses))
                noHonk = True
            elif ('goose' in message.content.lower() and noHonk == False):
                await channel.send("HONK")
                honks = int(await findVal(".stats.txt", "honkCount")) + 1
                await replaceVal(".stats.txt", "honkCount", honks)
            elif ('HONK' in message.content.upper()
                  and 'b!' not in message.content.lower() and noHonk == False):
                await channel.send("goose")
                honks = int(await findVal(".stats.txt", "honkCount")) + 1
                await replaceVal(".stats.txt", "honkCount", honks)

    else:
        try:
            gooseMode = await findVal(
                ".//serverInfo//{0}".format(str(message.guild.id)),
                "gooseMode")
            #Ignore bot messages
            if (message.author.bot):
                return
            else:
                if ("True" in gooseMode):
                    try:
                        #Check if messages contain trigger words
                        if (message.content.lower().startswith('goose say')):
                            await channel.send(message.content[10:])
                            await replaceVal(
                                ".//serverInfo//{0}".format(
                                    str(message.guild.id)), "lastAuthor",
                                str(message.author))
                            await message.delete()
                            noHonk = True
                        if ('duck' in message.content.lower()
                                and str(channel.id) not in str(await findVal(
                                    ".//serverInfo//{0}".format(
                                        str(message.guild.id)),
                                    "Ignored Channels"))
                                and 'b!' not in message.content.lower()):
                            await channel.send(random.choice(duck_responses))
                            noHonk = True
                        elif ('goose' in message.content.lower()
                              and noHonk == False
                              and str(channel.id) not in str(await findVal(
                                  ".//serverInfo//{0}".format(
                                      str(message.guild.id)),
                                  "Ignored Channels"))
                              and 'b!' not in message.content.lower()):
                            await channel.send("HONK")
                            honks = int(await findVal(".//stats.txt",
                                                      "honkCount")) + 1
                            await replaceVal(".//stats.txt", "honkCount",
                                             honks)
                        elif ('HONK' in message.content.upper()
                              and 'b!' not in message.content.lower()
                              and noHonk == False
                              and str(channel.id) not in str(await findVal(
                                  ".//serverInfo//{0}".format(
                                      str(message.guild.id)),
                                  "Ignored Channels"))):
                            await channel.send("goose")
                            honks = int(await findVal(".//stats.txt",
                                                      "honkCount")) + 1
                            await replaceVal(".//stats.txt", "honkCount",
                                             honks)
                        elif (gooseMode == ' False'
                              and 'b!' not in message.content.lower()
                              and 'goose' in message.content.lower()
                              or 'HONK' in message.content.upper()
                              and gooseMode == 'False'
                              or 'duck' in message.content.lower()
                              and gooseMode == 'False'
                              or 'goose say' in message.content.lower()
                              and gooseMode == 'False'):
                            await channel.send(
                                'Sorry, Goose has been disabled :(')
                        #Word sent that is in blacklist
                        elif os.path.isfile(".//serverInfo//BL{0}.txt".format(
                                message.guild.id)):
                            f = open(
                                ".//serverInfo//BL{0}.txt".format(
                                    message.guild.id), "r").readlines()
                            for line in f:
                                if line.strip('\n') in message.content.lower(
                                ) and len(line.strip('\n')) == len(
                                        message.content.lower()):
                                    await message.delete()
                                    await channel.send(
                                        "Detected a censored word!")
                    except discord.errors.Forbidden:
                        pass
        except FileNotFoundError:
            serverId = message.guild.id
            serverName = message.guild.name
            file = open(".//serverInfo//{0}".format(serverId), "w")
            file.write(
                "gooseMode = True\nwelcomeChannel = general\nwelcomeStatus = off\nlastAuthor = None\n"
            )
            print("Wrote info to new server doc after shut off, {0}, {1}".format(serverId, serverName))


async def calculateValue(item):
    if item in commonItems:
        itemPrice = len(item) * 5
    elif item in rareItems:
        itemPrice = len(item) * 7
    elif item in legendaryItems:
        itemPrice = len(item) * 10
    return itemPrice


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)
