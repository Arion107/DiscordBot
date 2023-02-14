import os
import discord
from discord.ext import commands

# Load previously saved message count data from file (if it exists)
if os.path.exists("message_count.json"):
    with open("message_count.json", "r") as f:
        message_count = json.load(f)
else:
    message_count = {}

bot = commands.Bot(command_prefix='/')

# Set up the allowed channel for the bot
allowed_channel = None

@bot.event
async def on_ready():
    global allowed_channel
    print(f'{bot.user.name} has connected to Discord!')
    # Load previously saved allowed channel ID from file (if it exists)
    if os.path.exists("allowed_channel_id.txt"):
        with open("allowed_channel_id.txt", "r") as f:
            channel_id = int(f.read())
            allowed_channel = bot.get_channel(channel_id)
            if allowed_channel:
                print(f"Allowed channel set to {allowed_channel.mention}")
            else:
                print("Could not find the previously set allowed channel.")
    else:
        print("No previously set allowed channel found.")

@bot.command()
async def setchannel(ctx, channel: discord.TextChannel):
    global allowed_channel
    allowed_channel = channel
    # Save the allowed channel ID to file
    with open("allowed_channel_id.txt", "w") as f:
        f.write(str(channel.id))
    await ctx.send(f"Allowed channel set to {channel.mention}")

@bot.event
async def on_message(message):
    global allowed_channel, message_count
    
    # Only process messages from the allowed channel
    if allowed_channel and message.channel != allowed_channel:
        return
    
    # Only process messages from non-bot users
    if message.author.bot:
        return
    
    user_id = message.author.id

   # If user has role AI, don't increment message count and allow message
    if any(role.name == 'AI' for role in message.author.roles):
        await bot.process_commands(message)
        return
      
   # Increment message count for the user
    if user_id not in message_count:
        message_count[user_id] = 1
    else:
        message_count[user_id] += 1
    
    # Check if the user has exceeded the message limit
    if message_count[user_id] > 25:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, Get the AI Role to continue sending messages on this channel")
    elif message_count[user_id] == 25:
        await message.channel.send(f"{message.author.mention}, Get the AI Role to continue sending messages on this channel")
    
    await bot.process_commands(message)

@bot.event
async def on_disconnect():
    # Save the message count data to file before disconnecting
    with open("message_count.json", "w") as f:
        json.dump(message_count, f)
    print("Bot disconnected.")

bot.run(os.getenv('TOKEN'))

#Si no es en replit y no hace falta secret se usa -> bot.run('Token_aqui')
