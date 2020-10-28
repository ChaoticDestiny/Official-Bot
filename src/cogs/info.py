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

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    with open("bot.json", "r") as f:
        data = json.load(f)
        prefix = data["prefix"]
        token = data["token"]
        print("Info Cog Loaded")

    @commands.Cog.listener()
    async def on_ready(self):
        main_logs = 646085909288058880
        embed = discord.Embed(colour=discord.Colour.gold(), description="Info Commands Loaded")
        channel = self.client.get_channel(main_logs)
        await channel.send(embed=embed)

    @commands.command(aliases=["userinfo"])
    async def user(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=member.name, colour=discord.Colour.blurple(),
                              description="User ID - " + str(member.id)
                              )
        embed.set_author(name="User Info", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Called by {ctx.author}")
        embed.add_field(inline=False, name="Server Nickname", value=member.display_name)
        cd = member.created_at
        cd_month = cd.strftime("%b")
        embed.add_field(inline=True, name="Created at", value=f"{cd.day} {cd_month} {cd.year}")
        jd = member.joined_at
        jd_month = jd.strftime("%b")
        embed.add_field(inline=True, name="Joined at", value=f"{jd.day} {jd_month} {jd.year}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["server"])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        cd = guild.created_at  # Guild creation date
        embed = discord.Embed(colour=discord.Colour.blue(), title="Server Info", description=f"""
        \N{SMALL BLUE DIAMOND} Name - **{guild.name}**
        \N{SMALL BLUE DIAMOND} ID - {guild.id}
        \N{SMALL BLUE DIAMOND} Owner - **{guild.owner}**
        \N{SMALL BLUE DIAMOND} Location - **{guild.region}**
        \N{SMALL BLUE DIAMOND} Members - **{guild.member_count}**
        \N{SMALL BLUE DIAMOND} Verification - **{guild.verification_level}**
        \N{SMALL BLUE DIAMOND} Created On - **{cd.day} {cd.strftime("%b")} {cd.year}**
        """
                              )

        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Called by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"__Avatar of {member.display_name}__",
                              colour=discord.Colour.blue())
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f"Called by {ctx.author}")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["boost", "perks"])
    async def BoosterPerks(self, ctx):
        embedo = discord.Embed(title='Perks', colour=discord.Colour.gold())
#        embedo.add_field(name='Comming Soon',value='', inline=False)
        embedo.add_field(name='✯ Custom Emojis', value="Upload up to 3 Custom Emoji's", inline=False)
        embedo.add_field(name='✯ Animated Emojis', value="Upload up to 3 Animated Emoji's", inline=False)
        embedo.add_field(name='✯ Custom Rank', value='Get a Custom Rank on our Upcoming MC Server', inline=False)
        embedo.add_field(name='✯ Extra Port', value='Get an Extra Port Forever', inline=False)
        embedo.add_field(name='✯ Discount', value='Get a Discount Code for our billing website', inline=False)

        embedo.set_footer(text="© Chaotic Destiny Hosting")
        await ctx.send(embed=embedo)

    @commands.command()
    async def FreeServer(self, ctx):
        embed = discord.Embed(title='**Here is info about the free discord bot hosting!**', colour=discord.Colour.gold())
        embed.add_field(name='**Free Server Specs**', value='Info : Host your free discord bot now! For free! Thats the best price!', inline=False)
        embed.add_field(name='✯ RAM : 128MB', value='➭ Basic Bots will run on this. ', inline=False)
        embed.add_field(name='✯ DISK : 500MB', value='➭ Logging Bots will need more than this.', inline=False)
        embed.add_field(name='✯ CPU : 1x 3.5GHz', value='➭ Most basic bots will run on this', inline=False)
        embed.add_field(name='✯ LOCATION : EU', value='➭ Located in Germany', inline=False)
        embed.add_field(name='✯ NODE : Free1', value='➭ Hosted on Free1.Eu Node', inline=False)

        embed2 = discord.Embed(title='**Here is info how to claim your discord bot hosting!**', colour=discord.Colour.gold())
        embed2.add_field(name='✯ Step 1', value='➭Create account on https://panel.chaoticdestiny.host/auth/register ', inline=False)
        embed2.add_field(name='✯ Step 2', value='➭Invite your friend. (Not an Alt)', inline=False)
        embed2.add_field(name='✯ Step 3', value='➭Then go in #tickets and press :free: reaction on the message.', inline=False)
        embed2.add_field(name='✯ Step 4', value='➭After opening a ticket , fill this format with your data in it : \n  ➭ Username : \n ➭ Bot coding language :', inline=False)

        embed.set_footer(text="© Chaotic Destiny Hosting")
        embed2.set_footer(text="© Chaotic Destiny Hosting")
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)

def setup(client):
    client.add_cog(Info(client))
