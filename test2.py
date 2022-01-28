from audioop import tomono
from datetime import date, datetime, timezone, timedelta
import numpy as np
import pandas
runNum = 2
current = pandas.read_csv('basketball_nba2022-01-20.csv').drop(columns='Unnamed: 0')

current = current.drop(columns='total_score')


current.to_csv('basketball_ncaab2022-01-20.csv')
#tomorrow's date + 'T09:00:00Z'

