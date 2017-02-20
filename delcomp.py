#!/usr/bin/env python3
import discord
from discord.ext import commands
import discord.utils
import time
import os
import asyncio

global log
global tlog
global dellist
log = []
tlog = []
dellist = []

with open('delete_on.log','a+') as delme:
    delme.seek(0)
    dellist = delme.read().splitlines()
    print(dellist)

async def defdel(meslog,timlog,chanlog):
    if chanlog in dellist:
        log.append(meslog)
        tlog.append(timlog)

class SAdmin():
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.call_soon(self.confdefdel)

    def confdefdel(self):
        self.bot.loop.create_task(self.delmsg())

    async def delmsg(self):
        while len(log) > 0:
            for i, j in zip(log, tlog):
                delete_at_time = j + 30.0
                while time.time() < delete_at_time:
                    await asyncio.sleep(1)
                try:
                    await self.bot.delete_message(i)
                except:
                    pass
                log.remove(i)
                tlog.remove(j)
        self.bot.loop.call_later(10, self.confdefdel)

    @commands.command(pass_context=True)
    async def deltoggle(self,ctx):
        'Toggle message deletion on and off by channel.'
        global dellist
        if ctx.message.author.id == ctx.message.server.owner.id:
            if not '{}#{}'.format(ctx.message.server.id,ctx.message.channel.name) in dellist:
                with open('delete_on.log','a+') as delme:
                    delme.write('{}#{}\n'.format(ctx.message.server.id,ctx.message.channel.name))
                    delme.seek(0)
                    dellist = delme.read().splitlines()
                await self.bot.say('`I will now delete commands and responses in this channel, server permissions permitting.`')
            else:
                with open('delete_on.log','w+') as delme:
                    for line in dellist:
                        if not line == '{}#{}'.format(ctx.message.server.id,ctx.message.channel.name):
                            delme.write('{}\n'.format(line))
                    delme.seek(0)
                    dellist = delme.read().splitlines()
                await self.bot.say('`I will no longer delete commands and responses in this channel.`')
        else:
            msg = await self.bot.say('`You must be the server owner to utilize this command.`')
            await defdel(msg,time.time(),ctx.message.server.id + '#' + ctx.message.channel.name)

def setup(bot):
    bot.add_cog(SAdmin(bot))
