from discord.ext import commands
import discord
import json
import resources

bot = commands.Bot(command_prefix=resources.config["prefix"])

protected_roles = [567478735356297226,  # Meilleur admin de tous les temps
                   572564528173285376,  # Pour que le bot puisse travailler
                   482292815166963714,  # poto
                   569953389970980870,  # Golems
                   524347357475897364,  # Rythm
                   420305560835981324,  # MathBot
                   572354706337300480,  # Mee6
                   638860564830879764,  # Mantaro
                   736863922111381556,  # Bienvenue
                   343694718879924235]  # Everyone


@bot.event
async def on_ready():
    print("Ready to go!")
    print("Cleaning done!")

@bot.command()
async def clear_permissions(ctx):
    guild = discord.utils.find(lambda guild: guild.id == 343694718879924235, bot.guilds)
    for role in guild.roles:
        if not (role.id in protected_roles):
            await role.edit(permissions=discord.Permissions(0), reason="Suppression des droits inutiles")

bot.run(resources.config["token"])
