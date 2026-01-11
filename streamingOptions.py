from nba_api.stats.endpoints import ScoreboardV2
from nba_api.stats.endpoints import PlayerGameLogs
from datetime import date, timedelta
import pandas as pd

today = date.today()

test_date_to = '12/15/2024'  
test_date_from = '11/15/2024'  

scoreboard = ScoreboardV2(game_date=today.strftime('%m/%d/%Y'))
player_logs = PlayerGameLogs(season_nullable='2024-25', date_from_nullable=test_date_from, date_to_nullable=test_date_to)

games_df = scoreboard.get_data_frames()[0]
players_df = player_logs.get_data_frames()[0]
 
home_team_ids = games_df['HOME_TEAM_ID']
visitor_team_ids = games_df['VISITOR_TEAM_ID']

team_ids = pd.concat([home_team_ids, visitor_team_ids]).unique().tolist()

print(team_ids)
print(players_df.head())
