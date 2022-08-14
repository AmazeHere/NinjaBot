import discord
from discord.ext import commands
import responses
import os
import sys

# i use 2.0 so intents are needed
bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
bot.owner_ids = [900793535828197446, 875213353658777620, 741486101218197565]


@bot.event
async def on_ready():
    print('bot has been connected to discord :D')


@bot.listen()
async def on_message(message):
    print(f'\033[1;36;40m {message.author}: {message.content}')
    if message.author == bot.user:
        return

    # one line for all responses in main.py!
    await responses.responses(message)


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
