import nextcord
from nextcord.ext import commands
import json

#Import command cogs.
#Cogs are just a way to organize commands in nextcord. Read more about them here: https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
from asuka_math import Math
from general import General

#Instatiate bot and set command prefix.
bot = commands.Bot(command_prefix="&")

#Add commands to bot in the form of cogs.
bot.add_cog(Math(bot))
bot.add_cog(General(bot))

#Read the bot token in from external JSON.
with open("creds/creds.json") as credfile:
    creds = json.load(credfile)
    bot.run(creds["token"])
