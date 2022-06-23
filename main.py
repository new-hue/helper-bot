import discord
from discord.ext import commands
import random
import asyncpraw
import math
import os
import keep_alive
# IMAGE EDITING
from PIL import Image, ImageOps
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import numpy as np
from io import BytesIO
from datetime import datetime
from pytz import timezone
import requests
# initialize the discord client.
bot = discord.Client()
# set the bots prefix
bot = commands.Bot(command_prefix=['matt ','Matt ','matt','Matt'])
bot.remove_command('help')
#print on connect to discord
@bot.event
async def on_connect():
    print("Connected to Discord as:", bot.user.name)
# sets the color of message embeds
DCOLOR=0x006eff
# commands
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Help", description="This bot helps you learn how to program! Here is a list of the commands! \n Commands: \n `matt embed` \n `matt RNG` \n `matt meme`\n `matt invite` \n `matt floor <message>` \n `matt code` \n `matt tweet <message>`", color=DCOLOR)
    await ctx.send(embed=embed)


@bot.command()
async def embed(ctx):
    embed=discord.Embed(title="Embed", description="This is an embed! to see how to make one click [here](https://bit.ly/3mzmCcj)", color=DCOLOR)
    await ctx.send(embed=embed)

@bot.command()
async def RNG(ctx):
 
   # checks the author is responding in the same channel
   # and the message is able to be converted to a positive int
   def check(msg):
       return msg.author == ctx.author and msg.content.isdigit() and \
              msg.channel == ctx.channel
 
   await ctx.send("Type a number")
   msg1 = await bot.wait_for("message", check=check)
   await ctx.send("Type a second, larger number")
   msg2 = await bot.wait_for("message", check=check)
   x = int(msg1.content)
   y = int(msg2.content)
   if x < y:
       value = random.randint(x,y)
       await ctx.send(f"You got {value}. To see how this works click the link:\n<https://bit.ly/3w5K5om>")  
   else:
       await ctx.send(":warning: Please ensure the first number is smaller than the second number.")

@bot.command()
async def meme(ctx):
  url = "https://meme-api.herokuapp.com/gimme"
  resp = requests.get(url)
  result = resp.json()
  embed=discord.Embed(title=result["title"], url=result["postLink"], color=DCOLOR)
  embed.set_image(url=result["url"])
  await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    embed=discord.Embed(title="Invite the Bot", description="You can invite the bot [here](https://discord.com/api/oauth2/authorize?client_id=903738470600704042&permissions=377957239872&scope=bot)", color=DCOLOR)
    await ctx.send(embed=embed)

@bot.command()
async def floor(ctx, *, text):
    pfp = Image.open(requests.get(ctx.author.avatar_url, stream=True).raw)

    img = Image.open("floor.png")
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("REFSANB.ttf", 40)
    draw.text((280,30), text, font=fnt, fill=(255,255,255,0))
    pfp = pfp.resize((20, 20), Image.ANTIALIAS)
    img.paste(pfp, (125,125))
    pfp = pfp.resize((50, 50), Image.ANTIALIAS)
    img.paste(pfp, (410,125))
    img.save('floor-out.png')
    await ctx.send(file=discord.File('floor-out.png'))


@bot.command(name='tweet')
async def tweet(ctx, *, text):
  if len(text) <= 360:
    asset = ctx.author.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    img=Image.open(data).convert("RGB")
    npImage=np.array(img)
    h,w=img.size
    
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)
    npAlpha=np.array(alpha)
    npImage=np.dstack((npImage,npAlpha))
    pfp = Image.fromarray(npImage)

    img = Image.open("basetweet.png")
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("REFSANB.ttf", 18)
    font2 = ImageFont.truetype("chirp.ttf", 15)
    font3 = ImageFont.truetype("chirp.ttf", 23)
    font4 = ImageFont.truetype("chirp.ttf", 17)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((90, 18),ctx.author.name,(15, 20, 25),font=font)
    draw.text((105, 36),ctx.author.name,(83, 100, 113),font=font2)
    draw.rectangle(((0, 100,), (743, 360)),fill="#ffffff")
    tz = timezone('EST')
    timee = datetime.now(tz).strftime('%H:%M · %D')
    draw.text((10, 340),f"{timee} · Helper Bot",(83, 101, 113),font=font4)
    margin = 20 
    offset = 80
    for line in textwrap.wrap(text, width=70):
      draw.text((margin, offset), line, font=font3, fill="#000000")
      offset += 28 
      #font.getsize(line)[1] + 15
    # draw.text((20, 80),text,(0,0,0),font=font3)
    # (20, 80),text,(0,0,0),font=font3
    pfp2 = pfp.resize((60, 60), Image.ANTIALIAS)
    img.paste(pfp2, (15,15), pfp2)
    img.save('tweet-out.png')
    await ctx.send(file=discord.File('tweet-out.png'))
  else:
    embed = discord.Embed(title=f"Tweet Error",description=f"You cannot use more than 160 characters in your tweet! You are {len(text) - 160} character over the limit!", color=DCOLOR)
    await ctx.send(embed=embed)



keep_alive.keep_alive()
# ACTUALLY logs the bot in
bot.run('YOU THOUGHT!')
