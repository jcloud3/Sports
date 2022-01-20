import Gambler
import FindBets


def run():
    Gambler.getOdds('basketball_ncaab')
    Gambler.getOdds('basketball_nba')
    FindBets.CheckBets('basketball_ncaab')
    FindBets.CheckBets('basketball_nba')

run()