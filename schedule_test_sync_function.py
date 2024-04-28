import schedule
import time

# Define a simple synchronous function
def simple_task():
    print("Executing simple task")

# Schedule the function to run every minute
schedule.every().minute.do(simple_task)

# Run the scheduler loop
while True:
    # Run any pending jobs
    schedule.run_pending()
    # Add a delay to avoid consuming too much CPU
    time.sleep(1)
