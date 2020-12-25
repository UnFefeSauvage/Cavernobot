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
    r"monkey|monki",
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
        compiled_ravaged_regexes.append(re.compile(regex))
    print("Done!")
    print("Ready to go!")

@bot.event
async def on_message(msg: discord.Message):
    if (not msg.author.bot) and (msg.guild.id == server_ids["Caverne"]):
        print(resources.counts)
        counted = resources.counts.keys()
        for word in counted:
            if word in msg.content:
                resources.counts[word] += 1
        
        resources.write("counts")

    await bot.process_commands(msg)

@bot.command()
async def list_unused_roles(ctx):
    """ Liste tous les rôles non utilisés ET non essentiels de la Caverne """
    if ctx.guild.id == server_ids["Caverne"]:
        guild = ctx.guild
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
    else:
        await ctx.send("Cette commande n'est utilisable que sur la Caverne!")


@bot.command()
async def delete_unused_roles(ctx):
    """ Supprime les derniers rôles listés par "list_unused_roles" """
    global unused_roles
    if ctx.guild.id == server_ids["Caverne"]:
        message = "This will delete the following roles:\n"
        for role in unused_roles:
            message += "**" + str(role) + "**" + "\n"
        await ctx.send(message)

        for role in unused_roles:
            await role.delete()
        unused_roles = []
        await ctx.send("Roles deleted!")
    else:
        await ctx.send("Cette commande n'est utilisable que sur la Caverne!")


@bot.command()
async def clear_permissions(ctx):
    """ Enlève les droits inutiles des rôles sur la Caverne """
    if ctx.guild.id == server_ids["Caverne"]:
        guild = ctx.guild
        for role in guild.roles:
            if not (role.id in protected_roles):
                if role.permissions.value != 0:
                    await role.edit(permissions=discord.Permissions.none(), reason="Suppression des droits inutiles")
                    await ctx.send("Cleared permissions of **" + str(role) + "**")

        await ctx.send("Done!")
    else:
        await ctx.send("Cette commande n'est utilisable que sur la Caverne!")



@bot.command()
async def ravagerie(ctx):
    """Évalue pour vous le niveau de ravagerie d'un salon de discussion, vous évitant ainsi une ravagerie surprise!"""
    ravaged_score = 0
    alert_msg = await ctx.send("Processing messages...")
    async for msg in ctx.channel.history(limit=501):
        for regex in compiled_ravaged_regexes:
            if re.search(regex, msg.content):
                ravaged_score += 1
    ravaged_score *= 1
    await alert_msg.delete()
    await ctx.send("Ce channel est ravagé à " + str(ravaged_score) + "%")

@bot.command()
async def ban(ctx):
    """Bobo senpai..."""
    await ctx.send("https://cdn.discordapp.com/attachments/459632261508235264/744966051187392562/image0.jpg")

@bot.command()
async def fight(ctx):
    """Stéphane Burnes wants to know your location"""
    await ctx.send("https://cdn.discordapp.com/attachments/435380743598899201/486932499650314241/image0.png")

@bot.command()
async def lol(ctx):
    """Des pépites de sagesse pour up votre ranking dans la ligue des légendes"""
    await ctx.send(metalol.create_meta())

@bot.command()
async def crewlink(ctx):
    """Vous donne le rôle CrewLink (Serveur AmongUs uniquement)"""
    if ctx.channel.guild.id == server_ids["AmongUs"]:
        await toggle_role(ctx.author,server_roles["AmongUs"]["CrewLink"])
        await ctx.send("Toggled role: CrewLink")
    else:
        await ctx.send("Cette commande ne fonctionne que sur le serveur AmongUs! (")

@bot.command()
async def count(ctx: commands.Context, arg):
    if ctx.guild.id == server_ids["Caverne"]:
        resources.reload("counts")
        if arg in resources.counts.keys():
            await ctx.send(f"\"{arg}\" a été dit {resources.counts[arg]} fois sur la Caverne")
        else:
            resources.counts[arg] = 0
            resources.write("counts")
            await ctx.send(f"Les \"{arg}\" sont désormais comptés!")


if __name__ == "__main__":
    bot.run(resources.config["token"])
