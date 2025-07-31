import os
import discord
from discord.ext import commands

BAD_WORDS = ["porn", "xxx"]

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='*', intents=intents)
intents = discord.Intents.default()

#############
# Commandes #
#############
@bot.command()
async def bonjour(ctx):
  await ctx.send(f"Salut {ctx.author.name}, ça va ?")

@bot.command()
async def cv(ctx):
  await ctx.send(f"Oe cv & toi {ctx.author.name} ?")

@bot.command(name="quiestla", aliases=["qui_est_la", "who_is_online", "whoisonline"])
async def quiestla(ctx):
    if not ctx.guild:
        await ctx.send("Cette commande doit être utilisée dans un serveur.")
        return

    # S'assurer que les membres sont bien chargés
    if not ctx.guild.chunked:
        try:
            await ctx.guild.chunk()
        except Exception:
            pass

    # Filtrer les membres non-bot qui ne sont pas offline
    online_members = [
        m for m in ctx.guild.members
        if not m.bot and m.status != discord.Status.offline
    ]

    if not online_members:
        await ctx.send("Personne de connecté (hors bots).")
        return

    # Limiter l'affichage à 25 pour éviter trop long
    display_list = ", ".join(m.display_name for m in online_members[:25])
    more = f" et {len(online_members)-25} de plus..." if len(online_members) > 25 else ""
    await ctx.send(f"En ligne : {display_list}{more}")

##############
# Evenements #
##############

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