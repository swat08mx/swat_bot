import discord
from replit import db
import os
import asyncio
import youtube_dl
from keep_alive import keep_alive



TOKEN = "MTAxMTI5NDI0MTM3MDE1Mjk5MA.GZ24s_.tGOxko32Qgo7sFuzn3Fjnp-dXNRr1TRAjNuDBI"

client = discord.Client(intents = discord.Intents().all())

blocked_words = ["nigger", "faggot", "fuck"]

swatsname = ["swat"]

voice_clients =  {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {'options': '-vn'}

@client.event
async def on_ready():
  print(f"You have logged in as {client.user}")

def addition(num, num_o):
    add = num + num_o
    return add

@client.event
async def on_message(mesg):
  if mesg.author != client.user:
      if mesg.content.lower().startswith("-hi"):
          await mesg.channel.send(f"Hi, {mesg.author.display_name}")
          
      elif mesg.content.startswith("-play "):
            
            try:
               voice_client = await mesg.author.voice.channel.connect()
               voice_clients[voice_client.guild.id] = voice_client
            except:
              print("error")
            
            try:
              url = mesg.content.split()[1]
              
              
              
              loop = asyncio.get_event_loop()
              data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))
              
              song = data['url']
              player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\Program Files\\ffmpeg\\ffmpeg.exe")
              
              voice_client.play(player)
              
            except Exception as err:
              print(err)
              
      elif mesg.content.startswith("-pause"):
            try:
              voice_clients[mesg.guild.id].pause()
            except Exception as err:
              print(err)
      elif mesg.content.startswith("-resume"):
            try:
              voice_clients[mesg.guild.id].resume()
            except Exception as err:
              print(err)
      elif mesg.content.startswith("-stop"):
            try:
              voice_clients[mesg.guild.id].stop()
              await voice_clients[mesg.guild.id].disconnect()
            except Exception as err:
              print(err)
              
              #and text in str(mesg.content.lower())
  
  if "Verified" in str(mesg.author.roles):
    if mesg.content.lower() in blocked_words:
      await mesg.delete()
      print("Message deleted....")
      await mesg.channel.send(f"Hi {mesg.author.display_name}, please dont use banned words")
      return      

keep_alive()
client.run(TOKEN)
            



