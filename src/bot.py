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
import traceback
import psutil


with open("bot.json","r") as f:
    data = json.load(f)
    prefix = data["prefix"]
    token = data["token"]

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),case_insensitive=True,help_command=None)
cdate = datetime.datetime.now().date()

@client.event
async def on_ready():
    with open("bot.json","r") as f:
        data = json.load(f)
        status_text = data["status"]
    await client.change_presence(status=discord.Status.dnd ,activity=discord.Game(status_text))
    change_status.start()
    ctime = datetime.datetime.now()
    membercount.start()
    main_logs = 646085909288058880
    channel = client.get_channel(main_logs)

@client.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    embed = discord.Embed(title='Chaotic Destiny Shutdown', description=f"Administrator has executed the shutdown command!",colour=red)
    await ctx.send(embed=embed)
    await asyncio.sleep(2)
    await client.change_presence(activity=discord.Activity(status=discord.Status.idle, name="Assets (1/3)",type=discord.ActivityType.watching))
    await asyncio.sleep(3)
    await client.change_presence(activity=discord.Activity(status=discord.Status.idle, name="Assets (2/3)",type=discord.ActivityType.watching))
    await asyncio.sleep(3)
    await client.change_presence(activity=discord.Activity(status=discord.Status.idle, name="Assets (3/3)",type=discord.ActivityType.watching))
    await asyncio.sleep(3)
    await client.change_presence(activity=discord.Activity(status=discord.Status.online, name="https://panel.chaoticdestiny.host",type=discord.ActivityType.watching))
    await asyncio.sleep(5)
    await client.logout()

@client.event
async def on_member_join(member):
    channelaa = client.get_channel(632331894532603915)
    embed = discord.Embed(title='👋 Welcome!', description="Welcome, {} to {}!".format(member.mention, member.guild.name), colour=gold)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.add_field(name="__Member__", value=member.name, inline=False)
    embed.add_field(name="__User ID__", value=member.id, inline=False)
    embed.add_field(name='__New Member Count__', value='{}'.format(str(member.guild.member_count)), inline=False)
    embed.add_field(name="__Joined Discord__", value=member.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"))
    embed.add_field(name="__Rules__", value="Please read <#664917307855994912>", inline=False)
    embed.add_field(name="__Verify__", value="Verify in <#704715255196024966>", inline=False)
    embed.set_thumbnail(url=member.avatar_url)
    await channelaa.send(embed=embed)
    x = member.guild.get_role(610769312424394753)
    y = member.guild.get_role(662695593638101071)
    z = member.guild.get_role(662694754928295937)
    await member.add_roles(y)
    await member.add_roles(z)
    await asyncio.sleep(10)
    if "Free Customer" in [x.name for x in member.roles]:
        for x in member.roles:
             if x.name == "Free Customer":
                 role1 = discord.utils.get(member.guild.roles, name='Deleted Server')
                 await member.add_roles(role1)
                 await member.add_roles(role0)
                 role2 = discord.utils.get(member.guild.roles, name='Free Customer')
                 await member.remove_roles(role2)
                 role3 = discord.utils.get(member.guild.roles, name='Premium Customer')
                 await member.remove_roles(role3)
                 channel = client.get_channel(638106435645079553)
                 await channel.send(f"{member.mention} rejoined, previously used to be Free Customers.")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(632331894532603915)
    jd = member.joined_at
    jd_month = jd.strftime("%b")
    embed = discord.Embed(title='Goodbye :( 👋', description="Sad to see you go {}. We hope you come back!".format(member.mention), colour=red)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.add_field(name="__User ID__", value=member.id, inline=False)
    embed.add_field(name='__New Member Count__', value='{}'.format(str(member.guild.member_count)), inline=False)
    embed.add_field(name="__Joined Chaotic Destiny__",value=f"{jd.day} {jd_month} {jd.year}", inline=False)
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)


@commands.command()
@commands.has_role("Server Creator")
async def leaderboard(ctx):
    arr = []
    
    guild = client.get_guild(610767680009535488)
    for channel in guild.channels:
        count = 0
        async for message in channel.history():
            count += 1
        arr.append((message.author.id, count))
    
    
        
        

def colour(r,g,b):
    return discord.Colour.from_rgb(r,g,b)
red = discord.Colour.red()
darkred = discord.Colour.dark_red()
blue = discord.Colour.blue()
darkblue = discord.Colour.dark_blue()
blurple = discord.Colour.blurple()
greyple = discord.Colour.greyple()
purple = discord.Colour.purple()
darkpurple = discord.Colour.dark_purple()
green = discord.Colour.green()
darkgreen = discord.Colour.dark_green()
teal = discord.Colour.teal()
darkteal = discord.Colour.dark_teal()
magenta = discord.Colour.magenta()
darkmagenta = discord.Colour.dark_magenta()
gold = discord.Colour.gold()
darkgold = discord.Colour.dark_gold()
orange = discord.Colour.orange()
darkorange = discord.Colour.dark_orange()


@client.command()
async def help(ctx, *, query="None"):
    with open("bot.json", "r") as f:
        data = json.load(f)
        prefix = data["prefix"]

    if query.lower() in ["admin", "admins"]:
        embed = discord.Embed(title="Admin Commands", colour=red)
        embed.add_field(name="Announce", value=f"`{prefix}announce <message>`", inline=False)
        embed.add_field(name="Purge", value=f"`{prefix}purge <amount>`", inline=False)
        embed.add_field(name="Create Channel", value=f"`{prefix}createchannel <name> <role> <topic>`", inline=False)
        embed.add_field(name="Kick", value=f"`{prefix}kick <member>`", inline=False)
        embed.add_field(name="Ban", value=f"`{prefix}ban <member>`", inline=False)
        embed.add_field(name="Mute", value=f"`{prefix}mute <member>`", inline=False)
        embed.add_field(name="Unmute", value=f"`{prefix}unmute <member>`", inline=False)
        embed.add_field(name="Nick", value=f"`{prefix}nick <member> <nick>`", inline=False)
        embed.add_field(name="Reset Nick", value=f"`{prefix}resetnick <member>`", inline=False)
        embed.add_field(name="Give Role", value=f"`{prefix}giverole <member> <role>`", inline=False)

    elif query.lower() in ["owner"]:
        embed = discord.Embed(colour=green, title="Owner Commands")
        embed.add_field(name="Config", value=f"`{prefix}config`")
        embed.add_field(name="Set Status", value=f"`{prefix}status <status>`", inline=False)
        embed.add_field(name="Set Name", value=f"`{prefix}setname <name>`", inline=False)
        embed.add_field(name="Close Bot", value=f"`{prefix}shutdown`", inline=False)

    elif query.lower() in ["pictures", "pic", "pics", "images", "img", "image"]:
        embed = discord.Embed(colour=green, title="Image Commands")
        embed.add_field(name="**Cat Foto**", value=f"`{prefix}cat`")
        embed.add_field(name="**Dog Foto**", value=f"`{prefix}dog`", inline=False)
        embed.add_field(name="**Shibe Foto**", value=f"`{prefix}shibe`", inline=False)
        embed.add_field(name="**Birb Foto**", value=f"`{prefix}birb`", inline=False)

    elif query.lower() in ["fighting", "fight", "1v1", "fun"]:
        embed = discord.Embed(colour=green, title="Fun Commands")
        embed.add_field(name="Fight", value=f"`{prefix}fight <User>`")
        embed.add_field(name="HowGay", value=f"`{prefix}howgay <User>`", inline=False)
        embed.add_field(name="Compare", value=f"`{prefix}compare <User>`", inline=False)
        embed.add_field(name="Meme", value=f"`{prefix}meme`")
        embed.add_field(name="8Ball", value=f"`{prefix}8ball <Question>`")

    elif query.lower() in ["ticket", "tickets"]:
        embed = discord.Embed(colour=green, title="Ticket Commands")
        embed.add_field(name="Add an User from your ticket", value=f"`{prefix}add <User>`")
        embed.add_field(name="Remove an User from your ticket", value=f"`{prefix}remove <User>`", inline=False)

    elif query.lower() in ["info", "about"]:
        embed = discord.Embed(colour=green, title="Information Commands")
        embed.add_field(name="Server Info", value=f"`{prefix}serverinfo`")
        embed.add_field(name="User Info", value=f"`{prefix}userinfo <User>`", inline=False)
        embed.add_field(name="User Avatar", value=f"`{prefix}avatar <User>`", inline=False)
        embed.add_field(name="Booster Perks", value=f"`{prefix}boost`", inline=False)

    elif query.lower() in ["links", "link"]:
        embed = discord.Embed(colour=green, title="Links Commands")
        embed.add_field(name="Website Link", value=f"`{prefix}website`")
        embed.add_field(name="Panel Link", value=f"`{prefix}panel`", inline=False)
        embed.add_field(name="Billing", value=f"`{prefix}billing`", inline=False)
        embed.add_field(name="Twitter", value=f"`{prefix}twitter`", inline=False)
        embed.add_field(name="Status", value=f"`{prefix}status`", inline=False)
        embed.add_field(name="Donate", value=f"`{prefix}donate`", inline=False)
        embed.add_field(name="MCMarket", value=f"`{prefix}mcm`", inline=False)
        embed.add_field(name="Official Youtube", value=f"`{prefix}youtube`", inline=False)
        embed.add_field(name="Terms & Privacy", value=f"`{prefix}tos`", inline=False)

    else:

        embed = discord.Embed(title="Help Commands", colour=blue)
        embed.set_footer(text=f"Called by {ctx.author}")
        embed.add_field(name="Images Help", value=f"`{prefix}help images`", inline=False)
        embed.add_field(name="Fun Help", value=f"`{prefix}help fun`", inline=False)
        embed.add_field(name="Info Help", value=f"`{prefix}help info`", inline=False)
        embed.add_field(name="Links Help", value=f"`{prefix}help links`", inline=False)
        embed.add_field(name="Tickets Help", value=f"`{prefix}help tickets`", inline=False)

    await ctx.send(embed=embed)

@client.command(aliases=["latency"])
async def ping(ctx):
    ping = round(client.latency*1000)
    embed = discord.Embed(Title='Pong')
    embed.set_author(name=f"🏓 Bot Ping is : {ping}ms")
    embed.set_footer(text=f"Called by {ctx.author}")
    await ctx.send(embed=embed)




@client.command()
async def remove(ctx, *, member: discord.Member):
    channel = ctx.channel
    if "ticket" in str(channel.name):
        await channel.set_permissions(member, send_messages=False, read_messages=False, attach_files=False)
        await ctx.send(f"Successfully removed that user from the ticket.")
    elif "partner" in str(channel.name):
        await channel.set_permissions(member, send_messages=False, read_messages=False, attach_files=False)
        await ctx.send(f"Successfully removed that user from the ticket.")
    elif "exclusive" in str(channel.name):
        await channel.set_permissions(member, send_messages=False, read_messages=False, attach_files=False)
        await ctx.send(f"Successfully removed that user from the ticket.")
    elif "server" in str(channel.name):
        await channel.set_permissions(member, send_messages=False, read_messages=False, attach_files=False)
        await ctx.send(f"Successfully removed that user from the ticket.")
    else:
        await ctx.send(f"This is not a ticket channel")
        
@client.command()
async def add(ctx, *, member: discord.Member):
    channel = ctx.channel
    if "ticket" in str(channel.name):
        await channel.set_permissions(member, send_messages=True, read_messages=True, attach_files=True)
        await ctx.send(f"Successfully added that user from the ticket.")
    elif "partner" in str(channel.name):
        await channel.set_permissions(member, send_messages=True, read_messages=True, attach_files=True)
        await ctx.send(f"Successfully added that user from the ticket.")
    elif "exclusive" in str(channel.name):
        await channel.set_permissions(member, send_messages=True, read_messages=True, attach_files=True)
        await ctx.send(f"Successfully added that user from the ticket.")
    elif "server" in str(channel.name):
        await channel.set_permissions(member, send_messages=True, read_messages=True, attach_files=True)
        await ctx.send(f"Successfully added that user from the ticket.")
    else:
        await ctx.send(f"This is not a ticket channel")

@client.command()
@commands.has_permissions(administrator=True)
async def close(ctx):
    channel = ctx.channel
    if "ticket" in str(channel.name):
        await ctx.send(f"Ticket successfully solved and closed.")
        await channel.delete()
    elif "partner" in str(channel.name):
        await ctx.send(f"Partnership ticket successfully solved and closed.")
        await channel.delete()
    elif "exclusive" in str(channel.name):
        await ctx.send(f"Admin ticket successfully solved and closed.")
        await channel.delete()
    elif "server" in str(channel.name):
        await ctx.send(f"Server successfully solved and closed.")
        await channel.delete()


@tasks.loop(seconds=600)
async def membercount():
    channel = client.get_channel(679400782625374227)
    await channel.edit(name=f"Member Count: {len(list(channel.guild.members))}")

@tasks.loop(seconds=600)
async def change_status():
    with open("bot.json","r") as f:
        data = json.load(f)
    status_text = data["status"]
    await client.change_presence(status=discord.Status.dnd,
    activity=discord.Game(status_text))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



client.run(token)
