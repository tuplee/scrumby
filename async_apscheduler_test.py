import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Define an asynchronous function that you want to schedule
async def async_task():
    print(f"Executing asynchronous task at {datetime.now()}")

# Set up the scheduler
scheduler = AsyncIOScheduler()

# Schedule the asynchronous function to run every minute
scheduler.add_job(async_task, 'interval', minutes=1)

# Define a simple synchronous function to run in the main event loop
async def event_loop():
    while True:
        print("Event loop running...")
        await asyncio.sleep(1)

# Run the scheduler in a separate task
async def run_scheduler():
    print("Starting the scheduler...")
    scheduler.start()

# Start the event loop and run the scheduler concurrently
async def main():
    await asyncio.gather(
        event_loop(),
        run_scheduler()
    )

# Run the main coroutine
asyncio.run(main())
