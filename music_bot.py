import os

from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix='!')
players = {}


@client.event
async def on_ready():
  print("Bot online")


@client.command()
async def join(ctx):
  channel = ctx.message.author.voice.channel
  voice = get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()


@client.command()
async def play(ctx, url):
  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
  FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
  }
  voice = get(client.voice_clients, guild=ctx.guild)

  try:
    if not voice.is_playing():
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
      URL = info['url']
      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      voice.is_playing()
      await ctx.send('Bot is ready!')

    else:
      await ctx.send('Bot is already playing')
      return
  except:
    await ctx.send('I must join a voice channel to play music. Use !join.')


@client.command()
async def resume(ctx):
  voice = get(client.voice_clients, guild=ctx.guild)

  if not voice.is_playing():
    voice.resume()
    await ctx.send('Bot is resuming')


@client.command()
async def pause(ctx):
  voice = get(client.voice_clients, guild=ctx.guild)

  if voice.is_playing():
    voice.pause()
    await ctx.send('Stopping...')


@client.command()
async def exit(ctx):
  voice = get(client.voice_clients, guild=ctx.guild)

  if voice.is_playing():
    voice.disconnect()
    await ctx.send('Bye :wave:')

client.run(os.getenv('TOKEN'))
