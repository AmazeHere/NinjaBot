import discord
from discord.ext import commands
import asyncio
import time

bot = commands.Bot(command_prefix = ">",intents=discord.Intents.all()) #i use 2.0 so intents are needed



@bot.event
async def on_ready():
    print("this sexy bot has been connected to discord")
    
@bot.listen()
async def on_message(message):
    print(f'\033[1;36;40m {message.author}: {message.content}') #this line print the whole chat cuz ez message logger heheha
    if message.author == bot.user:
        return

    if message.content.startswith('cookie'):
        await message.channel.send("🍪")
        
    if message.content.startswith('se'):
        await message.channel.send("sex")
        
    if 'kiss' in message.content:
        print(f'\033[1;33;40m react to {message.author} with moyai')
        await message.add_reaction("😽")


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run("OTk0NjIxMjg3Mjg2NzE4NTA0.G5iJbP.bSWeqPsVkevDttpOUEbvakLygrsukxcpsVhuzY")