#!/usr/bin/env python3
from urllib.request import Request, urlopen
from urllib.error import URLError
import discord
from discord.ext import commands
import datetime
import json
import asyncio
from aiohttp import ClientSession
import aiohttp
from aiohttp import web
import re
import time

global log
global tlog
log = []
tlog = []

def defdel(meslog,timlog):
    log.append(meslog)
    tlog.append(timlog)

async def split_line(text):
    words = re.split(': |,|\n|\\t| "|" ',text)
    for word in words:
        word = word.translate(str.maketrans('','','"{},'))
        if word:
            if re.match(r'\S', word):
                heraldlist.append(word)
                #print (word)

async def parsesearch(text):
    words = re.split(',|\n|\\t|  "',text)
    for word in words:
        word = word.translate(str.maketrans('','','"[],'))
        if word:
            if re.match(r'\S', word):
#                print(word)
                searchlist.append(word)

async def webquery(url,add):
    async with ClientSession() as session:
        async with session.get('{}{}'.format(url,add)) as resp:
            theout2 = await resp.text()
#            print(theout2)
            return theout2

class General():
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
    async def who(self, charName : str):
        'Returns character information.'
        if charName == '':
            result = 'Proper usage: ?who <charName>'
        try:
            heraldquery = await webquery('https://uthgard.org/herald/api/player/',charName.title())
            if len(heraldquery) < 20:
                msg = await self.bot.say('```Character \'{}\' doesn\'t exist.```'.format(charName))
                defdel(msg,time.time())
                return
            global heraldlist
            heraldlist = []
            await split_line(heraldquery)
            nNM = 1 #Name
            if heraldlist[3] == 'Race':
                nGD = 'N/A'
                nRC = 4 #Race
                nCL = 6 #Class
                nRP = 12 #RPs
                nLV = 14 #Level
                nRR = 16 #Realm Rank
                nXP = 18 #XP % of Level
                nRXP = 20 #Realm XP % of Level
                nUP = 22 #Last Updated
            else:
                nGD = 3 #Guild
                nRC = 5 #Race
                nCL = 7 #Class
                nRP = 13 #RPs
                nLV = 15 #Level
                nRR = 17 #Realm Rank
                nXP = 19 #XP % of Level
                nRXP = 21 #Realm XP % of Level
                nUP = 23 #Last Updated
            rrMax = heraldlist[nRR][:-1]
            rrMin = heraldlist[nRR][len(heraldlist[nRR])-1:]
            if nGD == 'N/A':
                result = '\n' + heraldlist[nNM] + '\nLv ' + heraldlist[nLV] + ' ' + heraldlist[nRC] + ' ' + heraldlist[nCL] + '\nRR ' + str(rrMax) + 'L' + str(rrMin) + ' - ' + heraldlist[nRP] + ' RPs\nUpdated: ' + str(datetime.datetime.fromtimestamp(float(heraldlist[nUP])).strftime('%c')) + ' UTC'
            else:
                result = '\n' + heraldlist[nNM] + ' <' + heraldlist[nGD] + '>\nLv ' + heraldlist[nLV] + ' ' + heraldlist[nRC] + ' ' + heraldlist[nCL] + '\nRR ' + str(rrMax) + 'L' + str(rrMin) + ' - ' + heraldlist[nRP] + ' RPs\nUpdated: ' + str(datetime.datetime.fromtimestamp(float(heraldlist[nUP])).strftime('%c')) + ' UTC'
        except Exception:
            result = 'An unknown exception occurred. Please contact Orito and include the command you were trying to run.'
        except:
            result = 'An unknown issue occurred. Please contact Orito and include the command you were trying to run.'
        msg = await self.bot.say('```' + result + '```')
        defdel(msg,time.time())

    @who.error
    async def who_error(self, error, ctw):
        msg = await self.bot.say('```Proper usage: ?who <charName>\nExample: ?who Orito```')
        defdel(msg,time.time())
        return

    @commands.command()
    async def search(self, type : str, *, query : str):
        'Performs a character or guild search.'
        if len(query) < 3:
            msg = await self.bot.say('```You entered too few characters. You must enter a minimum of 3 characters in order to perform a search.```')
            defdel(msg,time.time())
            return
        global searchlist
        searchlist = []
        query = query.replace(' ','%20')
        if type.lower() == 'character' or type.lower() == 'char':
            url = 'https://uthgard.org/herald/api/search/player/'
            query = query.title()
        elif type.lower() == 'guild':
            url = 'https://uthgard.org/herald/api/search/guild/'
        else:
            msg = await self.bot.say('```Invalid search type, \'{}\'. Valid entries: \'character\', \'char\', \'guild\'.```'.format(type))
            defdel(msg,time.time())
            return
        try:
            uthquery = await webquery(url,query)
            await parsesearch(uthquery)
        except (RuntimeError, TypeError, NameError):
            msg = await self.bot.say('```Error.\n{} : {} : {}```'.format(RuntimeError,TypeError,NameError))
            defdel(msg,time.time())
            return
        if searchlist == []:
            query = query.replace('%20',' ')
            msg = await self.bot.say('```Your search for \'{}\' returned no results.```'.format(query))
            defdel(msg,time.time())
            return
        complist = ''
        if not type.lower() == 'guild':
            list_of_players, _ = await asyncio.wait([webquery('https://uthgard.org/herald/api/player/',a) for a in searchlist])
            for i, heraldquery in zip(searchlist, list_of_players):
                heraldquery = await heraldquery
                global heraldlist
                heraldlist = []
                await split_line(str(heraldquery))
                if heraldlist[3] == 'Race':
                    nGD = 'N/A' #Guild
                    nRC = 4 #Race
                    nCL = 6 #Class
                    nLV = 14 #Level
                    nRR = 16 #Realm Rank
                else:
                    nGD = 3 #Guild
                    nRC = 5 #Race
                    nCL = 7 #Class
                    nLV = 15 #Level
                    nRR = 17 #Realm Rank
                rrMax = heraldlist[nRR][:-1]
                rrMin = heraldlist[nRR][len(heraldlist[nRR])-1:]
                div = ' '
                comptest = '{}{}'.format(i,div)
                while len(comptest) < 26:
                    div = '{} '.format(div)
                    comptest = '{}{}'.format(i,div)
                if nGD == 'N/A':
                    complist = '{}{}Lv {} {} {} RR {}L{}\n'.format(complist,comptest,heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin)
                else:
                    complist = '{}{}<{}> Lv {} {} {} RR {}L{}\n'.format(complist,comptest,heraldlist[nGD],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin)
                if len(complist) > 1600:
                    msg = await self.bot.say('```{}```'.format(complist))
                    defdel(msg,time.time())
                    complist = ''
        else:
            for i in searchlist:
                complist = '{}<{}>\n'.format(complist,i)
                if len(complist) > 1600:
                    msg = await self.bot.say('```{}```'.format(complist))
                    defdel(msg,time.time())
                    complist = ''
        msg = await self.bot.say('```{}```'.format(complist))
        defdel(msg,time.time())

    @search.error
    async def search_error(self, error, ctw):
        msg = await self.bot.say('```Proper usage: ?search [char,character,guild] <query>\nExample: ?search char Ori```')
        defdel(msg,time.time())
        return

def setup(bot):
    bot.add_cog(General(bot))

