"""This file uses PEP8 styling"""
import contextlib
import os
import io
import sys
import sqlite3
import asyncio
import logging 
import typing
import time
import re
import math
from discord.ext import commands
from discord.utils import setup_logging
import discord
import responses
from textwrap import indent
import datetime
datetime.datetime.utcnow()

SQL_SCHEMA: str = \
"""CREATE TABLE IF NOT EXISTS mutes(
user INTEGER PRIMARY KEY UNIQUE NOT NULL,
time REAL);
"""
logger=logging.getLogger("ninja.main")


class CodeBlock(commands.Converter):
    """Code Block argument converter"""
    async def convert(self, ctx: commands.Context, block:str):
        lines=block.split("\n")
        if re.search("``?`?((py)$)?",lines[0]):
            lines[0]=re.sub("``?`?((py)$)?","",lines[0])
        if re.search("``?`?",lines[-1]):
            lines[-1]=re.sub("``?`?","",lines[-1])
        lines[-1]="await ctx.send(repr("+lines[-1]+"))"
        return "\n".join(lines)


class Ninja(commands.Bot):
    start_time: typing.ClassVar[int]
    def __init__(self) -> None:
        super().__init__(command_prefix="?",
                         intents=discord.Intents.all(),
                         case_insensitive=True,
                         strip_after_prefix=True,
                         allowed_mentions=discord.AllowedMentions(everyone=False,roles=False))
        self.db: sqlite3.Connection = sqlite3.connect("bot.db")
        self.cur: sqlite3.Cursor = self.db.cursor()
      
    
    async def setup_hook(self) -> None:
        logger.info("bot has been connected to discord :D")
        self.cur.execute(SQL_SCHEMA)
        self.db.commit()
        self.start_time = time.time() 

    
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        em = discord.Embed(description=f"**An error occured!**\n```py\n{error}```",
                           color=discord.Color.red())
        await ctx.send(embed=em)
        logger.error("Command %s raised an error:\n" % ctx.invoked_with, exc_info=error)
        
        
bot: Ninja=Ninja()
bot.owner_ids: typing.List[int]=[900793535828197446,958390293760184392,875213353658777620]


@bot.listen("on_message")
async def message_logger_responder(message):
    print(f'\033[1;36;40m {message.author}: {message.content}')
    if not message.author == bot.user:
        await responses.responses(message)


@bot.command()
@commands.is_owner()
async def restart(ctx: commands.Context) -> None:
    await ctx.send("restarting bot :D")
    os.execv(sys.executable, ["python"]+sys.argv)


@bot.command()
@commands.is_owner()
async def shutdown(ctx: commands.Context) -> None:
    await ctx.send("bot has been shutdown D:")
    await ctx.bot.close()


@bot.command()
async def ping(ctx: commands.Context) -> None:
    start=time.perf_counter()
    msg = await ctx.send("Latency: ...ms\nWebsocket: ...ms")
    end=time.perf_counter()
    duration=(end-start)*1000
    await msg.edit(content=f"Latency: {duration:.2f}ms\nWebsocket: {bot.latency*1000:.2f}ms")
    

@bot.command()
async def say(ctx: commands.Context,*, message: typing.Optional[str]=None) -> None:
    await ctx.send(message)


@bot.command() # FUCKING STOP ADDING PASS_CONTEXT=TRUE PLEASE
async def uptime(ctx: commands.Context) -> None:
    current_time = time.time()
    difference = int(round(current_time - bot.start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=0xc8dc6c)
    embed.add_field(name="Uptime", value=text)
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        await ctx.send("Current uptime: " + text)
        

@bot.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(datetime.datetime.utcnow())
    embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{client.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='use a proper value wtf.')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='no')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='no')
    else:
        await ctx.send(f"ok i will remind you {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi Fuck you, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)

@bot.command(name="exec",aliases=["eval"])
@commands.is_owner()
async def _exec(ctx: commands.Context, *, code: CodeBlock) -> None:

    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            function="async def func():\n"+indent(code,"    ")
            
            env={
            "asyncio":asyncio,
            "ctx":ctx,
            "bot":bot,
            "message":ctx.message,
            "author":ctx.author,
            "guild":ctx.guild,
            "channel":ctx.channel,
            "db": bot.db,
            "cur":bot.cur,
            "discord":discord,
            "commands":commands,
            "utils":discord.utils,
            "ui":discord.ui,
            "btnstyles":discord.ButtonStyle,
            "os":os,
            "io":io,
            "sys":sys
            }
            if ctx.message.reference and isinstance(ctx.message.reference.resolved,discord.Message):
                env["ref"]=ctx.message.reference.resolved
            else:
                env["ref"]=None
        
            env.update(globals())
            exec(function,env)
            await env["func"]()
    except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'{str_obj.getvalue()}')


async def main() -> None:
    async with bot:
        setup_logging()
        await bot.start("use your own token smh")


asyncio.run(main())
