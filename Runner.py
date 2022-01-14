import Gambler
import FindBets
runNum = 7
Gambler.getOdds('basketball_ncaab',runNum)
Gambler.getOdds('basketball_nba',runNum)
FindBets.CheckBets('basketball_ncaab',runNum)
FindBets.CheckBets('basketball_nba',runNum)