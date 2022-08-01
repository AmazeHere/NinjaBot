import discord
from discord.ext import commands
import asyncio
import time
import os, sys 

bot = commands.Bot(command_prefix = ">",intents=discord.Intents.all()) #i use 2.0 so intents are needed
bot.owner_ids=[900793535828197446,875213353658777620]


@bot.event
async def on_ready():
    print('bot has been connected to discord:D')
    
@bot.listen()
async def on_message(message):
    print(f'{message.author}: {message.content}') #this line print the whole chat cuz ez message logger heheha
    if message.author == bot.user:
        return
        
    if message.content.startswith('cookie'):
        await message.channel.send("🍪")
        
    if message.content.startswith('sex'):
        await message.channel.send("sex")
        
    if message.content.startswith('free'): 
        await message.channel.send('<https://youtu.be/xvFZjo5PgG0>')
        
    if message.content.startswith('cock'):
        await message.channel.send('🐔')
        
    if 'kiss' in message.content:
        print(f'react to {message.author} with moyai')
        await message.add_reaction("😽")

@bot.command() # bro pass_context is for ancient coders that lives in a cave
@commands.is_owner()
async def restart(ctx):
    await ctx.send("restarting bot :D")
    os.execv(sys.executable,["python"]+sys.argv)
    
@bot.command() # pass_context is removed on dpy 1.0.0
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("bot has been shutdown")
    await ctx.bot.close()   

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run("OTk0NjIxMjg3Mjg2NzE4NTA0.G5iJbP.bSWeqPsVkevDttpOUEbvakLygrsukxcpsVhuzY")
