import discord
from discord.ext import tasks

# Bot Token Goes Here
TOKEN = 'BOT_TOKEN_GOES_HERE'

# Channel ID Goes HERE
GENERAL_CHANNEL_ID = 1234567891011121314

# Define the intents your bot requires
intents = discord.Intents.all()

# Create a Discord client with the specified intents
client = discord.Client(intents=intents)

# Function to send a message mentioning the selected user in the general channel
async def send_alert():
    channel = client.get_channel(GENERAL_CHANNEL_ID)
    if channel:
        await channel.send("This is just a test. Sorry for the ping!!!")
    else:
        print("Error: Channel not found.")

# Schedule the alert to run every minute for testing
@tasks.loop(seconds=60)  # Run every 60 seconds (1 minute)
async def schedule_alert():
    await send_alert()

# Event handler for bot ready event
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    schedule_alert.start()  # Start the task loop when the bot is ready

# Start the bot
client.run(TOKEN)
