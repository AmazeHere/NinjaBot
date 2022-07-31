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
async def on_message(message):
    print(f'\033[1;36;40m {message.author}: {message.content}') #this line print the whole chat cuz ez message logger heheha
    if message.author == client.user:
        return

@client.command()
async def ping(ctx):
     await ctx.send(f'your ping is {round(client.latency * 1000)}ms')
     
@bot.command()
async def say(ctx, message=None)
    await ctx.send(message)

client.run("OTk0NjIxMjg3Mjg2NzE4NTA0.GbjuYO.CoJJ0Hg_i8LqBb9NQHsocwiJOM2YrKwv0r3dNk")