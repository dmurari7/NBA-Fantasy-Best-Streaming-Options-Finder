from nba_api.stats.endpoints import ScoreboardV2
from nba_api.stats.endpoints import PlayerGameLogs
from datetime import date, timedelta
import pandas as pd
from injury_scraper import get_injury_report

def clean_name(name):
    name = name.lower().strip()
    name = name.replace(' jr.', '').replace(' sr.', '').replace(' iii', '').replace(' ii', '')
    return name

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

todays_players_grouped_logs = todays_players_30day_game_logs.groupby(['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION'])
agg_stats_for_players = todays_players_grouped_logs.agg({'MIN':'mean', 'PTS':'mean', 'AST':'mean','STL':'mean', 'BLK':'mean', 'REB':'mean'})
todays_players_df = agg_stats_for_players.reset_index()

todays_streamable_players = todays_players_df[(todays_players_df['MIN'] >= 15) & (todays_players_df['MIN'] <= 25)].copy()

# Rename columns
todays_streamable_players.columns = ['PLAYER_ID', 'PLAYER_NAME', 'TEAM', 'AVG_MIN', 'AVG_PTS', 'AVG_AST', 'AVG_STL', 'AVG_BLK', 'AVG_REB']

# Round decimals
todays_streamable_players['AVG_MIN'] = todays_streamable_players['AVG_MIN'].round(1)
todays_streamable_players['AVG_PTS'] = todays_streamable_players['AVG_PTS'].round(1)
todays_streamable_players['AVG_AST'] = todays_streamable_players['AVG_AST'].round(1)
todays_streamable_players['AVG_STL'] = todays_streamable_players['AVG_STL'].round(1)
todays_streamable_players['AVG_BLK'] = todays_streamable_players['AVG_BLK'].round(1)
todays_streamable_players['AVG_REB'] = todays_streamable_players['AVG_REB'].round(1)

injury_df = get_injury_report()

injury_df['PLAYER_NAME_CLEAN'] = injury_df['PLAYER_NAME'].apply(clean_name)
todays_streamable_players['PLAYER_NAME_CLEAN'] = todays_streamable_players['PLAYER_NAME'].apply(clean_name)

# Merge injury status into streamable players
todays_streamable_players = todays_streamable_players.merge(
    injury_df[['PLAYER_NAME_CLEAN', 'INJURY_STATUS']], 
    on='PLAYER_NAME_CLEAN', 
    how='left'
)

# Filter out players who are "Out"
todays_streamable_players = todays_streamable_players[
    (todays_streamable_players['INJURY_STATUS'].isna()) |  # Not on injury report
    (~todays_streamable_players['INJURY_STATUS'].isin(['Out']))  # Or not Out
]

# Optional: Flag questionable players with a visual indicator
todays_streamable_players['STATUS_FLAG'] = todays_streamable_players['INJURY_STATUS'].apply(
    lambda x: '⚠️' if pd.notna(x) and x in ['Questionable', 'Doubtful'] else ''
)

# Select columns to display
final_output = todays_streamable_players[['PLAYER_NAME', 'TEAM', 'AVG_MIN', 'AVG_PTS', 'AVG_AST', 'AVG_STL', 'AVG_BLK', 'AVG_REB','STATUS_FLAG']]
final_output = final_output.sort_values('AVG_PTS', ascending=False)

# Display streaming options
print("\n" + "="*84)
print("TOP STREAMING OPTIONS FOR TODAY")
print("="*84)
print(final_output.to_string(index=False))
print("="*84)


