import discord
from discord.ext import commands
import asyncio
import time
import os
import sys

# i use 2.0 so intents are needed
bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
bot.owner_ids = [900793535828197446, 875213353658777620, 741486101218197565]


@bot.event
async def on_ready():
    print('bot has been connected to discord   :D')


@bot.listen()
async def on_message(message):
    print(f'\033[1;36;40m {message.author}: {message.content}')
    if message.author == bot.user:
        return

    if message.content.startswith('cookie'):
        await message.channel.send("🍪")

    if message.content.startswith('free'):
        await message.channel.send('<https://youtu.be/xvFZjo5PgG0>')

    if message.content.startswith('coc'):
        await message.channel.send('🐔')

    if message.content.startswith('77+33'):
        await message.channel.send('100')

    if message.content.startswith('33+77'):
        await message.channel.send('100')

    if message.content.startswith('goofy'):
        await message.channel.send('ahh')

    if 'kiss' in message.content:
        print(f'react to {message.author}')
        await message.add_reaction("😽")

    if 'dick' in message.content:
        print(f'react to {message.author}')
        await message.add_reaction("🍆")

    if 'onix' in message.content:
        print(f'react to {message.auther}')
        await message.add_reaction("🤡")


@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send("restarting bot :D")
    os.execv(sys.executable, ["python"]+sys.argv)


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("bot has been shutdown")
    await ctx.bot.close()


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run("OTk0NjIxMjg3Mjg2NzE4NTA0.G5iJbP.bSWeqPsVkevDttpOUEbvakLygrsukxcpsVhuzY")
