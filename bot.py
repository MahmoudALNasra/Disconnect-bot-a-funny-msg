import discord
import os

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = discord.Client(intents=intents)

TARGET_USERNAMES = ["juba.x", "Nutonッ"]
COOLDOWN = 60
last_response_time = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('Bot is ready!')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Check if message is from target user
    if message.author.name in TARGET_USERNAMES:
        # Cooldown check
        current_time = message.created_at.timestamp()
        last_time = last_response_time.get(message.author.name, 0)
        
        if current_time - last_time < COOLDOWN:
            return
        
        # Send response
        await message.channel.send(f"Fuck off {message.author.name}")
        last_response_time[message.author.name] = current_time
        print(f"Responded to {message.author.name}")

# Get token from environment variable or prompt
token = os.getenv('DISCORD_BOT_TOKEN')
if not token:
    print("Please set the DISCORD_BOT_TOKEN environment variable")
    exit(1)

bot.run(token)
