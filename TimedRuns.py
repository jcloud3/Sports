#!/usr/bin/env python3
from ast import Num
import Gambler
import schedule
import time
import Runner
import os.path
import FinalsNBA
import FinalncaaB
def yesterdayScores():
                
    FinalncaaB.getFinalScores()

    FinalsNBA.getFinalScores()

def job():
    
    Runner.run()

schedule.every(40).minutes.do(job)
schedule.every(1).day.do(yesterdayScores)


while True:
    schedule.run_pending()
    
    time.sleep(1)
   

