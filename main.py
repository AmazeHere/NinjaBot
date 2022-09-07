import discord
from discord.ext import commands
import responses
import os
import sys
import time
import asyncio
import logging
import sqlite3
from discord.utils import setup_logging
import datetime, time
import contextlib
import io


schema=\
"""CREATE TABLE IF NOT EXISTS mutes(
user INTEGER PRIMARY KEY UNIQUE NOT NULL,
time REAL);
"""

log=logging.getLogger("Ninja")
#later ima use logging

class Ninja(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?", intents=discord.Intents.all())
        self.db=sqlite3.connect("bot.db")
        self.cursor=self.db.cursor()
    async def setup_hook(self):
        "Do something here like cog loading"
        # await self.load_extension("cogs.moderation")
        log.info('bot has been connected to discord :D')
        self.cursor.execute(schema)
    
    async def on_command_error(self, ctx, error):
        em = discord.Embed(description=f"**An error occured!**\n```py\n{error}```", color=discord.Color.red())
        await ctx.send(embed=em)
        log.error("Command %s raised an error:\n" % ctx.invoked_with, exc_info=error)
        


# i use 2.0 so intents are needed
bot = Ninja()
bot.owner_ids = [900793535828197446,958390293760184392,875213353658777620]


# @bot.event bloat
async def on_ready():
    print('bot has been connected to discord :D')

start_time = time.time()

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
    await ctx.send("bot has been shutdown D:")
    await ctx.bot.close()

@bot.command()
async def ping(ctx):
    start=time.perf_counter()
    msg = await ctx.send("Latency: ...ms\nWebsocket: ...ms")
    end=time.perf_counter()
    duration=(end-start)*1000
    await msg.edit(content=f"Latency: {duration:.2f}ms\nWebsocket: {bot.latency*1000:.2f}ms")
    
@bot.command()
async def say(ctx,*, message=None):
    await ctx.send(message)
    
    
@bot.command(pass_context=True)
async def uptime(ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.add_field(name="Uptime", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

@bot.command(name="exec",aliases=["eval"])
@commands.is_owner()
async def _exec(ctx, *, code):

    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'{str_obj.getvalue()}')
    
# loop=asyncio.get_event_loop()


async def main ():
    async with bot:
        setup_logging()
        await bot.start("OTk0NjIxMjg3Mjg2NzE4NTA0.G5iJbP.bSWeqPsVkevDttpOUEbvakLygrsukxcpsVhuzY")


asyncio.run(main())