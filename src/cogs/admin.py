import discord
from discord.ext import commands,tasks
import json
import asyncio
import random
import datetime
import os
import aiohttp
import textwrap
import asyncio
import io
import time
import typing
import inspect
import requests

from bs4 import BeautifulSoup
import codecs

from urllib.request import Request, urlopen
import urllib

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client
        
    def timeout(self, time):
        if time.endswith("s"):
            time = time.replace("s", "")
            return int(time)
        elif time.endswith("m"):
            time = time.replace("m", "")
            time = int(time)
            return time * 60
        elif time.endswith("h"):
            time = time.replace("h", "")
            time = int(time)
            return time * 60 * 60
        elif time.endswith("d"):
            time = time.replace("d", "")
            time = int(time)
            return time * 60 * 60 * 24
        elif time.endswith("w"):
            time = time.replace("w", "")
            time = int(time)
            return time * 60 * 60 * 24 * 7
        else:
            time = int(time)
            return time

    with open("bot.json", "r") as f:
        data = json.load(f)
        prefix = data["prefix"]
        token = data["token"]

    @commands.Cog.listener()
    async def on_ready(self):
        main_logs = 646085909288058880
        channel = self.client.get_channel(main_logs)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        embed = discord.Embed(description=f"Kicked {member.mention} from the server",
                              colour=discord.Colour.red())
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        if member.guild_permissions.ban_members:
            if ctx.author == member:
                await ctx.send("You can't ban yourself!")
            else:
                await ctx.send("I can't ban this member!")
        else:
            embed = discord.Embed(description=f"Banned {member.mention} from the server",
                                  colour=discord.Colour.red())
            await member.ban(reason=reason)
            await ctx.send(embed=embed)

    @commands.command(aliases=[])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name='Muted')

        await member.remove_roles(role)
        embed = discord.Embed(colour=discord.Colour.dark_blue())
        embed.set_author(name=f"{member.display_name} has been unmuted")
        await ctx.send(embed=embed)

    @commands.command(aliases=["suggestion-mute"])
    @commands.has_permissions(manage_roles=True)
    async def suggestionmute(self, ctx, member: discord.Member):
        with open("configs.json", "r") as f:
            data = json.load(f)
            sm = data["suggestion-mute-role"]
        role = ctx.guild.get_role(sm)
        await member.add_roles(role)
        embed = discord.Embed(colour=discord.Colour.dark_red(),
                              description=f"{member.mention} can now not post suggestions")
        await ctx.send(embed=embed)

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        if amount is None:
            amount = 5
        await ctx.channel.purge(limit=amount + 1)
        if amount < 2:
            embed = discord.Embed(colour=discord.Colour.teal(),
                                  description=f"**Cleared {amount} message** :white_check_mark:"
                                  )
        else:
            embed = discord.Embed(colour=discord.Colour.teal(),
                                  description=f"**Cleared {amount} messages** :white_check_mark:"
                                  )
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(aliases=["announcement"])
    @commands.has_permissions(manage_channels=True)
    async def announce(self, ctx, *, message):
        with open("configs.json", "r") as f:
            data = json.load(f)
            announce_footer = data["announce-footer"]
        await ctx.message.delete()
        embed = discord.Embed(title="**ANNOUNCEMENT**",
                              description=f"\n{message}")
        embed.set_footer(text=f"{announce_footer}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["arole", "ar"])
    async def addrole(self, ctx, member: discord.Member, *, roles: discord.Role):
        await member.add_roles(roles)
        embed = discord.Embed(colour=discord.Colour.blue(), description=f"{member.mention} has been given the {roles} role")
        await ctx.send(embed=embed)

    @commands.command(aliases=["rrole", "rr"])
    @commands.has_permissions(manage_roles=True)
    async def takerole(self, ctx, member: discord.Member, *, roles: discord.Role):
        await member.remove_roles(roles)
        embed = discord.Embed(colour=discord.Colour.blue(), description=f"{member.mention} has had the {roles} role removed!")
        await ctx.send(embed=embed)

    @commands.command(aliases=[])
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nick):
        if member is None:
            member = ctx.author

        embed = discord.Embed(colour=discord.Colour.teal(),
                              description=f"Nickname of {member.mention} has been set to {nick}")
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        await ctx.send(embed=embed)
        await member.edit(nick=nick)

    @commands.command(aliases=["nickreset"])
    @commands.has_permissions(manage_nicknames=True)
    async def resetnick(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(colour=discord.Colour.teal(),
                              description=f"Nickname of {member.mention} has been reset")
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        await ctx.send(embed=embed)
        await member.edit(nick=member.name)

    @commands.command()
    @commands.has_role('*')
    async def ticketsamount(self, ctx):
        channels_list = ctx.guild.channels
        ticket_channels = []
        t = 0
        for x in channels_list:
            if "ticket" in x.name:
                ticket_channels.append(x.mention)
                t = t + 1

        embed = discord.Embed(title="Open Tickets", colour=discord.Colour.gold(),
                              description="\n".join(ticket_channels))

        embed.set_footer(text=f"Total tickets - {t}")
        await ctx.send(embed=embed)



    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Required Arguments Missing',
                                  description=f"Incorrect command usage! \n**Please use**: `{prefix}kick @User @Reason`",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing Permissions',
                                  description=f"{ctx.author} -> You don't have permission to run this command.",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Required Arguments Missing',
                                  description=f"Incorrect command usage! \n**Please use**: `{prefix}ban @User @Reason`",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing Permissions',
                                  description=f"{ctx.author} -> You don't have permission to run this command.",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Required Arguments Missing',
                                  description=f"Incorrect command usage! \n**Please use**: `{prefix}unmute @User`",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing Permissions',
                                  description=f"{ctx.author} -> You don't have permission to run this command.",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

    # SuggestionsMute - Done
    @suggestionmute.error
    async def suggestionmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Required Arguments Missing',
                                  description=f"Incorrect command usage! \n**Please use**: `{prefix}suggestionmute @User`",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing Permissions',
                                  description=f"{ctx.author} -> You don't have permission to run this command.",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Required Arguments Missing',
                                  description=f"Incorrect command usage! \n**Please use**: `{prefix}purge [Amount]`",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing Permissions',
                                  description=f"{ctx.author} -> You don't have permission to run this command.",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Required Arguments Missing',
                                  description=f"Incorrect command usage! \n**Please use**: `{prefix}announce [Text]`",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing Permissions',
                                  description=f"{ctx.author} -> You don't have permission to run this command.",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Required Arguments Missing',
                                  description=f"Incorrect command usage! \n**Please use**: `{prefix}nick @User @Nickname`",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing Permissions',
                                  description=f"{ctx.author} -> You don't have permission to run this command.",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

    @resetnick.error
    async def resetnick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Required Arguments Missing',
                                  description=f"Incorrect command usage! \n**Please use**: `{prefix}resetnick @User`",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing Permissions',
                                  description=f"{ctx.author} -> You don't have permission to run this command.",
                                  colour=discord.Colour.red())
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg')
            embed.set_footer(text="© Chaotic Destiny Host")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role('Support')
    async def mute(self, ctx, member: discord.Member = None, time: typing.Union[int, float] = 1800, *, reason = "no reason"):
        if not member:
            return await ctx.send("specify a member to mute")
        mutedRole = ctx.guild.get_role(662700026413187083)
        memberRole = ctx.guild.get_role(610769312424394753)
        embed = discord.Embed(
            title="You have been muted in: Chaotic Destiny",
            description="Here's all the information regarding your mute:",
            colour=0xDD2E44
        )
        embed.set_footer(text=member.name, icon_url=member.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/687746620674408472/687746697044295738/xD.jpg")

        embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
        embed.add_field(name="Reasoning:", value=f"{reason}", inline=False)
        embed.add_field(name="Time:", value=f"{time} seconds", inline=False)

        await member.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.remove_roles(memberRole)
        await ctx.send(f"{member.mention} has been muted for: {reason}.")
        channel = self.client.get_channel(638106435645079553)
        await channel.send(embed=embed)
        await channel.send(f'{member} has been muted.')
        await asyncio.sleep(timeout(time))
        await member.remove_roles(mutedRole)
        await member.add_roles(memberRole)




def setup(client):
    client.add_cog(Admin(client))
