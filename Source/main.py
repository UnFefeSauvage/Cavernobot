import discord
from discord.ext import commands
import DiscordUtils

from time import sleep
import json
import re

from custom_utilities import *
import resources
import metalol

bot = commands.Bot(command_prefix=resources.config["prefix"])

music = DiscordUtils.Music()

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
        #TODO print a list of counted expressions if no argument is given
        if arg in resources.counts.keys():
            await ctx.send(f"\"{arg}\" a été dit {resources.counts[arg]} fois sur la Caverne")
        else:
            resources.counts[arg] = 0
            resources.write("counts")
            await ctx.send(f"Les \"{arg}\" sont désormais comptés!")

@bot.command(aliases=['connecter'])
async def join(ctx):
    await ctx.author.voice.channel.connect() #Joins author's voice channel

@bot.command(aliases=['fuckoff', 'zou', 'tagueule', 'tg'])
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(aliases=['p', 'joue', 'jouer'])
async def play(ctx, *, url):
    # Si aucun argument n'est fourni, 'play' signifie 'reprendre'    
    if not url:
        resume(ctx)
        return

    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"En train de jouer: {song.name}")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Ajouté à la queue: {song.name}")
    
@bot.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send("Musique mise en pause!")

@bot.command(aliases=['reprendre'])
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"On reprend {song.name}")

@bot.command()
async def stop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    await ctx.send("Yeet")

@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send("Bienvenue à Minas Morghul, la cité des morts!")
    else:
        await ctx.send("Bravo! Vous êtes sorti de votre boucle temporelle!")

@bot.command(aliases=['q'])
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send('\n'.join([f"{i}. {song.name}" for i, song in enumerate(player.current_queue())]))

@bot.command(aliases=['np'])
async def now_playing(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(f"En train de jouer {song.name}")

@bot.command(aliases=['s'])
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    await ctx.send(f"\"{data[0].name}\" a été yeet.")

@bot.command(aliases=['v'])
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(int(vol) / 100)) # volume should be a float between 0 to 1
    await ctx.send(f"Volume à {volume*100}% capitaine!")

@bot.command(aliases=['gerte','r'])
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue")


if __name__ == "__main__":
    bot.run(resources.config["token"])
