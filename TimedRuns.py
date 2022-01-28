from ast import Num
import Gambler
import schedule
import time
import Runner
import os.path
import FinalsNBA
import FinalNCAAB
def yesterdayScores():
                
    FinalNCAAB.getFinalScores()

    FinalsNBA.getFinalScores()

def job():
    
    Runner.run()

schedule.every(10).minutes.do(job)
schedule.every(1).day.do(yesterdayScores)


while True:
    schedule.run_pending()
    
    time.sleep(1)
   

