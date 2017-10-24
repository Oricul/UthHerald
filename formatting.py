#!/usr/bin/env python3
import discord
from discord.ext import commands
import datetime
import time
import delcomp

async def emMsg(mTitle,mDesc,mColor,mName,mIcon):
    readysend = discord.Embed(title='{}'.format(mTitle),description='{}'.format(mDesc),color=mColor)
    readysend.set_author(name=mName,icon_url=mIcon)
    return readysend

async def toDel(msg,ctx):
    await delcomp.defdel(msg,time.time(),ctx.message.server.id + '#' + ctx.message.channel.name)
    return
