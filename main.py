import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time


Client = discord.Client()
client = commands.Bot(command_prefix = ">")


@client.event
async def on_ready():
    print("this sexy bot has been connected to discord")
    
@client.event
async def on_message(message):
    print(f'\033[1;36;40m {message.author}: {message.content}') #this line print the whole chat cuz ez message logger heheha
    if message.author == client.user:
        return

@Bot.command
async def ping(ctx):
     await ctx.send(f'your ping is {round(client.latency)}ms')

client.run("OTk0NjIxMjg3Mjg2NzE4NTA0.G5iJbP.bSWeqPsVkevDttpOUEbvakLygrsukxcpsVhuzY")