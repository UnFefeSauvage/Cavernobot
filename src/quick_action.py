from discord.ext import commands
from custom_utilities import *
import discord
import json
import resources
import re
from time import sleep
import metalol

bot = commands.Bot(command_prefix=resources.config["prefix"])

server_ids = {
    "Caverne": 343694718879924235,
    "AmongUs": 770412313277628417
}

channel_ids = {
    "nouvel-an": 763379872465813504
}


@bot.event
async def on_ready():
    print("Connected!")
    # * ACTIONS A EFFECTUER
    caverne = discord.utils.find(
        lambda guild: guild.id == server_ids["Caverne"], bot.guilds)


bot.run(resources.config["token"])
