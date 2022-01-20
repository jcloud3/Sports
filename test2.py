import pandas
runNum = 2
current = pandas.read_csv('basketball_ncaab2022-01-13.csv').drop(columns=['Unnamed: 0'])
current.to_csv('basketball_ncaab2022-01-13.csv')
print(len(current.columns)-5)