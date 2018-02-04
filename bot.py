import discord
import os
import io
import traceback
import sys
import time
import datetime
import asyncio
import random
import aiohttp
import pip
import random
import textwrap
from contextlib import redirect_stdout
from discord.ext import commands
import json
bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'),description="Specialized bot made for HWCWL.\n\nHelp Commands",owner_id=277981712989028353)



def cleanup_code(content):
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')
    
  
@bot.event
async def on_ready():
    print('Bot is online, and ready to ROLL!')
    await bot.change_presence(game=discord.Game(name="with HWCWL! | ?help"))



@bot.command()
async def ping(ctx):
    """Premium ping pong giving you a websocket latency."""
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='PoIIIng! Your supersonic latency is:')
    em.description = f"{bot.latency * 1000:.4f} ms"
    await ctx.send(embed=em)


@bot.command()
async def invite(ctx):
    """Allow my bot to join the hood. YOUR hood."""
    await ctx.send("Aye, invite me! https://discordapp.com/oauth2/authorize?client_id=409708279980228608&scope=bot&permissions=2146958591")


@bot.command(hidden=True, name='eval')
async def _eval(ctx, *, body: str):

    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')  


@bot.command()
async def clanlist(ctx):
	color = discord.Color(value=0x00ff00)
	em = discord.Embed(color=color, title='Clan List')
	em.description = 'This is a list of clans currently registered in HWCWL. \nOne field is ONE team, and underneath it are the clans that are part of it.'
	em.add_field(name='Savage Core', value='SHIELD (#CUQGLURJ) \nGhost Rider (#QYOCQ9RU) \nHindustan (#8L9QYQCR) \nMAHABHARAT (#P2GUJCQY)')
	em.add_field(name="Ice Avengers", value='expnedabls (#PY0UYQP) \nIndia (#89Q8UQ88)')
	em.set_thumbnail(url='https://media.discordapp.net/attachments/409395139019276288/409706582364913677/HWCWL_LOGO_MAIN.png?width=676&height=676')
	await ctx.send(embed=em)


if not os.environ.get('TOKEN'):
    print("no token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('"'))    