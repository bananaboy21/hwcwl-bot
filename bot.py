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
bot.remove_command("help")


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
async def help(ctx, command=None):
	if command is None:
		color = discord.Color(value=0x00ff00)
		em = discord.Embed(color=color, title='HWCWL Bot')
		em.description = 'Thank you for using the HWCWL Discord bot. Here are a list of commands to use for me.'
		em.add_field(name="ping", value="Gets the bot's websocket latency.")
		em.add_field(name="clanlist", value="Gets the list of clans added to this bot.")
		em.add_field(name="claninfo [clan name]", value="Gets information of a clan by its clan name.")
		em.set_thumbnail(url='https://media.discordapp.net/attachments/409395139019276288/409706582364913677/HWCWL_LOGO_MAIN.png?width=676&height=676')
		await ctx.send(embed=em)
	else:
		if command.lower() == 'ping':
			color = discord.Color(value=0x00ff00)
			em = discord.Embed(color=color, title='ping')
			em.description = 'Gets the websocket latency for the bot.\nA latency higher than 100 ms usually means a slower response.'
			await ctx.send(embed=em)
		if command.lower() == 'clanlist':
			color = discord.Color(value=0x00ff00)
			em = discord.Embed(color=color, title='clanlist')
			em.description = 'Gets a list of clans that are added to the bot.\nYou may type `?claninfo [clan name]`, by replacing [clan name] with the name of a clan on this list.\n\nIf your clan is not yet on the list, notify dat banana boi #1982 or TiTAN|HWCWL|CNA #8672 to update it.'
			await ctx.send(embed=em)
		if command.lower() == 'claninfo':
			color = discord.Color(value=0x00ff00)
			em = discord.Embed(color=color, title='claninfo [clan name]')
			em.description = 'Gets clan info for a given clan name.\nType `?claninfo [clan name]` and replace [clan name] with a name of a clan.\nAll the clans supported by this command are listed in the command `?clanlist`.\nPlease make sure you type the name correctly.'
			await ctx.send(embed=em)
		else:
			await ctx.send('Command not found. To view all commands, type `?help`.')




@bot.command()
async def ping(ctx):
    """Premium ping pong giving you a websocket latency."""
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='PoIIIng! Your supersonic latency is:')
    em.description = f"{bot.latency * 1000:.4f} ms"
    await ctx.send(embed=em)



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
	em.add_field(name='Savage Core', value='SHIELD (#CUQGLURJ) \nGhost Rider (#QYOCQ9RU) \nHindustan (#8L9QYQCR) \nMAHABHARAT (#P2GUJCQY) \nZampui clashers (#2PYP9CRP)')
	em.add_field(name="Ice Avengers", value='expnedabls (#PY0UYQP) \nIndia (#89Q8UQ88)')
	em.set_thumbnail(url='https://media.discordapp.net/attachments/409395139019276288/409706582364913677/HWCWL_LOGO_MAIN.png?width=676&height=676')
	await ctx.send(embed=em)


@bot.command()
async def claninfo(ctx, clan=None):
	if clan is None:
		await ctx.send("Oops! Be sure to enter a clan's name to look up info for it.")
	else:
		if clan.lower() == 'shield':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%23CUQGLURJ', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'ghost rider':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%23QYOCQ9RU', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'hindustan':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%238L9QYQCR', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'mahabharat':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%23P2GUJCQY', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'expnedabls':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%23PY0UYQP', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'india':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%2389Q8UQ88', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'zampui clashers':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%232PYP9CRP', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		else:
			await ctx.send("Clan not found. Use `?clanlist` to see a list of clans currently added to the bot.")



@bot.command()
async def warinfo(ctx, *, clan=None):
	if clan is None:
		await ctx.send("Oops! Please enter a clan name to access the war info for it.")
	else:
		if clan.lower() == 'shield':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%23CUQGLURJ/currentwar', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='War Info')
					if clan['state'] == 'inWar':
						warstate = 'In War'
					else:
						warstate = 'Not In War'
					em.add_field(name='Status', value=warstate)
					em.add_field(name='War Size', value=f'{clan['teamSize']} vs {clan['teamSize']}')
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan['name']}({clan['tag']}) vs {opponent['name']} ({opponent['tag']})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'ghost rider':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%23QYOCQ9RU', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'hindustan':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%238L9QYQCR', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'mahabharat':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%23P2GUJCQY', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'expnedabls':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%23PY0UYQP', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		if clan.lower() == 'india':
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.clashofclans.com/v1/clans/%2389Q8UQ88', headers=client) as respclan:
					clan = await respclan.json()
					color = discord.Color(value=0xe5f442)
					em = discord.Embed(color=color, title='Clan Info')
					em.add_field(name='Location', value=clan.get('location', {}).get('name'))
					em.add_field(name='Clan Level', value=clan.get('clanLevel', 0))
					em.add_field(name='Clan Points - Home Base', value=clan.get('clanPoints', 0))
					em.add_field(name='Clan Points - Builder Base', value=clan.get('clanVersusPoints', 0))
					em.add_field(name='Members', value=f'{clan.get('members')}/50')
					em.add_field(name='Required Trophies', value=clan.get('requiredTrophies', 0))
					em.add_field(name='War Frequency', value=clan.get('warFrequency', 0))
					em.add_field(name='War Win Streak', value=clan.get('warWinStreak', 0))
					em.add_field(name='War Wins', value=clan.get('warWins', 0))
					em.add_field(name='War Draws', value=clan.get('warTies', 0))
					em.add_field(name='War Losses', value=clan.get('warLosses', 0))
					if clan['isWarLogPublic'] is True:
						warlog = 'Public'
					else:
						warlog = 'Private'
					em.add_field(name='War Log', value=warlog)
					em.set_author(name=f"{clan.get('name', '[Unknown Name]')} ({clan.get('tag', '[Unknown Tag]')})")
					em.set_thumbnail(url=clan['badgeUrls']['medium'])
					await ctx.send(embed=em)
		else:
			await ctx.send("Clan not found. Use `?clanlist` to see a list of clans currently added to the bot.")



if not os.environ.get('TOKEN'):
    print("no token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('"'))    