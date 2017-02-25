#!/usr/bin/env python3
from urllib.request import Request, urlopen
from urllib.error import URLError
import discord
from discord.ext import commands
import datetime
import json
import time
import asyncio
import delcomp
import ADMIN
import formatting

class RVR():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def df(self, ctx):
        'Returns the current realm that owns Darkness Falls.'
        await formatting.toDel(ctx.message,ctx)
        await ADMIN.addcount('?df')
        try:
            response = urlopen('http://uthgard.riftmetric.com/realmwarjson/')
            obj = json.loads(response.read().decode('utf-8'))
            dfquery = obj['df']['owner']
            divider = ' '
            combine = 'Darkness Falls' + divider + dfquery
            color = 0x00FF00
            title = ''
            name = 'Darkness Falls'
            avatar = self.bot.user.avatar_url
            while len(combine) < 30:
                divider = divider + ' '
                combine = 'Darkness Falls' + divider + dfquery
            result = combine
            msg = await self.bot.send_message(ctx.message.channel,'```\n' + result + '\n```')
            await formatting.toDel(msg,ctx)
            return
        except:
            title = 'ERROR'
            color = 0xFF0000
            avatar = 'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png'
            result = 'An unknown error occurred.\nProbably can\'t reach \'http://uthgard.riftmetric.com/\'.'
            name = self.bot.user.name
        readysend = await formatting.emMsg(title,result,color,name,avatar)
        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
        await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True)
    async def relic(self, ctx):
        'Returns a list of relics and their current owners.'
        await formatting.toDel(ctx.message,ctx)
        await ADMIN.addcount('?relic')
        try:
            response = urlopen('http://uthgard.riftmetric.com/realmwarjson/')
            obj = json.loads(response.read().decode('utf-8'))
            result = '\n'
            for relic in obj['all_keeps']:
                if relic['location'] == '':
                    if 'captured' in relic['name']:
                        if relic['name'] == 'captured the Power relic of Hibernia':
                            relicname = 'Cauldron of Dagda (Power)'
                        elif relic['name'] == 'captured the Strength relic of Hibernia':
                            relicname = 'Lug\'s Spear of Lightning (Strength)'
                        elif relic['name'] == 'captured the Power relic of Midgard':
                            relicname = 'Horn of Valhalla (Power)'
                        elif relic['name'] == 'captured the Strength relic of Midgard':
                            relicname = 'Thor\'s Hammer (Strength)'
                        elif relic['name'] == 'captured the Power relic of Albion':
                            relicname = 'Merlin\'s Staff (Power)'
                        else:
                            relicname = 'Scabbard of Excalibur (Strength)'
                        divider = ' '
                        combine = relicname + divider + relic['owner']
                        while len(combine) < 53:
                            divider = divider + ' '
                            combine = relicname + divider + relic['owner']
                        if relic['name'] == 'captured the Power relic of Hibernia':
                            two = combine
                        elif relic['name'] == 'captured the Strength relic of Hibernia':
                            one = combine
                        elif relic['name'] == 'captured the Power relic of Midgard':
                            four = combine
                        elif relic['name'] == 'captured the Strength relic of Midgard':
                            three = combine
                        elif relic['name'] == 'captured the Power relic of Albion':
                            six = combine
                        else:
                            five = combine
            result = '\nHIBERNIA\n-----------------------------------------------------\n{}\n{}\n\nMIDGARD\n-----------------------------------------------------\n{}\n{}\n\nALBION\n-----------------------------------------------------\n{}\n{}'.format(one,two,three,four,five,six)
            msg = await self.bot.send_message(ctx.message.channel,'```\n' + result + '\n```')
            await formatting.toDel(msg,ctx)
            return
        except URLError as e:
            result = 'http://uthgard.riftmetric.com/realmwar.html appears to be unreachable.'
            title = 'CONNECTIVITY ERROR'
            name = self.bot.user.name
            color = 0xFF0000
            avatar = 'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png'
        readysend = await formatting.emMsg(title,result,color,name,avatar)
        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
        await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True)
    async def bg(self, ctx):
        'Returns a list of battlegrounds keeps and their current owners.'
        await formatting.toDel(ctx.message,ctx)
        await ADMIN.addcount('?bg')
        try:
            response = urlopen('http://uthgard.riftmetric.com/realmwarjson/')
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
                avatar = 'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png'
                name = self.bot.user.name
                title = 'ERROR'
                color = 0xFF0000
            else:
                msg = await self.bot.send_message(ctx.message.channel,'```\n' + result + '\n```')
                await formatting.toDel(msg,ctx)
                return
        except URLError as e:
            avatar = 'http://pngimages.net/sites/default/files/network-offline-png-image-40320.png'
            name = self.bot.user.name
            title = 'CONNECTIVITY ERROR'
            color = 0xFF0000
            result = 'http://uthgard.riftmetric.com/ appears to be unreachable.'
        except Exception as e:
            avatar = 'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png'
            name = self.bot.user.name
            color = 0xFF0000
            title = 'UNKNOWN ERROR'
            result = 'Contact Orito with the below details.\n\n{}'.format(e)
        readysend = await formatting.emMsg(title,result,color,name,avatar)
        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
        await formatting.toDel(msg,ctx)

    @commands.command(pass_context=True)
    async def keeps(self, ctx, realm : str):
        'Returns a list of keeps by realm and their current owners.\nPossible Entries: ALL, HIB, MID, ALB, HIBERNIA, MIDGARD, ALBION'
        await formatting.toDel(ctx.message,ctx)
        await ADMIN.addcount('?keeps')
        try:
            title = ''
            color = 0x00FF00
            avatar = self.bot.user.avatar_url
            response = urlopen('http://uthgard.riftmetric.com/realmwarjson/')
            obj = json.loads(response.read().decode('utf-8'))
            if realm.upper() == 'HIBERNIA' or realm.upper() == 'HIB':
                nSEL = 2
                name = 'Hibernia Keeps'
            elif realm.upper() == 'MIDGARD' or realm.upper() == 'MID':
                nSEL = 1
                name = 'Midgard Keeps'
            elif realm.upper() == 'ALBION' or realm.upper() == 'ALB':
                nSEL = 0
                name = 'Albion Keeps'
            elif realm.upper() == 'ALL':
                name = 'All Keeps'
                rquery = obj['realm_keeps'][int(2)]['keeps']
                combineit = '\nHIBERNIA\n------------------------------\n'
                for i in rquery:
                    spacer = ' '
                    combineone = i['name'] + spacer + i['owner']
                    while len(combineone) < 30:
                        spacer = spacer + ' '
                        combineone = i['name'] + spacer + i['owner']
                    combineit = combineit + combineone + '\n'
                combineit = combineit + '\nMIDGARD\n------------------------------\n'
                rquery = obj['realm_keeps'][int(1)]['keeps']
                for i in rquery:
                    spacer = ' '
                    combineone = i['name'] + spacer + i['owner']
                    while len(combineone) < 30:
                        spacer = spacer + ' '
                        combineone = i['name'] + spacer + i['owner']
                    combineit = combineit + combineone + '\n'
                combineit = combineit + '\nALBION\n------------------------------\n'
                rquery = obj['realm_keeps'][int(0)]['keeps']
                for i in rquery:
                    spacer = ' '
                    combineone = i['name'] + spacer + i['owner']
                    while len(combineone) < 30:
                        spacer = spacer + ' '
                        combineone = i['name'] + spacer + i['owner']
                    combineit = combineit + combineone + '\n'
                result = combineit
                msg = await self.bot.send_message(ctx.message.channel,'```\n' + result + '\n```')
                await formatting.toDel(msg,ctx)
                return
            else:
                readysend = await formatting.emMsg('INVALID SELECTION','Possible choice are: ALL, HIB, MID, ALB, HIBERNIA, MIDGARD, ALBION',0xFF0000,self.bot.user.name,'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png')
                msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
                await formatting.toDel(msg,ctx)
                return
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
            msg = await self.bot.send_message(ctx.message.channel,'```\n' + result + '\n```')
            await formatting.toDel(msg,ctx)
            return
        except URLError as e:
            name = self.bot.user.name
            avatar = 'http://pngimages.net/sites/default/files/network-offline-png-image-40320.png'
            title = 'CONNECTIVITY ERROR'
            color = 0xFF0000
            result = 'http://uthgard.riftmetric.com/ appears to be unreachable.'
        except Exception as e:
            title = 'UNKNOWN ERROR'
            color = 0xFF0000
            name = self.bot.user.name
            avatar = 'https://www.helpnetsecurity.com/wp-content/uploads/2015/12/error.png'
            result = 'An unknown exception occurred. Please contact Orito and include the command you tried to run.'
        readysend = await formatting.emMsg(title,result,color,name,avatar)
        msg = await self.bot.send_message(ctx.message.channel, embed=readysend)
        await formatting.toDel(msg,ctx)

#    @keeps.error
#    async def keeps_error(self, error, ctw):
#        msg = await self.bot.say('```Proper usage: ?keeps <realm>\nExample: ?keeps hib```')
#        return


def setup(bot):
    bot.add_cog(RVR(bot))
