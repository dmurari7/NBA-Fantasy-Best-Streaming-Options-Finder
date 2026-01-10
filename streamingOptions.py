from nba_api.stats.endpoints import ScoreboardV2
from datetime import date
import pandas as pd

today = date.today()

scoreboard = ScoreboardV2(game_date=today.strftime('%m/%d/%Y'))

games_df = scoreboard.get_data_frames()[0]
 
home_team_ids = games_df['HOME_TEAM_ID']
visitor_team_ids = games_df['VISITOR_TEAM_ID']

team_ids = pd.concat([home_team_ids, visitor_team_ids]).unique().tolist()

print(team_ids)
