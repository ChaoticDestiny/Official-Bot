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

class Staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    with open("bot.json", "r") as f:
        data = json.load(f)
        prefix = data["prefix"]
        token = data["token"]
        print("Staff Cog Loaded")

    @commands.Cog.listener()
    async def on_ready(self):
        main_logs = 646085909288058880
        channel = self.client.get_channel(main_logs)

    def can_create_channel(self, ctx):
        with open("configs.json", "r") as f:
            data = json.load(f)
        roleid = int(data["create-channel-role"])
        author_roles = []
        for x in ctx.author.roles:
            author_roles.append(x.id)
        if roleid in author_roles:
            return True
        else:
            return False

    @commands.command()
    @commands.check(can_create_channel)
    async def createchannel(self, ctx, channel=None, role: discord.Role = None, *, topic=None):
        if channel is None:
            await ctx.send(f"Command usage is `{prefix}createchannel <channelname> <access role> <topic>`")
        else:
            if topic is None:
                topic = "No Topic Provided"
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.get_role(role.id): discord.PermissionOverwrite(read_messages=True, send_messages=True),
                ctx.guild.me: discord.PermissionOverwrite(send_messages=True, manage_messages=True),
                ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            await ctx.guild.create_text_channel(channel, overwrites=overwrites, position=0, topic=str(topic))

    @commands.command()
    @commands.is_owner()
    async def config(self, ctx, module=None, *, value=None):
        found = False
        with open("configs.json", "r") as f:
            data = json.load(f)

        if module is None:

            embed = discord.Embed(title="__All Configs__", colour=discord.Colour.green(),
                                  description=f"""\n
            `{prefix}config suggestions-mute-role <ROLE ID>`
            `{prefix}config support-role <ROLE ID>`
            `{prefix}config support-role <ROLE ID>`
            `{prefix}config create-channel-role <ROLE ID>`
            `{prefix}config tickets-category <CAT ID>`
            `{prefix}config logs-channel <CHANNEL ID>`
            `{prefix}config blacklist-channel <CHANNEL ID>`
            `{prefix}config announce-footer <TEXT>`
            """)
            await ctx.send(embed=embed)

        else:
            module = module.lower()
            if module in ["suggestion-mute-role", "suggestions-mute-role"]:
                data["suggestions-mute-role"] = value
                found = True

            elif module in ["support-role"]:
                data["support-role"] = value
                found = True

            elif module in ["tickets-category", "tickets-category"]:
                data["tickets-category"] = value
                found = True

            elif module in ["announce-footer"]:
                data["announce-footer"] = value
                found = True

            elif module in ["create-channel-role"]:
                data["create-channel-role"] = value
                found = True

            elif module in ["logs-channel", "ticket-logs"]:
                data["logs-channel"] = value
                found = True

            elif module in ["blacklist-channel", "blacklist-channels"]:
                data["blacklist-channels"] = value
                found = True

            if found == True:
                embed = discord.Embed(colour=discord.Colour.green(),
                                      description=f"Edited Config `{module}` to value `{value}`")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=discord.Colour.blurple(),
                                      description=f"No config named `{module}` found")
                await ctx.send(embed=embed)

        with open("configs.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.command(aliases=["setprefix"])
    @commands.is_owner()
    async def changeprefix(self, ctx, *, prefix=None):
        with open("bot.json", "r") as f:
            data = json.load(f)
        if prefix is None:
            return
        else:
            data["prefix"] = prefix
            embed = discord.Embed(colour=discord.Colour.green(), description=f"Prefix set to `{prefix}`")
            embed.set_footer(text="Prefix will work after next restart")
            await ctx.send(embed=embed)
            with open("bot.json", "w") as f:
                json.dump(data, f, indent=4)

    @commands.command(aliases=["botname"])
    @commands.is_owner()
    async def setname(self, ctx, *, nick=None):
        member: discord.Member = self.client.user
        if nick is None:
            nick = self.client.user.name
            await member.edit(nick=nick)
        else:
            await member.edit(nick=nick)
        embed = discord.Embed(colour=discord.Colour.green(),
                              description=f"Bot name has been set to `{nick}`")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def statuschange(self, ctx, *, status):
        with open("bot.json", "r") as f:
            data = json.load(f)
        data["status"] = status
        with open("bot.json", "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(colour=discord.Colour.green(),
                              description=f"Bot status set to `{status}`")

        await ctx.send(embed=embed)



    @commands.command()
    @commands.is_owner()
    async def giveaway(self, ctx, time, *, item):
        await ctx.message.delete()
        embed = discord.Embed(title=f"**__Chaotic Destiny Hosting Giveaway__**", colour=discord.Colour.blue(),
                              description=f'**{item}** \n\n {time} Winners\n ')            
        embed.add_field(name="Requirements : Have a Free Server.", value=f"\u200B", inline=False)
        embed.add_field(name="\u200B", value=f"***React with 🎉 to enter the giveaway!***", inline=False)
        embed.set_footer(text="© Chaotic Destiny Hosting")
        sent = await ctx.send(embed=embed)

        giveaway = '🎉'

        await sent.add_reaction(emoji = "🎉") 
    
    
    @commands.command()
    @commands.is_owner()
    async def evote(self, ctx, *, content):
        channel = self.client.get_channel(712429517137772604)
        up = '✔'
        down = '❌'
        
        await ctx.message.delete()
        embed = discord.Embed(title='New Vote Poll', description = content, color = discord.Colour.dark_red())
        embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        sent = await channel.send(embed = embed) 
        await sent.add_reaction(emoji = "✔") 
        await sent.add_reaction(emoji = "❌")

def setup(client):
    client.add_cog(Staff(client))
