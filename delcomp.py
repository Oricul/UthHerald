#!/usr/bin/env python3
import discord
from discord.ext import commands
import discord.utils
import time
import os
import asyncio
import ADMIN
import formatting

global log
global tlog
global dellist
global broadtog
log = []
tlog = []
dellist = []
broadtog = []

with open('delete_on.log','a+') as delme:
    delme.seek(0)
    dellist = delme.read().splitlines()
#    print(dellist)

with open ('broad_delete.log','a+') as broadme:
    broadme.seek(0)
    broadtog = broadme.read().splitlines()
#    print(broadtog)

async def defdel(meslog,timlog,chanlog):
    if chanlog in dellist:
        log.append(meslog)
        tlog.append(timlog)

async def broadto(srvid):
    if not srvid in broadtog:
        return 'True'
    else:
        return 'False'

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
        await ADMIN.addcount('?deltoggle')
        await formatting.toDel(ctx.message,ctx)
        global dellist
        if ctx.message.author.id == ctx.message.server.owner.id:
            if not '{}#{}'.format(ctx.message.server.id,ctx.message.channel.name) in dellist:
                with open('delete_on.log','a+') as delme:
                    delme.write('{}#{}\n'.format(ctx.message.server.id,ctx.message.channel.name))
                    delme.seek(0)
                    dellist = delme.read().splitlines()
                readysend = await formatting.emMsg('ENABLED MESSAGE DELETION','I will now delete commands and responses in this channel, server permissions permitting.',0x00FF00,self.bot.user.name,self.bot.user.avatar_url)
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
            else:
                with open('delete_on.log','w+') as delme:
                    for line in dellist:
                        if not line == '{}#{}'.format(ctx.message.server.id,ctx.message.channel.name):
                            delme.write('{}\n'.format(line))
                    delme.seek(0)
                    dellist = delme.read().splitlines()
                readysend = await formatting.emMsg('DISABLED MESSAGE DELETION','I will no longer delete commands and responses in this channel.',0x00FF00,self.bot.user.name,self.bot.user.avatar_url)
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
        else:
            readysend = await formatting.emMsg('NOT ALLOWED','You must be the server owner to utilize this command.',0xFF0000,self.bot.user.name,self.bot.user.avatar_url)
            msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
            await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True)
    async def supptoggle(self,ctx):
        'Toggle support messages on and off by server.'
        await ADMIN.addcount('?supptoggle')
        await formatting.toDel(ctx.message,ctx)
        global broadtog
        if ctx.message.author.id == ctx.message.server.owner.id:
            if not ctx.message.server.id in broadtog:
                with open('broad_delete.log','a+') as broadme:
                    broadme.write('{}\n'.format(ctx.message.server.id))
                    broadme.seek(0)
                    broadtog = broadme.read().splitlines()
                readysend = await formatting.emMsg('SUPPORT MESSAGES DISABLED','I will no longer send support messages to this server.\nYou will not receive status updates or new command notices.',0x00FF00,self.bot.user.name,self.bot.user.avatar_url)
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
            else:
                with open('broad_delete.log','w+') as broadme:
                    for line in broadtog:
                        if not line == '{}'.format(ctx.message.server.id):
                            broadme.write('{}\n'.format(line))
                    broadme.seek(0)
                    broadtog = broadme.read().splitlines()
                readysend = await formatting.emMsg('SUPPORT MESSAGES ENABLED','I will now send support messages to this server.',0x00FF00,self.bot.user.name,self.bot.user.avatar_url)
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
        else:
            readysend = await formatting.emMsg('NOT ALLOWED','You must be the server owner to utilize this command.',0xFF0000,self.bot.user.name,self.bot.user.avatar_url)
            await self.bot.send_message(ctx.message.channel, embed=readysend)
            await formatting.toDel(msg,ctx)

def setup(bot):
    bot.add_cog(SAdmin(bot))
