#!/usr/bin/env python3
from urllib.request import Request, urlopen
from urllib.error import URLError
import discord
from discord.ext import commands
import datetime
import json

startup_extensions = ['RVR','General','ADMIN']

description = 'Created by Orito <Sword of the Dragon>\nSpecial thanks to Armsperson for providing JSON access to his data.\n\nFor support visit: https://goo.gl/QuM7J8\n\nUpdated: 02/16/2017 00:46 GMT-6'
bot = commands.Bot(command_prefix='?', description=description)

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded extension: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__,e)
            print('Failed to load extension: {}\n{}'.format(extension, exc))

@bot.event
async def on_ready():
    onlineMSG = '* Logged in as \'' + bot.user.name + '\' (' + bot.user.id + '). *'
    onDIV = '*'
    while len(onDIV) < len(onlineMSG):
        onDIV = onDIV + '*'
    print(onDIV + '\n' + onlineMSG + '\n' + onDIV)
#    for server in bot.servers:
#        try:
#            await bot.send_message(discord.Object(id=server.id), '`Bot started. Now accepting commands.`')
#        except:
#            pass

@bot.event
async def on_server_join(server):
    await bot.send_message(server, '```Hello! Thanks for choosing UthHerald. For a list of commands, please use \'?help\'.```')

#Start the bot.
bot.run('REMOVED_KEY')
