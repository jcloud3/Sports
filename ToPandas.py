import pandas as pd
import json
def pds(file):

    
    df_nested_list = pd.json_normalize(file, record_path=['bookmakers','markets','outcomes'],meta=['home_team','away_team',['bookmakers','title'],'commence_time'])
    return (df_nested_list)
