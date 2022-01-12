import pandas
from datetime import date

def CheckBets(sport):
    today = str(date.today())
    fileName = sport+today+".csv"
    oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
    oddsDF['Bet'] = oddsDF['point']