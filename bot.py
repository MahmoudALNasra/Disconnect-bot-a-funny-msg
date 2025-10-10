import discord
import os
import asyncio
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.voice_states = True  # Required for voice channel tracking

bot = discord.Client(intents=intents)

# ===== CONFIGURATION =====
TARGET_USERNAMES = ["nutonx","kooka_n"]
TEXT_COOLDOWN = 3  # seconds for text responses
VOICE_DISCONNECT_MINUTES = 9999990  # minutes before disconnecting from voice
# =========================

# Storage for bot functionality
last_response_time = {}
voice_check_tasks = {}  # Track active voice disconnect timers

@bot.event
async def on_ready():
    print(f'🚀 Combined Bot Started Successfully!')
    print(f'✅ Logged in as: {bot.user} (ID: {bot.user.id})')
    print(f'⏰ Started at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'🔧 Features: Auto-Response + Voice Auto-Disconnect')
    print(f'🎯 Target users: {TARGET_USERNAMES}')
    print(f'⏱️ Voice disconnect after: {VOICE_DISCONNECT_MINUTES} minutes')
    print('=' * 50)

# ===== AUTO-RESPONSE FUNCTIONALITY =====
async def handle_auto_response(message):
    """Handle automatic responses to target users"""
    if message.author.name in TARGET_USERNAMES:
        current_time = message.created_at.timestamp()
        last_time = last_response_time.get(message.author.name, 0)
        
        # Check cooldown
        if current_time - last_time < TEXT_COOLDOWN:
            return False
        
        # Send response
        await message.channel.send(f"Fuck off {message.author.name} ya gay lol rekt ez")
        last_response_time[message.author.name] = current_time
        print(f"🤖 Auto-response to {message.author.name}")
        return True
    return False

# ===== VOICE DISCONNECT FUNCTIONALITY =====
@bot.event
async def on_voice_state_update(member, before, after):
    """Track when users join/leave voice channels"""
    
    # Only care about target users
    if member.name not in TARGET_USERNAMES:
        return
    
    user_id = member.id
    username = member.name
    
    # User joined a voice channel
    if after.channel is not None and (before.channel is None or before.channel != after.channel):
        print(f"🎧 {username} joined voice channel: {after.channel.name}")
        
        # Start disconnect timer
        voice_check_tasks[user_id] = asyncio.create_task(
            voice_disconnect_timer(member)
        )
    
    # User left voice channel
    elif before.channel is not None and after.channel is None:
        print(f"🎧 {username} left voice channel")
        
        # Cancel any pending disconnect task
        if user_id in voice_check_tasks:
            voice_check_tasks[user_id].cancel()
            del voice_check_tasks[user_id]

async def voice_disconnect_timer(member):
    """Wait for specified time, then disconnect user"""
    try:
        username = member.name
        
        # Wait for the specified minutes
        print(f"⏰ Started {VOICE_DISCONNECT_MINUTES} minute timer for {username}")
        await asyncio.sleep(VOICE_DISCONNECT_MINUTES * 60)  # Convert to seconds
        
        # Check if user is still in a voice channel
        if member.voice and member.voice.channel:
            print(f"🔌 Disconnecting {username} from voice channel")
            
            try:
                # Disconnect the user (no warning message)
                await member.move_to(None)
                print(f"✅ Successfully disconnected {username}")
                        
            except discord.Forbidden:
                print(f"❌ No permission to disconnect {username}")
            except discord.HTTPException as e:
                print(f"❌ Failed to disconnect {username}: {e}")
        
        # Clean up
        if member.id in voice_check_tasks:
            del voice_check_tasks[member.id]
            
    except asyncio.CancelledError:
        print(f"⏹️ Voice timer cancelled for {member.name}")
    except Exception as e:
        print(f"❌ Error in voice timer for {member.name}: {e}")

# ===== UTILITY COMMANDS =====
async def handle_utility_commands(message):
    """Handle utility commands for bot management"""
    if message.content.startswith('!voicestats'):
        # Show current voice tracking stats
        active_count = len(voice_check_tasks)
        await message.channel.send(f"🎧 Tracking {active_count} user(s) in voice channels")
        return True
    
    return False

# ===== MAIN MESSAGE HANDLER =====
@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Process utility commands first
    if await handle_utility_commands(message):
        return
    
    # Process auto-response
    await handle_auto_response(message)

# ===== BOT STARTUP =====
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        print("❌ ERROR: DISCORD_BOT_TOKEN environment variable not set!")
        print("💡 Set it in Railway dashboard → Variables")
        exit(1)
    
    print("🚂 Starting Enhanced Discord Bot...")
    bot.run(token)
