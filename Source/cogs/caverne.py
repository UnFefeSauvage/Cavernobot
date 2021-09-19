import discord
from discord.ext import commands

class DeactivatedCommand(Exception):
    """This command has been deactivated"""
    pass

class Caverne(commands.Cog):
    """Commandes disponibles uniquement sur la Caverne"""
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 343694718879924235
        self.protected_roles = [567478735356297226,  # Meilleur admin de tous les temps
                                572564528173285376,  # Pour que le bot puisse travailler
                                482292815166963714,  # poto
                                569953389970980870,  # Golems
                                524347357475897364,  # Rythm
                                420305560835981324,  # MathBot
                                572354706337300480,  # Mee6
                                638860564830879764,  # Mantaro
                                736863922111381556,  # Bienvenue
                                343694718879924235]  # Everyone
        self.deactivated_commands = []
        print("Caverne initialised!")

    async def cog_check(self, ctx):
        if ctx.command in self.deactivated_commands and ctx.message.content[:5] != f'{self.bot.command_prefix}help':
            await ctx.send("Désolé, cette commande a été désactivée le temps de la débugger :(")
            raise DeactivatedCommand()
        return ctx.guild.id == self.guild_id
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error,commands.CheckFailure):
            await ctx.send("Cette commande n'est utilisable que sur la Caverne, mon serveur de naissance...")
        else:
            await ctx.send("Une erreur imprévue est survenue... Si vous tapez mon créateur assez fort ça devrait bientôt remarcher!")
            raise error

    @commands.command()
    async def clear_permissions(self, ctx):
        """Enlève les droits inutiles des rôles décoatifs"""
        await ctx.send("Début du nettoyage...")
        guild = ctx.guild
        cleaned_roles = 0
        for role in guild.roles:
            if not (role.id in self.protected_roles):
                if role.permissions.value != 0:
                    cleaned_roles += 1
                    await role.edit(permissions=discord.Permissions.none(), reason="Suppression des droits inutiles")
                    await ctx.send("Permissions du rôle **" + str(role) + "** nettoyées!")

        await ctx.send(f"Nettoyage terminé! Rôles nettoyés: {cleaned_roles}")
