# Checking for Magic-Bucks playoff games specifically
mask = (
    (games_df['SEASON'] == '2019-20') & 
    (games_df['SEASON_TYPE'] == 'Playoffs') & 
    (
        ((games_df['TEAM_NAME'] == 'Orlando Magic') & (games_df['MATCHUP'].str.contains('MIL'))) |
        ((games_df['TEAM_NAME'] == 'Milwaukee Bucks') & (games_df['MATCHUP'].str.contains('ORL')))
    )
)

playoff_games = games_df[mask]
print(f"Found {len(playoff_games)} Magic-Bucks playoff game records from 2019-20")
print(f"Number of unique games: {playoff_games['GAME_ID'].nunique()}")