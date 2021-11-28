import discord
from discord.ext import commands

from time import sleep
import json
import re

from custom_utilities import *
import resources
import metalol
import cogs

bot = commands.Bot(command_prefix=resources.config["prefix"])


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

ravaged_regexes = [
    r"ouais? ?gros?",
    r"oo+k",
    r"o+u+[kh]",
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
        counted = resources.counts.keys()
        for word in counted:
            if word in msg.content:
                resources.counts[word] += 1

        resources.write("counts")

    await bot.process_commands(msg)


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


@bot.command(aliases=['bagar'])
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
        await toggle_role(ctx.author, server_roles["AmongUs"]["CrewLink"])
        await ctx.send("Toggled role: CrewLink")
    else:
        await ctx.send("Cette commande ne fonctionne que sur le serveur AmongUs!")


@bot.command()
async def count(ctx: commands.Context, arg):
    if ctx.guild.id == server_ids["Caverne"]:
        resources.reload("counts")
        # TODO print a list of counted expressions if no argument is given
        if arg in resources.counts.keys():
            await ctx.send(f"\"{arg}\" a été dit {resources.counts[arg]} fois sur la Caverne")
        else:
            resources.counts[arg] = 0
            resources.write("counts")
            await ctx.send(f"Les \"{arg}\" sont désormais comptés!")

if __name__ == "__main__":
    print("Loading cogs...")
    bot.add_cog(cogs.Jukebox(bot))
    bot.add_cog(cogs.Caverne(bot))
    bot.add_cog(cogs.AdminCommands(bot, resources.config["administrators"]))
    print("Cogs loaded!")
    print("Launching bot...")
    bot.run(resources.config["token"])
