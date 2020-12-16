from discord.ext import commands
from custom_utilities import *
import discord
import json
import resources
import re
from time import sleep
import metalol

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

server_ids = {
    "Caverne": 343694718879924235,
    "AmongUs": 770412313277628417
}

server_roles = {
    "Caverne": {},
    "AmongUs": {
        "CrewLink": 786986614987292683
    }
}

unused_roles = []

ravaged_regexes = [
    r"ouais? ?gros?",
    r"oo+k",
    r"o+u+k",
    r"o+u+h",
    r"🗿",
    r"monkey",
    r"ouga",
    r"bouga",
    r"🦍",
    r"🐒",
    r"piou|pew",
    r"🤙",
    r"🥰",
    r"(HA){2}",
    r"crack",
    r"rah",
    r"empereur",
    r"alka?pote?",
    r"kaaris",
    r"bouillave",
    r"tennis",
    r"ravag*",
    r"G.{2,6}G",
    r"/.{2,6}\\"
]

compiled_ravaged_regexes = []

@bot.event
async def on_ready():
    print("Compiling regexes...")
    for regex in ravaged_regexes:
        print("compiling " + regex)
        compiled_ravaged_regexes.append(re.compile(regex, flags=re.IGNORECASE))
    print("Ready to go!")


@bot.command()
async def list_unused_roles(ctx):
    guild = discord.utils.find(lambda guild: guild.id == 343694718879924235, bot.guilds)
    message = "> Unused roles:\n"
    for role in guild.roles:
        if not (role.id in protected_roles):
            number_of_members = 0
            for member in guild.members:
                if role in member.roles:
                    number_of_members += 1
            if number_of_members == 0:
                message += "**" + str(role) + "**" + "\n"
                unused_roles.append(role)
    await ctx.send(message)


@bot.command()
async def delete_unused_roles(ctx):
    global unused_roles
    message = "This will delete the following roles:\n"
    for role in unused_roles:
        message += "**" + str(role) + "**" + "\n"
    await ctx.send(message)

    for role in unused_roles:
        await role.delete()
    unused_roles = []
    await ctx.send("Roles deleted!")


@bot.command()
async def clear_permissions(ctx):
    guild = discord.utils.find(lambda guild: guild.id == 343694718879924235, bot.guilds)
    for role in guild.roles:
        if not (role.id in protected_roles):
            if role.permissions.value != 0:
                await role.edit(permissions=discord.Permissions.none(), reason="Suppression des droits inutiles")
                await ctx.send("Cleared permissions of **" + str(role) + "**")

    await ctx.send("Done!")


@bot.command()
async def ravagerie(ctx):
    ravaged_score = 0
    async for msg in ctx.channel.history(limit=500):
        for regex in compiled_ravaged_regexes:
            if re.search(regex, msg.content):
                ravaged_score += 1
    ravaged_score *= 1
    await ctx.send("Ce channel est ravagé à " + str(ravaged_score) + "%")

@bot.command()
async def ban(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/459632261508235264/744966051187392562/image0.jpg")

@bot.command()
async def fight(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/435380743598899201/486932499650314241/image0.png")

@bot.command()
async def lol(ctx):
    await ctx.send(metalol.create_meta())

@bot.command()
async def crewlink(ctx):
    if ctx.channel.guild.id == server_ids["AmongUs"]:
        await toggle_role(ctx.author,server_roles["AmongUs"]["CrewLink"])
        await ctx.send("Toggled role: CrewLink")
    else:
        await ctx.send("Tu n'es pas sur le serveur Among Us. (Ou on m'a codé comme un pied")


if __name__ == "__main__":
    bot.run(resources.config["token"])
