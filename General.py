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
import delcomp
import formatting
import ADMIN

global charList
charList = []

with open('character_list.log','a+') as charOpen:
    charOpen.seek(0)
    charList = charOpen.read().splitlines()
    #print(charList)

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

async def addperlist(usernameid,chara):
    global charList
    with open('character_list.log','a+') as charOpen:
        charOpen.write('{}#{}\n'.format(usernameid,chara.title()))
        charOpen.seek(0)
        charList = charOpen.read().splitlines()
    return

async def remperlist(usernameid,chara):
    global charList
    with open('character_list.log','w+') as charOpen:
        for line in charList:
            if not line == '{}#{}'.format(usernameid,chara.title()):
                charOpen.write('{}\n'.format(line))
                charOpen.seek(0)
                charList = charOpen.read().splitlines()
    return

async def heraldedList(trigger):
    b = []
    if trigger == 'Race':
        b = ['N/A',4,6,12,14,16,18,20,22]
    else:
        b = [3,5,7,13,15,17,19,21,23]
    return b

class General():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def who(self, ctx, *, query : str):
        'Performs a character search similar to in-game.'
        await formatting.toDel(ctx.message,ctx)
        await ADMIN.addcount('?who')
        global heraldlist
        if len(query) < 3:
            readysend = await formatting.emMsg('TOO FEW CHARACTERS','You did not enter the minimum number of characters (3) to perform a search.',0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
            msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
            await formatting.toDel(msg,ctx)
            return
        global searchlist
        searchlist = []
        query = query.replace(' ','%20')
        url = 'https://www2.uthgard.net/herald/api/search/player/'
        query = query.title()
        try:
            uthquery = await webquery(url,query)
            await parsesearch(uthquery)
        except Exception as e:
            if '[Errno -2] Cannot connect to host uthgard.org:443 ssl:True [Name or service not known]' == str(e):
                readysend = await formatting.emMsg('DNS ERROR','{} cannot currently communicate with https://www2.uthgard.net/.\nPlease try again later, if issue persists send the following information to Orito.\n\nException: {}'.format(self.bot.user.name,e),0xFF0000,self.bot.user.name,'http://pngimages.net/sites/default/files/network-offline-png-image-40320.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
            else:
                readysend = await formatting.emMsg('FATAL ERROR','A fatal error ocurred.\nPlease send the following to Orito:\n\n{}'.format(e),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
            return
        if searchlist == [] or searchlist == ['Not Found']:
            try:
                uthquery = await webquery(url,'Orito')
                await parsesearch(uthquery)
                if searchlist == []:
                    readysend = await formatting.emMsg('API ERROR','The Uthgard API is currently returning no results.\nPlease try again later. If the issue persists, contact Orito.',0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                    return
            except Exception as e:
                if '[Errno -2] Cannot connect to host uthgard.org:443 ssl:True [Name or service not known]' == str(e):
                    readysend = await formatting.emMsg('DNS ERROR','{} cannot currently communicate with https://www2.uthgard.net/.\nPlease try again later, if issue persists send the following information to Orito.\n\nException: {}'.format(self.bot.user.name,e),0xFF0000,self.bot.user.name,'http://pngimages.net/sites/default/files/network-offline-png-image-40320.png')
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                else:
                    readysend = await formatting.emMsg('FATAL ERROR','A fatal error ocurred.\nPlease send the following to Orito:\n\n{}'.format(e),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                return
            query = query.replace('%20',' ')
            readysend = await formatting.emMsg('','\'{}\' returned no results.'.format(query),0xFF0000,'?who {}'.format(query),ctx.message.author.avatar_url)
            msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
            await formatting.toDel(msg,ctx)
            return
        complist = ''
        try:
            list_of_players, _ = await asyncio.wait([webquery('https://www2.uthgard.net/herald/api/player/',a) for a in searchlist])
        except error as e:
            await self.bot.say('{}.{}'.format(error,e))
        if query in searchlist:
            for i, heraldquery in zip(searchlist, list_of_players):
                heraldquery = await heraldquery
                heraldlist = []
                await split_line(str(heraldquery))
                nNM = 1 #Name
                convherald = await heraldedList(heraldlist[3])
                nGD = convherald[0]  #Guild
                nRC = convherald[1]  #Race
                nCL = convherald[2]  #Class
                nRP = convherald[3]  #RPs
                nLV = convherald[4]  #Level
                nRR = convherald[5]  #Realm Rank
                nXP = convherald[6]  #XP % of Level
                nRXP = convherald[7] #Realm XP % of Level
                nUP = convherald[8]  #Last Updated
                rrMax = heraldlist[nRR][:-1]
                rrMin = heraldlist[nRR][len(heraldlist[nRR])-1:]
                if heraldlist[nNM] == query:
                    if nGD == 'N/A':
                        complist = 'Exact Match: {} the level {} {} {} RR {}L{}, {} RPs\n\n{}'.format(heraldlist[nNM],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin,heraldlist[nRP],complist)
                    else:
                        complist = 'Exact Match: {} <{}> the level {} {} {} RR {}L{}, {} RPs\n\n{}'.format(heraldlist[nNM],heraldlist[nGD],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin,heraldlist[nRP],complist)
        print(searchlist)
        print('--------')
        print(list_of_players)
        #return
        for i, heraldquery in zip(searchlist, list_of_players):
            #charMatch = sorted(charMatch)
            heraldquery = await heraldquery
            heraldlist = []
            await split_line(str(heraldquery))
            nNM = 1 #Name
            convherald = await heraldedList(heraldlist[3])
            nGD = convherald[0]  #Guild
            nRC = convherald[1]  #Race
            nCL = convherald[2]  #Class
            nRP = convherald[3]  #RPs
            nLV = convherald[4]  #Level
            nRR = convherald[5]  #Realm Rank
            nXP = convherald[6]  #XP % of Level
            nRXP = convherald[7] #Realm XP % of Level
            nUP = convherald[8]  #Last Updated
            rrMax = heraldlist[nRR][:-1]
            rrMin = heraldlist[nRR][len(heraldlist[nRR])-1:]
            if not heraldlist[nNM] == query:
                if nGD == 'N/A':
                    complist = '{}{} the level {} {} {} RR {}L{}, {} RPs\n'.format(complist,heraldlist[nNM],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin,heraldlist[nRP])
                else:
                    complist = '{}{} <{}> the level {} {} {} RR {}L{}, {} RPs\n'.format(complist,heraldlist[nNM],heraldlist[nGD],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin,heraldlist[nRP])
                if len(complist) > 1600:
                    readysend = await formatting.emMsg('','{}'.format(complist),0xFFFFFF,'?who {}'.format(query),self.bot.user.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                    complist = ''
        if len(complist) > 7:
            readysend = await formatting.emMsg('','{}'.format(complist),0xFFFFFF,'?who {}'.format(query),self.bot.user.avatar_url)
            msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
            await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True)
    async def me(self,ctx,opt='show',*,char='0'):
        '''Tracking for your own characters.
            '?me' - (ex. ?me) Shows your saved characters, if any.
            '?me add <charName>(, <charName>)' - (ex. ?me add Orito; ?me add Orito,Oricul) Adds character(s) to your saved list.
            '?me [rem|remove] <charName>' - (ex. ?me rem Orito; ?me rem Orito,Oricul; ?me remove Orito; ?me remove Orito,Oricul) Removes character(s) from your saved list.
            '?me list <@another_user>' - (ex. ?me list @Orito#2679) Lists another user's characters. NOTE: You must tag them. This is due to how the lists are stored, and the unique identifier to each user.'''
        global charList
        await formatting.toDel(ctx.message,ctx)
        await ADMIN.addcount('?me')
        global searchlist
        global heraldlist
        searchlist = []
        try:
            uthquery = await webquery('https://www2.uthgard.net/herald/api/player/','Orito')
            await parsesearch(uthquery)
            if searchlist == ['Not Found'] or searchlist == []:
                readysend = await formatting.emMsg('API ERROR','The Uthgard API is currently returning no results.\nPlease try again later. If the issue persists, contact Orito.',0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
                return
        except Exception as e:
            if '[Errno -2] Cannot connect to host uthgard.org:443 ssl:True [Name or service not known]' == str(e):
                readysend = await formatting.emMsg('DNS ERROR','{} cannot currently communicate with https://www2.uthgard.net/.\nPlease try again later, if issue persists send the following information to Orito.\n\nException: {}'.format(self.bot.user.name,e),0xFF0000,self.bot.user.name,'http://pngimages.net/sites/default/files/network-offline-png-image-40320.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
            else:
                readysend = await formatting.emMsg('FATAL ERROR','A fatal error ocurred.\nPlease send the following to Orito:\n\n{}'.format(e),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
            return
        try:
            if opt == 'show':
                if any(ctx.message.author.id in s for s in charList):
                    charMatch = [i for i in charList if ctx.message.author.id in i]
                    charMatch = sorted(charMatch)
                    compiled = ''
                    for i in charMatch:
                        charMatched = i.split('#',1)[-1]
                        try:
                            heraldquery = await webquery('https://www2.uthgard.net/herald/api/player/',charMatched.title())
                            if len(heraldquery) < 20:
                                compiled = '{}Character \'{}\' doesn\'t exist and has been removed from your saved list.\n'.format(compiled,charMatched.title())
                                with open('character_list.log','w+') as charOpen:
                                    for line in charList:
                                        if not line == '{}#{}'.format(ctx.message.author.id,charMatched.title()):
                                            charOpen.write('{}\n'.format(line))
                                    charOpen.seek(0)
                                    charList = charOpen.read().splitlines()
                                continue
                            heraldlist = []
                            await split_line(heraldquery)
                            nNM = 1 #Name
                            convherald = await heraldedList(heraldlist[3])
                            nGD = convherald[0]  #Guild
                            nRC = convherald[1]  #Race
                            nCL = convherald[2]  #Class
                            nRP = convherald[3]  #RPs
                            nLV = convherald[4]  #Level
                            nRR = convherald[5]  #Realm Rank
                            nXP = convherald[6]  #XP % of Level
                            nRXP = convherald[7] #Realm XP % of Level
                            nUP = convherald[8]  #Last Updated
                            rrMax = heraldlist[nRR][:-1]
                            rrMin = heraldlist[nRR][len(heraldlist[nRR])-1:]
                            if nGD == 'N/A':
                                compiled = '{}{} the level {} {} {} RR {}L{}, {} RPs\n'.format(compiled,heraldlist[nNM],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin,heraldlist[nRP])
                            else:
                                compiled = '{}{} <{}> the level {} {} {} RR {}L{}, {} RPs\n'.format(compiled,heraldlist[nNM],heraldlist[nGD],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin,heraldlist[nRP])
                            if len(compiled) > 1600:
                                readysend = await formatting.emMsg('','{}'.format(compiled),0xFFFFFF,ctx.message.author.name + '\'s saved character(s):',ctx.message.author.avatar_url)
                                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                                await formatting.toDel(msg,ctx)
                                compiled = ''
                        except Exception as e:
                            if '[Errno -2]' in e:
                                readysend = await formatting.emMsg('DNS ERROR','{} cannot currently communicate with https://www2.uthgard.net/.\nPlease try again later, if issue persists send the following information to Orito.\n\nException: {}'.format(self.bot.user.name,e),0xFF0000,self.bot.user.name,'http://pngimages.net/sites/default/files/network-offline-png-image-40320.png')
                                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                                await formatting.toDel(msg,ctx)
                            else:
                                await delcomp.defdel(msg,time.time(),ctx.message.server.id + '#' + ctx.message.channel.name)
                                readysend = await formatting.emMsg('FATAL ERROR','An unknown error ocurred.\nPlease contact Orito with the following information:\n\n{}'.format(e),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                                
                            return
                    readysend = await formatting.emMsg('','{}'.format(compiled),0xFFFFFF,ctx.message.author.name + '\'s saved character(s):',ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                else:
                    readysend = await formatting.emMsg('','To start, try some of the following commands:\n\n?me add <charName> - (ex. ?me add Orito) Adds a single character to your saved list.\n?me add <charName>(,<charName>) - (ex. ?me add Orito,Oricul) Adds multiple characters to your saved list.',0xFF0000,ctx.message.author.name + ' does not have any characters setup!',ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                return
            elif opt == 'add' and char != '0':
                if ',' in char:
                    charSanitize = char.split(',')
                    charSanitize = [i.replace(' ', '') for i in charSanitize]
                    charSanitize = list(set(charSanitize))
                    compmsg = ''
                    compfail = ''
                    compalr = ''
                    for i in charSanitize:
                        i = re.sub(r'\W+','',i)
                        doesexist = await webquery('https://www2.uthgard.net/herald/api/search/player/',i)
                        if len(doesexist) > 3:
                            if not '{}#{}'.format(ctx.message.author.id,i.title()) in charList:
                                await addperlist(ctx.message.author.id,i.title())
                                compmsg = '{}{}\n'.format(compmsg,i.title())
                            else:
                                compalr = '{}{}\n'.format(compalr,i.title())
                        else:
                            compfail = '{}{}\n'.format(compfail,i.title())
                    if len(compmsg) > 2:
                        readysend = await formatting.emMsg('','{}'.format(compmsg),0x00FF00,ctx.message.author.name + ' added characters:',ctx.message.author.avatar_url)
                        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                        await formatting.toDel(msg,ctx)
                    if len(compfail) > 2:
                        readysend = await formatting.emMsg('','{}'.format(compfail),0xFF0000,ctx.message.author.name + ' tried adding character(s) that don\'t exist:',ctx.message.author.avatar_url)
                        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                        await formatting.toDel(msg,ctx)
                    if len(compalr) > 2:
                        readysend = await formatting.emMsg('','{}'.format(compalr),0xFF0000,ctx.message.author.name + ' tried adding a character already in their list:',ctx.message.author.avatar_url)
                        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                        await formatting.toDel(msg,ctx)
                elif not '{}#{}'.format(ctx.message.author.id,char.title()) in charList:
                    char = re.sub(r'\W+','',char)
                    await addperlist(ctx.message.author.id,char.title())
                    readysend = await formatting.emMsg('','{}'.format(char.title()),0x00FF00,ctx.message.author.name + ' added character:',ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                else:
                    readysend = await formatting.emMsg('','{}'.format(char.title()),0xFF0000,ctx.message.author.name + ' already has character assigned:',ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                return
            elif (opt == 'rem' or opt == 'remove') and char != '0' and ',' in char:
                charSanitize = char.split(',')
                charSanitize = [i.replace(' ', "") for i in charSanitize]
                print(charSanitize)
                compmsg = ''
                compfail = ''
                for i in charSanitize:
                    i = re.sub(r'\W+','',i)
                    if '{}#{}'.format(ctx.message.author.id,i.title()) in charList:
                        await remperlist(ctx.message.author.id,i.title())
                        compmsg = '{}{}\n'.format(compmsg,i.title())
                    else:
                        compfail = '{}{}\n'.format(compfail,i.title(),ctx.message.author.name)
                if len(compmsg) > 2:
                    readysend = await formatting.emMsg('','{}'.format(compmsg),0x00FF00,ctx.message.author.name + ' removed characters:',ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                if len(compfail) > 2:
                    readysend = await formatting.emMsg('','{}'.format(compfail),0xFF0000,ctx.message.author.name + ' is not assigned character(s):',ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
            elif (opt == 'rem' or opt == 'remove') and char != '0':
                char = re.sub(r'\W+','',char)
                if '{}#{}'.format(ctx.message.author.id,char.title()) in charList:
                    await remperlist(ctx.message.author.id,char.title())
                    readysend = await formatting.emMsg('','{}'.format(char.title()),0x00FF00,ctx.message.author.name + ' removed character:',ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                else:
                    readysend = await formatting.emMsg('','{}'.format(char.title()),0xFF0000,ctx.message.author.name + ' is not assigned character:',ctx.message.author.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                return
            elif opt == 'list' and char != '0':
                charSanitize = char.replace('@', '').replace('<', '').replace('>', '').replace('!', '')
                them = await self.bot.get_user_info(charSanitize)
                if any(charSanitize in s for s in charList):
                    charMatch = [i for i in charList if charSanitize in i]
                    charMatch = sorted(charMatch)
                    them
                    compiled = ''
                    for i in charMatch:
                        charMatched = i.split('#',1)[-1]
                        try:
                            heraldquery = await webquery('https://www2.uthgard.net/herald/api/player/',charMatched.title())
                            if len(heraldquery) < 20:
                                compiled = '{}Character \'{}\' doesn\'t exist. Not removing from other user\'s list.\n'.format(compiled,charMatched.title())
                                continue
                            heraldlist = []
                            await split_line(heraldquery)
                            nNM = 1 #Name
                            convherald = await heraldedList(heraldlist[3])
                            nGD = convherald[0]  #Guild
                            nRC = convherald[1]  #Race
                            nCL = convherald[2]  #Class
                            nRP = convherald[3]  #RPs
                            nLV = convherald[4]  #Level
                            nRR = convherald[5]  #Realm Rank
                            nXP = convherald[6]  #XP % of Level
                            nRXP = convherald[7] #Realm XP % of Level
                            nUP = convherald[8]  #Last Updated
                            rrMax = heraldlist[nRR][:-1]
                            rrMin = heraldlist[nRR][len(heraldlist[nRR])-1:]
                            if nGD == 'N/A':
                                compiled = '{}{} the level {} {} {} RR {}L{}, {} RPs\n'.format(compiled,heraldlist[nNM],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin,heraldlist[nRP])
                            else:
                                compiled = '{}{} <{}> the level {} {} {} RR {}L{}, {} RPs\n'.format(compiled,heraldlist[nNM],heraldlist[nGD],heraldlist[nLV],heraldlist[nRC],heraldlist[nCL],rrMax,rrMin,heraldlist[nRP])
                            if len(compiled) > 1600:
                                readysend = await formatting.emMsg('','{}'.format(compiled),0xFFFFFF,them.name + '\'s saved character(s):',them.avatar_url)
                                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                                await formatting.toDel(msg,ctx)
                                compiled = ''
                        except Exception as e:
                            if '[Errno -2]' in e:
                                readysend = await formatting.emMsg('DNS ERROR','{} cannot currently communicate with https://www2.uthgard.net/.\nPlease try again later, if issue persists send the following information to Orito.\n\nException: {}'.format(self.bot.user.name,e),0xFF0000,self.bot.user.name,'http://pngimages.net/sites/default/files/network-offline-png-image-40320.png')
                                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                                await formatting.toDel(msg,ctx)
                            else:
                                readysend = await formatting.emMsg('FATAL ERROR','An unknown error ocurred.\nPlease contact Orito with the following information:\n\n{}'.format(e),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                                await formatting.toDel(msg,ctx)
                            return
                    readysend = await formatting.emMsg('','{}'.format(compiled),0xFFFFFF,them.name + '\'s saved character(s):',them.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                else:
                    readysend = await formatting.emMsg('','Help them get started! Introduce them to \'?me\'!',0xFF0000,them.name + ' does not have any characters setup!',them.avatar_url)
                    msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                    await formatting.toDel(msg,ctx)
                return
            else:
                readysend = await formatting.emMsg('COMMAND ERROR','Invalid option in command: {}\n\nPossible entries:\n?me\n?me add <charName>(,<charName>)\n?me [rem|remove] <charName>(,<charName>)\n?me list <@another_user>'.format(opt),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
                return
        except Exception as e:
            if '[Errno -2] Cannot connect to host uthgard.org:443 ssl:True [Name or service not known]' == str(e):
                readysend = await formatting.emMsg('DNS ERROR','{} cannot currently communicate with https://www2.uthgard.net/.\nPlease try again later, if issue persists send the following information to Orito.\n\nException: {}'.format(self.bot.user.name,e),0xFF0000,self.bot.user.name,'http://pngimages.net/sites/default/files/network-offline-png-image-40320.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
            else:
                readysend = await formatting.emMsg('FATAL ERROR','A fatal error ocurred.\nPlease send the following to Orito:\n\n{}'.format(e),0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
            return

#    @who.error
#    async def who_error(self, error, ctw):
#        readysend = await formatting.emMsg('','Proper usage: ?who <charName>\nExample: ?who Orito',0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
#        msg = await self.bot.say(embed=readysend)
#        return


def setup(bot):
    bot.add_cog(General(bot))

