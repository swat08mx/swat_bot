import discord
from replit import db
import os
import asyncio
import youtube_dl
from keep_alive import keep_alive



TOKEN = "MTAxMTI5NDI0MTM3MDE1Mjk5MA.G8nXw3.7_WyLOvv-JU_D2dQWzwGC8vN8Fbb6PgN697y8E"

client = discord.Client(intents = discord.Intents().all())

blocked_words = ['dumb']

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
      elif mesg.content.startswith("orf"):
            string = input(await mesg.channel.send("Enter a string: "))
            target = input("Enter a target: ")
            m=0
            for i in range(len(string)-1):
              count=0
              if target[m]==string[i]:
                k=i
                for j in range(len(target)):
                  if target[j]==string[k]:
                    count+=1
                    k+=1
                  if count==len(target):
                    index=k-count
                    print(f"The pattern was found at {index+1}")
  for texts in swatsname:
        if texts in str(mesg.content.lower()):
              print("Your name was used")
  for text in blocked_words:
    if "sebastian" not in str(mesg.author.roles) and text in str(mesg.content.lower()):
      await mesg.delete()
      print("Message deleted....")
      await mesg.channel.send(f"Hi {mesg.author.display_name}, Do not use banned words")
      return

keep_alive()
client.run(TOKEN)
