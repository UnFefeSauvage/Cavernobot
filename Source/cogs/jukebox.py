from discord.ext import commands
import DiscordUtils.music as music

class JukeboxError(Exception):
    """Something went wrong with the Jukebox and we know what"""

class Jukebox(commands.Cog):
    """Commandes permettant de m'utiliser comme bot musique"""
    def __init__(self, bot):
        self.bot = bot
        self.jukebox = music.Music()
        print("Jukebox initialised!")
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        
        if isinstance(error, JukeboxError):
            await ctx.send(str(error))
        elif isinstance(error, music.NotPlaying):
            await ctx.send("Je ne suis pas en train de jouer de la musique!")
        elif isinstance(error, music.EmptyQueue):
            await ctx.send("La queue est vide!")
        elif isinstance(error, music.NotConnectedToVoice):
            await ctx.send("Je ne suis pas dans un canal vocal! Connectes moi avec `=join` avant de lancer une musique!")
        else:
            await ctx.send("Désolé, une erreur inconnue est survenue dans le module Jukebox :(")
            raise error

    @commands.command(aliases=['connect'])
    async def join(self, ctx):
        """Envoie le Cavernobot dans ton canal vocal"""
        try:
            await ctx.author.voice.channel.connect() #Joins author's voice channel
        except AttributeError:
            raise JukeboxError("Tu dois être dans un canal vocal pour m'y connecter!")

    @commands.command(aliases=['fuckoff', 'zou', 'tagueule', 'tg'])
    async def leave(self, ctx):
        """Déconnecte le Cavernobot du canal"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        if player:
            await player.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("Yeet")
    
    @commands.command(aliases=['p', 'joue', 'jouer'])
    async def play(self, ctx, *, url):
        """Joues ou ajoutes une musique à la queue"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)


        if not player:
            player = self.jukebox.create_player(ctx, ffmpeg_error_betterfix=True)

        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True, allow_generic_file=True)
            #TODO Resume the current song if there is one
            song = await player.play()
            await ctx.send(f"En train de jouer: {song.name}")
        else:
            song = await player.queue(url, search=True, allow_generic_file=True)
            await ctx.send(f"Ajouté à la queue: {song.name}")
    
    @commands.command()
    async def pause(self, ctx):
        """Mets la musique actuelle en pause"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        if player is None:
            raise music.NotPlaying("Je ne joue pas de musique!")
        song = await player.pause()
        await ctx.send("Musique mise en pause!")

    @commands.command(aliases=['reprendre'])
    async def resume(self, ctx):
        """Reprends la musique que tu écoutais"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        if player is None:
            raise music.NotPlaying("Je ne joue pas de musique!")
        song = await player.resume()
        await ctx.send(f"On reprend {song.name}")

    @commands.command()
    async def stop(self, ctx):
        """Arrête la musique et vide la queue"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        if player is None:
            raise music.NotPlaying("Je ne joue pas de musique!")
        await player.stop()
        await ctx.send("Yeet")

    @commands.command()
    async def loop(self, ctx):
        """Actives ou désactives le tourbillon des enfers"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        if player is None:
            raise music.NotPlaying("Je ne joue pas de musique!")
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send("*\"Boule qui roule tourne en rond.\" -Rémy (je crois)*")
        else:
            await ctx.send("Et on arrête le manège!")

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        """Affiches la queue sur le point d'être jouée"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        if player is None:
            raise music.NotPlaying("Je ne joue pas de musique!")
        queue = player.current_queue()
        message = f'```python\n@ EN COURS DE LECTURE: {queue[0].name}\n\n@ MUSIQUES SUIVANTES:'
        for i in range(1,len(queue)):
            song = queue[i]
            message += f'\n{i}) {song.name} -- {int(song.duration//60)}:{int(song.duration%60)}'
        message += '\n```'
        await ctx.send(message)

    @commands.command(aliases=['np'])
    async def now_playing(self, ctx):
        """Vois ce qui est en train d'être joué"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send(f"En train de jouer {song.name}")

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        """Passes à la musique suivante"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        if player is None:
            raise music.NotPlaying("Cannot skip because nothing is being played!")
        data = await player.skip(force=True)
        await ctx.send(f"\"{data[0].name}\" a été yeet. Passage à la musique suivante.")

    @commands.command(aliases=['v'])
    async def volume(self, ctx, vol):
        """Changes le volume avec une valeur entre 0 et 100"""
        vol = min(max(0,int(vol)), 300)
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(vol / 100)) # volume should be a float between 0 to 1
        await ctx.send(f"Volume à {vol}% capitaine!")

    @commands.command(aliases=['gerte','r'])
    async def remove(self, ctx, index):
        """Enlèves la musique d'index indiqué de la file"""
        player = self.jukebox.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await ctx.send(f"Removed {song.name} from queue")