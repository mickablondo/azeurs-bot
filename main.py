import os
import discord
from discord.ext import commands

BAD_WORDS = ["porn", "xxx"]

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

@bot.event
async def on_message(message: discord.Message):
    # On ignore les messages envoyés par le bot lui-même => très important sinon on va créer une boucle infinie
    if message.author.bot:
        return
    # await message.channel.send(f"{message.author.name} vient d'écrire {message.content}")
  
    # antispam
    content_lower = message.content.lower()
    if "https://" in content_lower and any(bad in content_lower for bad in BAD_WORDS):
      try:
          await message.delete()
          await message.channel.send(f"⚠️ {message.author.mention}, lien avec contenu interdit supprimé.")
      except discord.Forbidden:
          # pas les droits
          pass
      except discord.HTTPException:
          # échec de suppression
          pass

    await bot.process_commands(message)

token = os.environ['TOKEN_BOT_DISCORD']
bot.run(token)