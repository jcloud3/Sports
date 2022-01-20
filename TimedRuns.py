from ast import Num
import Gambler
import schedule
import time
import Runner
import os.path
from datetime import date



def job():
    
    Runner.run()

schedule.every(10).minutes.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)


