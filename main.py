import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
intents = discord.Intents.default()

@bot.command()
async def bonjour(ctx):
  await ctx.send(f"Salut {ctx.author.name}, ça va ?")

@bot.command()
async def cv(ctx):
  await ctx.send(f"Oe cv & toi {ctx.author.name} ?")

token = os.environ['TOKEN_BOT_DISCORD']
bot.run(token)