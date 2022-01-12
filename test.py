from datetime import date
import pandas
runNum = 2
current = pandas.read_csv('basketball_nba2022-01-06.csv').drop(columns='Unnamed: 0')
current2 = current.rename(columns={'price':f'price{runNum}','point':f'point{runNum}'}).sort_values(["home_team",'name','bookmakers.title'])
print(pandas.concat([current,current2],axis=1))
