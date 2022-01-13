from datetime import datetime, timedelta
from sportsipy.nba.boxscore import Boxscores
import pandas
sport = 'basketball_nba'
yesterday = datetime.today()- timedelta(days = 1)
games_today = Boxscores(yesterday)
date = yesterday.strftime('%-m-%d-%Y')
print (games_today.games.keys())
df = pandas.DataFrame.from_dict(games_today.games[date]).drop(['boxscore','losing_abbr','losing_name','winning_abbr','winning_name','home_abbr','away_abbr'],axis=1)
df['total_score'] = df['away_score'] + df['home_score']
print(df)
fileName = sport+yesterday.strftime('%Y-%m-%d')+'.csv'
oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')

#print(oddsDF.loc[oddsDF['home_team'].str.contains('Brooklyn', case=False)])
for team in df:
    print(team)
    oddsDF[oddsDF.loc[oddsDF['home_team'].str.contains(team.loc['home_name'], case=False)],'total_score'] = team.loc['total_score']