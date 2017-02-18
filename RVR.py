#!/usr/bin/env python3
from urllib.request import Request, urlopen
from urllib.error import URLError
import discord
from discord.ext import commands
import datetime
import json
import time
import asyncio

global log
log = []
global tlog
tlog = []

def defdel(meslog,timlog):
    log.append(meslog)
    tlog.append(timlog)

class RVR():
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
                await self.bot.delete_message(i)
                log.remove(i)
                tlog.remove(j)
        self.bot.loop.call_later(10, self.confdefdel)

    @commands.command()
    async def df(self):
        'Returns the current realm that owns Darkness Falls.'
        try:
            response = urlopen('http://uthgard.riftmetric.com/realmwar.html.json')
            obj = json.loads(response.read().decode('utf-8'))
            dfquery = obj['df']['owner']
            divider = ' '
            combine = 'Darkness Falls' + divider + dfquery
            while len(combine) < 30:
                divider = divider + ' '
                combine = 'Darkness Falls' + divider + dfquery
            result = combine
        except:
            result = 'An error occurred.'
        msg = await self.bot.say('```' + result + '```')
        defdel(msg,time.time())

    @commands.command()
    async def bg(self):
        'Returns a list of battlegrounds keeps and their current owners.'
        try:
            response = urlopen('http://uthgard.riftmetric.com/realmwar.html.json')
            obj = json.loads(response.read().decode('utf-8'))
            result = '\n'
            for keep in obj['all_keeps']:
                if keep['location'] == '':
                    if not 'captured' in keep['name']:
                        if keep['name'] == 'Dun Abermenai':
                            keepname = keep['name'] + ' (Lv 15-19)'
                        elif keep['name'] == 'Thidranki Faste':
                            keepname = keep['name'] + ' (Lv 20-24)'
                        elif keep['name'] == 'Dun Murdaigean':
                            keepname = keep['name'] + ' (Lv 25-29)'
                        else:
                            keepname = keep['name'] + ' (Lv 30-35)'
                        divider = ' '
                        combine = keepname + divider + keep['owner']
                        while len(combine) < 40:
                            divider = divider + ' '
                            combine = keepname + divider + keep['owner']
                        if keep['name'] == 'Dun Abermenai':
                            one = combine
                        elif keep['name'] == 'Thidranki Faste':
                            two = combine
                        elif keep['name'] == 'Dun Murdaigean':
                            three = combine
                        else:
                            four = combine
            result = one + '\n' + two + '\n' + three + '\n' + four
            if len(result) < 5:
                result = 'Parsing error. Contact Orito.'
        except URLError as e:
            result = 'http://uthgard.riftmetric.com/realmwar.html appears to be unreachable.'
        except Exception:
            result = 'An unknown exception occurred. Please contact Orito with the command you tried when encountering this.'
        except:
            result = 'An unknown error occurred. Please contact Orito with the command you tried when encountering this.'
        msg = await self.bot.say('```' + result + '```')
        defdel(msg,time.time())

    @commands.command()
    async def keeps(self, realm : str):
        'Returns a list of keeps by realm and their current owners.'
        try:
            response = urlopen('http://uthgard.riftmetric.com/realmwar.html.json')
            obj = json.loads(response.read().decode('utf-8'))
            if realm.upper() == 'HIBERNIA' or realm.upper() == 'HIB':
                nSEL = 2
            elif realm.upper() == 'MIDGARD' or realm.upper() == 'MID':
                nSEL = 1
            elif realm.upper() == 'ALBION' or realm.upper() == 'ALB':
                nSEL = 0
            else:
                result = 'Invalid selection. Possible choices: HIB, MID, ALB, HIBERNIA, MIDGARD, ALBION'
            rquery = obj['realm_keeps'][int(nSEL)]['keeps']
            combineit = '\n'
            for i in rquery:
                spacer = ' '
                combineone = i['name'] + spacer + i['owner']
                while len(combineone) < 30:
                    spacer = spacer + ' '
                    combineone = i['name'] + spacer + i['owner']
                combineit = combineit + combineone + '\n'
            result = combineit
        except URLError as e:
            result = 'http://uthgard.riftmetric.com/ appears to be unreachable.'
        except Exception:
            result = 'An unknown exception occurred. Please contact Orito and include the command you tried to run.'
        msg = await self.bot.say('```' + result + '```')
        defdel(msg,time.time())

    @keeps.error
    async def keeps_error(self, error, ctw):
        msg = await self.bot.say('```Proper usage: ?keeps <realm>\nExample: ?keeps hib```')
        defdel(msg,time.time())
        return


def setup(bot):
    bot.add_cog(RVR(bot))
