#!/usr/bin/env python3
"""'discord' is the default module for Discord bots.
'json' is used to hide private information from GitHub using .ignore.
'commands' from 'discord.ext' because of additional Discord commands and because we're not on rewrite.
'python_version' from 'platform' gives us the Python version. Useful as a startup message for troubleshooting.
'Shortener' (or 'short') from 'pyshorteners' allows us to create a short URL for our bot's OAUTH URL.
'print' from 'printoverride' is a custom module that causes all prints to immediately flush. Useful for PM2."""
import discord, json
from discord.ext import commands
from platform import python_version
from pyshorteners import Shortener as short
from printoverride import print

# Set the default cogs to load. Currently: 'RVR','General','ADMIN','delcomp'
startup_extensions = []

# Setup the description that is displayed when the user uses your help command.
description = '''Created by Orito.
                Special thanks to Armsperson for providing his JSON data.
                
                For support, visit: https://goo.gl/QuM7J8'''
# Set the bot's prefix here.
prefix = '?'
# Start building your bot command.
bot = commands.Bot(command_prefix=prefix,description=description)

# Setup welcome message and load all default cogs.
@bot.event
async def on_ready():
    onlineMSG = "* Logged in as '{0}' ({1}). *".format(bot.user.name,bot.user.id)
    dversionMSG = "Discord API v{0}".format(discord.__version__)
    pversionMSG = "Python3 v{0}".format(python_version())
    appinfo = await bot.application_info()
    ownMSG = "Owner: {0}".format(appinfo.owner)
    chanMSG = "Servers: {0}".format(len(bot.servers))
    userMSG = "Users: {0}".format(len(list(bot.get_all_members())))
    url = "{0}".format(discord.utils.oauth_url(bot.user.id))
    urlshort = short('Google',api_key=gToken)
    try:
        oauth = "OAuth URL: {0}".format(urlshort.short(url))
    except Exception as e:
        print("Google API failure.\nError: {0}".format(e))
        oauth = "Failed to generated OAuth URL."
    onDIV = '*'
    while len(onDIV) < len(onlineMSG):
        onDIV = onDIV + '*'
    onLEN = len(onlineMSG) - 2
    while len(dversionMSG) < onLEN:
        dversionMSG = ' ' + dversionMSG
        if len(dversionMSG) < onLEN:
            dversionMSG = dversionMSG + ' '
    dversionMSG = '*' + dversionMSG + '*'
    while len (pversionMSG) < onLEN:
        pversionMSG = ' ' + pversionMSG
        if len(pversionMSG) < onLEN:
            pversionMSG = pversionMSG + ' '
    pversionMSG = '*' + pversionMSG + '*'
    while len(ownMSG) < onLEN:
        ownMSG = ' ' + ownMSG
        if len(ownMSG) < onLEN:
            ownMSG = ownMSG + ' '
    ownMSG = '*' + ownMSG + '*'
    while len(chanMSG) < onLEN:
        chanMSG = ' ' + chanMSG
        if len(chanMSG) < onLEN:
            chanMSG = chanMSG + ' '
    chanMSG = '*' + chanMSG + '*'
    while len(userMSG) < onLEN:
        userMSG = ' ' + userMSG
        if len(userMSG) < onLEN:
            userMSG = userMSG + ' '
    userMSG = '*' + userMSG + '*'
    while len(oauth) < onLEN:
        oauth = ' ' + oauth
        if len(oauth) < onLEN:
            oauth = oauth + ' '
    oauth = '*' + oauth + '*'
    print("{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{0}".format(onDIV,onlineMSG,dversionMSG,pversionMSG,ownMSG,chanMSG,userMSG,oauth))
    if __name__ == '__main__':
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
                print('Loaded extension: {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__,e)
                print('Failed to load extension: {}\n{}'.format(extension,exc))


@bot.event
async def on_server_join(server):
    await bot.send_message(server, '```Hello! Thanks for choosing UthHerald. For a list of commands please use \'{0}help\'.```'.format(prefix))

bot.run(token)
