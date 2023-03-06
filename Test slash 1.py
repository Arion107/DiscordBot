import discord
from discord import Intents, File
from discord.ext import commands
from discord import app_commands
from io import BytesIO
import base64
import asyncio
from keep_alive import keep_alive

intents = Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)
tree = app_commands.CommandTree(bot)
guildsList = []

queue = []
users = {}


async def check_command_limit(interaction: discord.Interaction):
    user = interaction.author
    if isinstance(interaction.channel, discord.DMChannel):  # Deshabilitar comando en mensajes privados
        return False
    if "AI" in [role.name for role in user.roles]:
        return True
    if user.id in users and users[user.id] >= 25:
        await interaction.response.send_message(
            f"{user.mention}, Your free dreams have come to an end. Please consider subscribing to one of our plans.To see more details, use the /subscribe command or visit our website at https://mee6.gg/m/thedream",
            ephemeral=True)
        return False
    return True


def increment_user_command_count(interaction: discord.Interaction):
    user = interaction.author
    if user.id in users:
        users[user.id] += 1
    else:
        users[user.id] = 1
    with open('command_count.txt', 'w') as f:
        for user_id, count in users.items():
            f.write(f"{user_id}:{count}\n")


async def generate_dream(interaction: discord.Interaction, task: str):
    try:
        img_data = generateToken64(task)
        decoded_bytes = base64.b64decode(img_data[0])
        image = BytesIO(decoded_bytes)
        await interaction.response.send_message(f" **{task}** - {interaction.author.mention}",
                                                file=File(image, "dream.png"))
    except Exception as e:
        await interaction.response.send_message(
            f"{interaction.author.mention}, The bot is having technical problems, in a few moments it will be operational again.",
            ephemeral=True)
        print(e)


async def process_queue():
    while True:
        if queue:
            interaction, task = queue.pop(0)
            print(f"Processing task '{task}'...")
            if await check_command_limit(interaction):
                increment_user_command_count(interaction)
                await generate_dream(interaction, task)
        await asyncio.sleep(1)


async def start_bot():
    while True:
        try:
            with open('command_count.txt', 'r') as f:
                for line in f:
                    user_id, count = line.strip().split(':')
                    users[int(user_id)] = int(count)
            @bot.tree.command()
            async def something(interaction: discord.Interaction):
            
            @bot.event
            async def on_ready():

                for guildId in guildsList:
                    await tree.sync(guild=discord.Object(id=guildId))

                print("Bot has connected to Discord!")
                bot.loop.create_task(process_queue())

            @tree.command(name="dream",
                          description="This is the dream command description",
                          guilds=guildsList)
            @app_commands.describe(task=f"Task?")
            async def dream(interaction, task: str):
                queue.append((interaction, task))
                await ctx.response.defer()
                await ctx.followup.send("Dreaming...", ephemeral=True)

            @tree.command(name="subscribe",
                          description="This is the subscribe description",
                          guilds=guildsList)
            async def subscribe(interaction):
                await ctx.response.send_message(
                    "Open the page below to pick your plan and subscribe! https://mee6.gg/m/thedream", ephemeral=True)

            await bot.start(TOKEN)
        except Exception as e:
            print(f"Error: {e}")
            await bot.close()


keep_alive()
asyncio.run(start_bot())
