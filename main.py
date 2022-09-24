from urllib.request import urlopen
import discord
import os
import spotipy

from discord.ext import commands
from discord import Member
from discord import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='$', case_insensitive=True)
bot.remove_command("help")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"))
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='liaozhu.herokuapp.com/'))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Spotify"))
    
@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title = "List of Commands",
        color = 0x90EE90
    )     
    embed.add_field(name="$current/playing/song", value="returns song currently playing", inline=False)
    embed.add_field(name="$search + song + songTitle", value="returns song searched", inline=False)
    embed.add_field(name="$search + album + albumTitle", value="returns album searched", inline=False)
    embed.add_field(name="$search + artist + artistName", value="returns artist searched", inline=False)
    await ctx.channel.send(embed=embed)

@bot.command(name="hello", aliases=["hi", "hey"])
async def hello(ctx):
  await ctx.channel.send("hello")
  
@bot.command(name="current", aliases=["playing", "song"])
async def current(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
        pass
      
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed = discord.Embed(
                    title = f"{user.name}'s Current Song",
                    description = "Listening to {}".format(activity.title),
                    color = 0x90EE90
                )
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("Not playing anything, please make sure Spotify is connected")

    else:
        await ctx.channel.send("Not playing anything, please make sure Spotify is connected")

@bot.command(name="spotify", aliases=["profile", "account", "user", "me"])
async def spotify(ctx, *, username=None):
    if username == None:
        username = ctx.author.name
        await ctx.channel.send("Searching for account with username: " + f"{username}")
        pass
    
    try:
        user = sp.user(f"{username}")
        
        embed = discord.Embed(
            title = user["display_name"],
            color = 0x90EE90)
        try:
            embed.set_thumbnail(url=user['images'][0]['url'])
        except:
            print("no image found")
            
        embed.add_field(name="View Profile: ", value=user["external_urls"]["spotify"], inline=False)
        embed.add_field(name="Followers: ", value=f"{user['followers']['total']}", inline=False)
        playlists = sp.user_playlists(f"{username}")
        while playlists:
            embed.add_field(name="User Playlists", value="Showing public playlists by " + f"{username}", inline=False)
            for i, playlist in enumerate(playlists['items']):
                embed.add_field(name="\u200b", value=f"{i + 1 + playlists['offset']}: {playlist['name']} {playlist['external_urls']['spotify']}", inline=False)
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None

        await ctx.channel.send(embed=embed)
        
    except:
        await ctx.channel.send("No User Found With Username: " + f"{username}")
    
@bot.command()
async def search(ctx, typeSearch=None, *, title=None):
    if title == None or typeSearch == None:
        await ctx.channel.send("Please do: $search + 'type of search' + 'title of song/album' in order to search for a track")
        return
    
    if typeSearch == "song":
        song = sp.search(f"{title}", limit=1, type="track")
        try:
            embed = discord.Embed(
                color = 0x90EE90
            )
            embed.add_field(name="Title", value=song['tracks']['items'][0]['name'], inline=False)
            embed.add_field(name="Open", value=song['tracks']['items'][0]['external_urls']['spotify'], inline=False)
            embed.add_field(name="Album", value=song['tracks']['items'][0]['album']['name'], inline=False)
            embed.set_thumbnail(url=song['tracks']['items'][0]['album']['images'][0]['url'])
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send("Could not find song: " + f"{title}")
            
    elif typeSearch == "album":
        album = sp.search(q=f"{title}", type="album", limit=1)
        tracks = sp.search(q=f"{title}", limit=6)
        try: 
            embed = discord.Embed(
                color = 0x90EE90
            )
            embed.add_field(name="Title", value=album['albums']['items'][0]['name'], inline=False)
            embed.add_field(name="Open", value=album['albums']['items'][0]['external_urls']['spotify'], inline=False)
            embed.add_field(name="Artist", value=album['albums']['items'][0]['artists'][0]['name'], inline=False)
            embed.set_thumbnail(url=album['albums']['items'][0]['images'][0]['url'])
            embed.add_field(name="Release Date", value=album['albums']['items'][0]['release_date'])
            embed.add_field(name="Top 5 Tracks", value="\u200b", inline=False)
            for idx, track in enumerate(tracks['tracks']['items'][1:]):
                embed.add_field(name=f"{idx + 1}", value=track['name'], inline=False)
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send("Could not find album: " + f"{'album'}")
    
    elif typeSearch == "artist":
        artist = sp.search(q=f"{title}", type="artist")
        albums = sp.search(q=f"{title}", type="album", limit=6)
        try:
            embed = discord.Embed(
                title = artist['artists']['items'][0]['name'],
                color = 0x90EE90
            )
            embed.set_thumbnail(url=artist['artists']['items'][0]['images'][0]['url'])
            embed.add_field(name="Followers: ", value=artist['artists']['items'][0]['followers']['total'], inline=False)
            embed.add_field(name="Artist Profile: ", value=artist['artists']['items'][0]['external_urls']['spotify'], inline=False)
            embed.add_field(name="Top Albums", value="\u200b", inline=False)
            for idx, album in enumerate(albums['albums']['items'][1:]):
                embed.add_field(name=f"{idx + 1}", value=f"{album['name']} {album['external_urls']['spotify']}", inline=False)
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send("No artist found with name: " + f"{artist}")
 
bot.run(os.environ.get('TOKEN'))