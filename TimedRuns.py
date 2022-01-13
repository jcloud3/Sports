import Gambler
import schedule
import time

def job():
    print("I'm working...")

schedule.every().day.at("10:47").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)


