import os
import discord
from discord.ext import commands

async def start_bot():
    while True:
        try:
            bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
            @bot.event
            async def on_ready():
                print("Bot has connected to Discord!")
                bot.loop.create_task(process_queue())

@bot.command()
async def info(ctx: commands.Context):
    message = "test_command"
    await ctx.send(content=message, ephemeral=True)


await bot.start(TOKEN)
        except Exception as e:
            print(f"Error: {e}")
            await bot.close()
