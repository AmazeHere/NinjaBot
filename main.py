import discord
from discord.ext import commands
import asyncio
import time

client = commands.Bot(command_prefix = ">")

cookie = '\N{COOKIE}'

@client.event
async def on_ready():
    print("this sexy bot has been connected to discord")
    
@client.event
async def on_message(message):
    print(f'\033[1;36;40m {message.author}: {message.content}') #this line print the whole chat cuz ez message logger heheha
    if message.author == client.user:
        return

    if message.content.startswith('cookies'):
        await message.channel.send(cookie)

    await client.process_commands(message)

@client.command
async def ping(ctx):
     await ctx.send(f'your ping is {round(client.latency)}ms')

client.add_command(ping)
client.run("OTk0NjIxMjg3Mjg2NzE4NTA0.G5iJbP.bSWeqPsVkevDttpOUEbvakLygrsukxcpsVhuzY")