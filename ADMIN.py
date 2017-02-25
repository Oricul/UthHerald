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
import delcomp
import formatting

global comcount
comcount = []

with open('command_count.log','a+') as comOpen:
    comOpen.seek(0)
    comcount = comOpen.read().splitlines()
    print(comcount)

async def addcount(comused):
    global comcount
    if any(comused in s for s in comcount):
        s = [i for i in comcount if comused in i]
        s = ''.join(s)
        comSan = s.split('#',1)[-1]
        comSaned = int(comSan) + 1
        with open('command_count.log','w+') as comOpen:
            for line in comcount:
                if line == '{}#{}'.format(comused,comSan):
                    comOpen.write('{}#{}\n'.format(comused,comSaned))
                else:
                    comOpen.write('{}\n'.format(line))
            comOpen.seek(0)
            comcount = comOpen.read().splitlines()
    else:
        with open('command_count.log','a+') as comOpen:
            comOpen.write('{}#{}\n'.format(comused,1))
            comOpen.seek(0)
            comcount = comOpen.read().splitlines()
    return
            

def is_owner_check(message):
    return message.author.id == '107270310344024064'

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


class ADMIN():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def count(self,ctx):
        'View how many times a command has been ran.'
        outmsg = ''
        for i in comcount:
            comSan = i.replace('#',' - ')
            outmsg = '{}{}\n'.format(outmsg,comSan)
        readysend = await formatting.emMsg('','{}'.format(outmsg),0x00FFFF,'Command Usage Count:',self.bot.user.avatar_url)
        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
        await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def load(self,ctx,extension_name : str):
        'Load an extension/category.'
        await formatting.toDel(ctx.message,ctx)
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            readysend = await formatting.emMsg('LOAD ERROR','There was an error loading module \'{}\'.\n\n{}: {}'.format(extension_name,type(e).__name__,str(e)),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
            msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
            await formatting.toDel(msg,ctx)
            return
        except Exception as e:
            readysend = await formatting.emMsg('UNKNOWN LOAD ERROR','There was an unknown error loading module \'{}\'.\n\n{}'.format(extension_name,e),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
            msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
            await formatting.toDel(msg,ctx)
        readysend = await formatting.emMsg('MODULE LOADED','Successfully loaded \'{}\'.'.format(extension_name),0x00FF00,self.bot.user.name,self.bot.user.avatar_url)
        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
        await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def unload(self, ctx, extension_name : str):
        'Unload an extension/category.'
        await formatting.toDel(ctx.message,ctx)
        self.bot.unload_extension(extension_name)
        readysend = await formatting.emMsg('MODULE UNLOADED','Successfully unloaded \'{}\'.'.format(extension_name),0x00FF00,self.bot.user.name,self.bot.user.avatar_url)
        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
        await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def reload(self, ctx, extension_name : str):
        'Reload an extension/category.'
        await formatting.toDel(ctx.message,ctx)
        self.bot.unload_extension(extension_name)
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            readysend = await formatting.emMsg('RELOAD ERROR','There was an error reloading module \'{}\'.\n\n{}: {}'.format(extension_name,type(e).__name__,str(e)),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
            msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
            await formatting.toDel(msg,ctx)
            return
        readysend = await formatting.emMsg('MODULE RELOADED','Successfully reloaded \'{}\'.'.format(extension_name),0x00FF00,self.bot.user.name,self.bot.user.avatar_url)
        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
        await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def broadcast(self, ctx, *, inputmsg : str):
        'Send a message to all server\'s default channel, if permissions allow it.'
        await formatting.toDel(ctx.message,ctx)
        for server in self.bot.servers:
            cani = await delcomp.broadto(server.id)
            if cani == 'True':
                try:
                    readysend = await formatting.emMsg('','{}'.format(inputmsg),0x00FFFF,'Broadcast from {}:'.format(ctx.message.author.name),ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(discord.Object(id=server.id), embed=readysend)
                    await formatting.toDel(msg,ctx)
                except:
                    pass
        msg = await self.bot.say('`Broadcast complete.`')


    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def sayit(self,ctx,*,saywhat : str):
        await delcomp.defdel(ctx.message,time.time(),ctx.message.server.id + '#' + ctx.message.channel.name)
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

    #@broadcast.error
    #async def variablemissing(self, error, ctw):
    #    msg = await self.bot.say('`Missing message input. Proper usage: ?broadcast <message>`')
    #    return

    @load.error
    @unload.error
    @reload.error
    #@sayit.error
    async def permission_error(self, error, ctw):
        error = str(error)
        if 'The check functions for command' in error:
            title = 'HIDDEN COMMAND'
            result = 'You\'ve found a hidden admin command. You do not have permissions to use it, sorry!'
        elif 'NameError' in error:
            title = 'MODULE DOES NOT EXIT'
            result = 'That module does not exist.'
        else:
            title = 'FATAL ERROR'
            result = '{} : {}\nContact Orito with the above error.'.format(error,ctw)
        readysend = await formatting.emMsg(title,result,0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
        msg = await self.bot.say(embed=readysend)
        return

def setup(bot):
    bot.add_cog(ADMIN(bot))
