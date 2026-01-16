from nba_api.stats.endpoints import ScoreboardV2
from nba_api.stats.endpoints import PlayerGameLogs
from datetime import date, timedelta
import pandas as pd

today = date.today()
thirty_days_ago = today - timedelta(days = 30)

scoreboard = ScoreboardV2(game_date=today.strftime('%m/%d/%Y'))
player_logs = PlayerGameLogs(season_nullable='2025-26', date_from_nullable=thirty_days_ago.strftime('%m/%d/%Y'), date_to_nullable=today.strftime('%m/%d/%Y'))

games_df = scoreboard.get_data_frames()[0]
players_df = player_logs.get_data_frames()[0]
 
home_team_ids = games_df['HOME_TEAM_ID']
visitor_team_ids = games_df['VISITOR_TEAM_ID']

team_ids = pd.concat([home_team_ids, visitor_team_ids]).unique().tolist()

todays_players_30day_game_logs = players_df[players_df['TEAM_ID'].isin(team_ids)]

todays_players_grouped_logs = todays_players_30day_game_logs.groupby(['PLAYER_ID', 'PLAYER_NAME'])
agg_stats_for_players = todays_players_grouped_logs.agg({'MIN':'mean', 'PTS':'mean'})
todays_players_df = agg_stats_for_players.reset_index()

todays_streamable_players = todays_players_df[(todays_players_df['MIN'] >= 15) & (todays_players_df['MIN'] <= 25)]

print(todays_streamable_players.sort_values('PTS', ascending=False))


