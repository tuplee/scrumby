import discord
import random
import asyncio
from discord.ext import tasks
from datetime import datetime, timedelta
import pytz

# Define the intents your bot requires
intents = discord.Intents.all()

# Create a Discord client with the specified intents
client = discord.Client(intents=intents)

# Bot Token Goes Here
TOKEN = 'BOT_TOKEN_GOES_HERE'

# Channel ID Goes HERE
GENERAL_CHANNEL_ID = 123456789012345678

# List of users
users = ["user1", "user2", "user3"]

# Dictionary to keep track of previous scrum masters and their last selection time
previous_scrum_masters = {}

# Function to select a random user as scrum master, ensuring they haven't been selected in the last 2 weeks
def select_scrum_master(users):
    eligible_users = [user for user in users if user not in previous_scrum_masters or (datetime.now() - datetime.fromtimestamp(previous_scrum_masters[user])).days >= 14]
    if not eligible_users:
        # If no eligible users found (all have been selected within the last 2 weeks), reset the selection
        previous_scrum_masters.clear()
        eligible_users = users
    selected_user = random.choice(eligible_users)
    previous_scrum_masters[selected_user] = datetime.now().timestamp()
    return selected_user

# Function to send a message mentioning the selected user in the general channel
async def send_alert(selected_user):
    # Get the general channel
    channel = client.get_channel(GENERAL_CHANNEL_ID)
    
    if channel:
        # Mention the selected user in a message
        await channel.send(f"@{selected_user} Look at me. You are the SCRUM Master for the week. Your job is to keep the Product Owners on track, run the standup meetings, and build the Gantt chart with weekly tasks. Have fun!")

# Function to calculate the next Sunday at 6 PM PDT
def next_sunday_6pm_pdt():
    tz = pytz.timezone('America/Los_Angeles')  # Set timezone to PDT
    today = datetime.now(tz)
    next_sunday = today + timedelta(days=(6 - today.weekday() % 7))  # Calculate the next Sunday
    next_sunday_6pm = next_sunday.replace(hour=18, minute=0, second=0, microsecond=0)  # Set time to 6 PM
    return next_sunday_6pm

# Function to schedule the scrum master selection and alert
@tasks.loop(hours=24*7)  # Run every week
async def schedule_alert():
    next_alert_time = next_sunday_6pm_pdt()
    await asyncio.sleep((next_alert_time - datetime.now()).total_seconds())
    # Select a scrum master
    selected_user = select_scrum_master(users)
    print("The selected scrum master for this test is:", selected_user)
    
    # Send the alert
    await send_alert(selected_user)

# Event handler for bot ready event
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    schedule_alert.start()  # Start the task

# Start the bot
client.run(TOKEN)
