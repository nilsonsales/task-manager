import schedule
import time
import logging

logger = logging.getLogger()


def schedule_task(my_function):
    # Schedule the task to run every day at midnight
    schedule.every().day.at("00:00").do(my_function)

    # Run the scheduling loop continuously
    while True:
        logger.debug("Running scheduled task")
        schedule.run_pending()
        time.sleep(3600)  # Sleep for 3600 seconds (1 hour) before checking the schedule again