#!/usr/bin/env python3
from urllib.request import Request, urlopen
from urllib.error import URLError
import discord
from discord.ext import commands
import discord.utils
import datetime
import json
import time
import asyncio
import inspect

global log
log = []
global tlog
tlog = []

async def defdel(meslog,timlog):
    log.append(meslog)
    tlog.append(timlog)


def is_owner_check(message):
    return message.author.id == '107270310344024064'

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


class ADMIN():
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.call_soon(self.confdefdel)

    def confdefdel(self):
        self.bot.loop.create_task(self.delmsg())

    async def delmsg(self):
        while len(log) > 0:
            for i, j in zip(log,tlog):
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

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def load(self,ctx,extension_name : str):
        'Load an extension/category.'
        await defdel(ctx.message,time.time())
        try:
            self.bot.load_extension(extension_name)
        except ImportError:
            msg = await self.bot.say('```py\n{}: {}\n```'.format(type(e).__name__, str(e)))
            await defdel(msg,time.time())
            return
        msg = await self.bot.say('```py\n\'{}\' loaded.\n```'.format(extension_name))
        await defdel(msg,time.time())

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def unload(self, ctx, extension_name : str):
        'Unload an extension/category.'
        await defdel(ctx.message,time.time())
        self.bot.unload_extension(extension_name)
        msg = await self.bot.say('```py\n\'{}\' unloaded.\n```'.format(extension_name))
        await defdel(msg,time.time())

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def reload(self, ctx, extension_name : str):
        'Reload an extension/category.'
        await defdel(ctx.message,time.time())
        self.bot.unload_extension(extension_name)
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            msg = await self.bot.say('```py\n{}: {}\n```'.format(type(e).__name__, str(e)))
            await defdel(msg,time.time())
            return
        msg = await self.bot.say('```py\n\'{}\' reloaded.\n```'.format(extension_name))
        await defdel(msg,time.time())

    @commands.command(hidden=True)
    @is_owner()
    async def broadcast(self, *, input : str):
        'Send a message to all server\'s default channel, if permissions allow it.'
        for server in self.bot.servers:
            try:
                message = await self.bot.send_message(discord.Object(id=server.id), '`' + input + '`')
            except:
                pass
        msg = await self.bot.say('`Broadcast complete.`')

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def sayit(self,ctx,*,saywhat : str):
        await defdel(ctx.message,time.time())
        await self.bot.say(saywhat)
        return

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def debug(self, ctx, *, code : str):
        'Evaluate code.'
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author
            }
        env.update(globals())
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
            return
        await self.bot.say(python.format(result))

    @broadcast.error
    async def variablemissing(self, error, ctw):
        msg = await self.bot.say('`Missing message input. Proper usage: ?broadcast <message>`')
        return

    @load.error
    @unload.error
    @reload.error
    @sayit.error
    async def permission_error(self, error, ctw):
        error = str(error)
        if 'The check functions for command' in error:
            result = '```You\'ve found a hidden admin command. You do not have permissions to use it, sorry!```'
        elif 'NameError' in error:
            result = '```That module does not exist.```'
        else:
            result = '```Fatal error: {} : {}\nContact Orito with the above error.```'.format(error,ctw)
        msg = await self.bot.say(result)
        return

def setup(bot):
    bot.add_cog(ADMIN(bot))
