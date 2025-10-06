import discord
import os

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = discord.Client(intents=intents)

TARGET_USERNAMES = ["juba.x", "nutonx","ibra6710","kooka_n"]
COOLDOWN = 3
last_response_time = {}

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    print('🚀 Bot is online and ready!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.author.name in TARGET_USERNAMES:
        current_time = message.created_at.timestamp()
        last_time = last_response_time.get(message.author.name, 0)
        
        if current_time - last_time < COOLDOWN:
            return
        
        await message.channel.send(f"Fuck off {message.author.name}")
        last_response_time[message.author.name] = current_time
        print(f"📨 Responded to {message.author.name}")

if __name__ == "__main__":
    # Railway provides the PORT environment variable, but Discord bots don't use it
    # We just need to start the bot
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        print("❌ ERROR: DISCORD_BOT_TOKEN environment variable not set!")
        print("💡 Please set it in Railway dashboard → Variables")
        exit(1)
    
    print("🚂 Starting bot...")
    bot.run(token)
