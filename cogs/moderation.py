import asyncio
import datetime
import json
import sys
import traceback
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.MuteID = 1013832135020380182
        super().__init__()

    @commands.group(name="mute", invoke_without_command=True)
    async def mute_group(
        self,
        ctx: commands.Context,
        member: discord.Member = None,
        reason: str = None
    ):
        if not ctx.author.guild_permissions.ban_members: return
        if ctx.author.bot: return
        if not ctx.invoked_subcommand:
            if not member:
                embed = discord.Embed(
                    title=f"Mute command",
                    description=f"`Description:` Mute a member in the server.\n`Subcommands:` mute -timed\n`Usage:` mute <member> [reason] or mute --timed <member> <time> [reason]",
                    color = discord.Color.green()
                )
                embed.set_thumbnail(url=ctx.guild.me.avatar.url)
                return await ctx.send(embed=embed)
            if member:
                if not reason: reason = "N/A"
                if (
                    member == ctx.guild.owner or member.id in self.bot.owner_ids
                ):
                    return await ctx.send(f":x: You cannot mute the owner of this bot, or the bot owner!")
                if member == ctx.author: return await ctx.send(":x: You cannot mute yourself!")
                if (
                    member.top_role > ctx.author.top_role or member.top_role == ctx.author.top_role
                ):
                    return await ctx.send(":x: You cannot mute this member due to role hierarchy!")
                else:
                    embed = discord.Embed(
                        description=f"***__Successfully muted {member}__***",
                        color = discord.Color.green()
                    )
                    dmBed = discord.Embed(
                        description=f"***__You have been permanently muted from {ctx.guild.name}__***\n`Reason:` {reason}",
                        color = discord.Color.red(),
                        timestamp=ctx.message.created_at
                    )
                    dmBed.set_thumbnail(url=ctx.guild.me.avatar.url)
                    try: await member.send(embed=dmBed)
                    except: pass
                    await member.add_roles(ctx.guild.get_role(self.MuteID))
                    await ctx.send(embed=embed)

    @mute_group.command(name="-timed")
    async def mute_group_timed(
        self,
        ctx: commands.Context,
        member: discord.Member=None,
        time: str = None,
        reason: str = None
    ):
        if not ctx.author.guild_permissions.manage_messages: return
        if ctx.author.bot: return
        if not member:
            return await ctx.send(":x: `Member` is a missing argument that's required. If you need help with the command, please run `>mute`.")
        if member:
            if not reason: reason = "N/A"
            if not time: return await ctx.send(":x: `Time` is a missing argument that's required. If you need help with the command, please run `>mute`.")
            if (
                member == ctx.guild.owner or member.id in self.bot.owner_ids
            ):
                return await ctx.send(f":x: You cannot mute the owner of this bot, or the mute owner!")
            if member == ctx.author: return await ctx.send(":x: You cannot mute yourself!")
            if (
                member.top_role > ctx.author.top_role or member.top_role == ctx.author.top_role
            ):
                return await ctx.send(":x: You cannot mute this member due to role hierarchy!")
            else:
                seconds = 0
                try:
                    if time.lower().endswith("m"):
                        seconds += int(time.replace("m", "")) * 60
                    elif time.lower().endswith("h"):
                        seconds += int(time.replace("h", "")) * 3600
                    elif time.lower().endswith("d"):
                        seconds += int(time.replace("d", "")) * 86400
                    elif time.lower().endswith("w"):
                        seconds += int(time.replace("w", "")) * 604800
                    elif time.lower().endswith("mo"):
                        seconds += int(time.replace("mo", "")) * 2592000
                    else:
                        return await ctx.send(f":x: Invalid `Time` argument, `{time}`, please use the following time formats: ```1m,\n1h,\n1d,\n1w,\n1mo```")
                except:
                    return await ctx.send(f":x: Invalid `Time` argument, `{time}`, please use the following time formats: ```1m,\n1h,\n1d,\n1w,\n1mo```")
                embed = discord.Embed(
                    description=f"***__Successfully muted {member}__***",
                    color = discord.Color.green()
                )
                dmBed = discord.Embed(
                    description=f"***__You have been muted from {ctx.guild.name}__***\n`Reason:` {reason}\n'Time:' {time}",
                    color = discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                dmBed.set_thumbnail(url=ctx.guild.me.avatar.url)
                try: await member.send(embed=dmBed)
                except: pass
                await member.add_roles(ctx.guild.get_role(self.MuteID))
                self.bot.loop.call_later(seconds, asyncio.create_task, member.remove_roles(ctx.guild.get_role(self.MuteID)))
                await ctx.send(embed=embed)
                with open("temptasks.json", "r") as f:
                    data = json.load(f)
                data['mutes'].append(
                    [
                        member.id,
                        datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds))
                    ]
                )
                self.bot.cursor.execute("INSERT INTO mutes(user,time) VALUES(?,?)",(member.id,datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds))))
                self.bot.db.commit()
                with open("temptasks.json", "w") as f:
                    json.dump(data, f, indent=4)


#    @commands.Cog.listener("on_ready")
    async def cog_load(self):
        print("cogs.Moderation is now loaded.")

#    @commands.Cog.listener()
# Moved this thing to main
    async def on_command_error(self, ctx, error):
        em = discord.Embed(description=f"**An error occured!**\n```py\n{error}```", color=discord.Color.red())
        await ctx.send(embed=em)
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

#    @commands.Cog.listener()
# already existing in main
    async def on_message(self, message: discord.Message):
        from responses import responses
        await responses(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
