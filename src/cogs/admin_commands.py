import discord
from discord.ext import commands


class AdminCommands(commands.Cog):
    """Commandes réservées aux administrateurs du bot"""

    def __init__(self, bot, admins):
        self.bot = bot
        self.admins = admins
        print("AdminCommands initialised!")

    async def cog_check(self, ctx):
        return ctx.author.id in self.admins

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Cette commande n'est utilisable que par un administarteur du bot (pas du serveur)")
        else:
            await ctx.send("Une erreur imprévue est survenue dans le module AdminCommands")
            raise error

    @commands.command()
    async def list_servers(self, ctx):
        """Liste les serveurs où le bot est présent"""
        message = ""
        guild_text = ""
        async for guild in self.bot.fetch_guilds(limit=None):
            guild_text += "%s (%s)\n" % (guild.id, guild.name)
            if len(guild_text) + len(message) > 2000:
                await ctx.send(message)
                message = ""
            message += guild_text
            guild_text = ""

        await ctx.send(message)
        return
