import asyncio
import json
import os
import sys
import traceback
import discord 
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def setup_hook(self):
        pass
    
bot = Bot(
    command_prefix=">",
    intents=discord.Intents().all(),
    owner_ids=[900793535828197446, 875213353658777620, 741486101218197565, 958390293760184392],
    case_insensitive=True,
    status=discord.Status.dnd,
    activity=discord.Activity(type=discord.ActivityType.watching, name="Onix play with himself cuz lonely")
)

async def main():
    for cog in os.listdir("./cogs"):
        try:
            await bot.load_extension("cogs."+cog[:-3])
        except Exception as e:
            print(f"Error Loading {cog}", file=sys.stderr)
            traceback.print_exc()
        # await bot.load_extension("jishaku")
    print("Logging in...")
    await bot.load_extension('jishaku')
    with open("config.json", "r") as f:
        data = json.load(f)
    async with bot:
        await bot.start(data['TOKEN'])
        
@bot.event
async def on_command_error(ctx, error):
  await ctx.send(f"Error lmao, \ 
py\n{error}`")
`

@bot.event
async def on_ready():
    print("======================================")
    print(f"Logged in")
    print(f"Bot Name: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("======================================")


asyncio.run(main())
