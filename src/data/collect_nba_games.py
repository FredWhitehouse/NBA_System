"""
NBA Game Data Collection and Cleaning

This script collects NBA game data from 2017-18 through 2023-24 seasons,
applies prefix-based filtering to include only official regular season (002) 
and playoff games (004), and validates the results against expected game counts.
"""

import os
import time
import pandas as pd
from datetime import datetime
from nba_api.stats.endpoints import leaguegamefinder

def get_complete_season_games(season):
    """
    Retrieve complete game data for a specific NBA season.
    
    Args:
        season (str): Season in format 'YYYY-YY' (e.g., '2022-23')
    
    Returns:
        pandas.DataFrame: Complete data for the season
    """
    print(f"Collecting data for season {season}...")
    
    # Collect data for each conference to ensure completeness
    all_data = []
    
    for conference in ['East', 'West']:
        gamefinder = leaguegamefinder.LeagueGameFinder(
            season_nullable=season,
            league_id_nullable='00',  # NBA league ID
            conference_nullable=conference
        )
        
        # Get the game data
        conf_df = gamefinder.get_data_frames()[0]
        print(f"  - Retrieved {len(conf_df)} {conference}ern Conference game records")
        all_data.append(conf_df)
        
        # Add pause to avoid API rate limits
        time.sleep(1)
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df['SEASON'] = season  # Add season identifier
    
    # Report counts
    unique_games = combined_df['GAME_ID'].nunique()
    print(f"  - Total: {len(combined_df)} team records representing {unique_games} unique games")
    
    return combined_df

def clean_nba_data(games_df):
    """
    Clean NBA game data using the game ID prefix system to identify game types.
    NBA Game ID prefixes:
    - 001: Preseason games (exclude)
    - 002: Regular season games (keep)
    - 004: Playoff games (keep)
    - 003: All-Star games (exclude)
    
    Args:
        games_df (pandas.DataFrame): Raw game data
        
    Returns:
        pandas.DataFrame: Cleaned data containing only regular season and playoff games
    """
    # Make a copy to avoid the SettingWithCopyWarning
    games_df = games_df.copy()
    
    print(f"\nCleaning data - starting with {len(games_df)} records")
    
    # Step 1: Keep only official NBA teams
    official_nba_teams = [
        'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets',
        'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
        'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
        'LA Clippers', 'LA Lakers', 'Memphis Grizzlies', 'Miami Heat',
        'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
        'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns',
        'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors',
        'Utah Jazz', 'Washington Wizards'
    ]
    
    # Include historical team names
    historical_team_names = {
        'New Orleans Hornets': 'New Orleans Pelicans',
        'Charlotte Bobcats': 'Charlotte Hornets',
        'New Jersey Nets': 'Brooklyn Nets',
        'New Orleans/Oklahoma City Hornets': 'New Orleans Pelicans'
    }
    
    all_valid_names = official_nba_teams + list(historical_team_names.keys())
    team_mask = games_df['TEAM_NAME'].isin(all_valid_names)
    games_df = games_df[team_mask].copy()
    print(f"After filtering non-NBA teams: {len(games_df)} records")
    
    
    # Step 2: Extract game type from GAME_ID prefix
    games_df['GAME_TYPE'] = games_df['GAME_ID'].astype(str).str[:3]
    
    # Print distribution of game types to verify our understanding
    print("\nGame type distribution based on GAME_ID prefix:")
    game_type_counts = games_df['GAME_TYPE'].value_counts()
    print(game_type_counts)
    
    # Step 3: Filter to keep only regular season (002) and playoff (004) games
    valid_game_types = ['002', '004']
    games_df = games_df[games_df['GAME_TYPE'].isin(valid_game_types)].copy()
    print(f"After filtering by game type prefix: {len(games_df)} records")
    
    # Step 4: Additional safety check for exhibition games (redundant but thorough)
    exhibition_keywords = ['all-star', 'all star', 'rising stars', 'celebrity']
    matchup_mask = ~games_df['MATCHUP'].str.lower().str.contains('|'.join(exhibition_keywords), na=False)
    games_df = games_df[matchup_mask].copy()
    print(f"After removing any remaining exhibition games: {len(games_df)} records")
    
    # Step 5: Remove games with 0 points (likely errors)
    games_df = games_df[games_df['PTS'] > 0].copy()
    print(f"After removing zero-point games: {len(games_df)} records")
    
    # Drop temporary columns
    games_df = games_df.drop(columns=['GAME_TYPE'])
    
    return games_df

def standardize_team_names(games_df):
    """
    Standardize team names for consistency across the dataset.
    Specifically addresses the Lakers/Clippers naming inconsistency.
    """
    # Create a copy to avoid warnings
    games_df = games_df.copy()
    
    # Option 1: Standardize to full city names
    # games_df['TEAM_NAME'] = games_df['TEAM_NAME'].replace('LA Clippers', 'Los Angeles Clippers')
    
    # Option 2: Standardize to abbreviated city names (probably better)
    games_df['TEAM_NAME'] = games_df['TEAM_NAME'].replace('Los Angeles Lakers', 'LA Lakers')
    
    print(f"Standardized team names for consistency")
    return games_df

def validate_data(games_df):
    """
    Validate cleaned data against expected game counts.
    
    Args:
        games_df (pandas.DataFrame): Cleaned game data
    """
    print("\nValidating data completeness:")
    
    # Records per season
    season_counts = games_df['SEASON'].value_counts().sort_index()
    print("\nRecords per season:")
    print(season_counts)
    
    # Unique games per season
    unique_games = games_df.groupby('SEASON')['GAME_ID'].nunique()
    print("\nUnique games per season:")
    print(unique_games)
    
    # Expected games (regular season + playoffs) per season
    expected_games = {
        '2017-18': 1312,
        '2018-19': 1313,
        '2019-20': 1142,  # COVID-shortened season
        '2020-21': 1165,  # Reduced 72-game season
        '2021-22': 1312,
        '2022-23': 1313,
        '2023-24': 1314
    }
    
    # Expected team records (double the game count)
    expected_records = {season: count*2 for season, count in expected_games.items()}
    
    # Check both game counts and team records
    print("\nValidation results:")
    print("Season   | Unique Games | Expected | % Match | Team Records | Expected | % Match")
    print("---------|--------------|----------|---------|--------------|----------|--------")
    
    for season in sorted(unique_games.index):
        if season in expected_games:
            # Game count validation
            actual_games = unique_games[season]
            expected = expected_games[season]
            game_pct = (actual_games / expected) * 100
            game_status = "✓" if 95 <= game_pct <= 105 else "!"
            
            # Team record validation
            actual_records = season_counts[season]
            expected_rec = expected_records[season]
            record_pct = (actual_records / expected_rec) * 100
            record_status = "✓" if 95 <= record_pct <= 105 else "!"
            
            print(f"{season} | {actual_games:12d} | {expected:8d} | {game_pct:6.1f}% {game_status} | {actual_records:12d} | {expected_rec:8d} | {record_pct:6.1f}% {record_status}")
    
    # Overall assessment
    all_valid = all(95 <= (unique_games[s] / expected_games[s]) * 100 <= 105 for s in expected_games if s in unique_games)
    
    if all_valid:
        print("\n✅ SUCCESS: All seasons have complete data (within 5% of expected counts)")
    else:
        incomplete = [s for s in expected_games if s in unique_games and not (95 <= (unique_games[s] / expected_games[s]) * 100 <= 105)]
        print(f"\n⚠️ WARNING: The following seasons may have incomplete data: {', '.join(incomplete)}")

def main():
    """Main function to collect, clean, and save NBA game data."""
    print("NBA Game Data Collection and Cleaning Started")
    
    # Timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define seasons to collect
    seasons = ['2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    
    # Step 1: Collect data for all seasons
    all_seasons_data = []
    for season in seasons:
        try:
            season_data = get_complete_season_games(season)
            all_seasons_data.append(season_data)
        except Exception as e:
            print(f"Error collecting data for season {season}: {e}")
    
    # Combine all seasons
    if all_seasons_data:
        print("\nCombining data from all seasons...")
        all_games_df = pd.concat(all_seasons_data, ignore_index=True)
        all_games_df = standardize_team_names(all_games_df)
    
        print(f"Combined dataset: {len(all_games_df)} records")
        
        # Save raw data
        raw_dir = 'data/raw'
        os.makedirs(raw_dir, exist_ok=True)
        raw_file = os.path.join(raw_dir, f"nba_games_raw_{timestamp}.csv")
        all_games_df.to_csv(raw_file, index=False)
        print(f"Raw data saved to: {raw_file}")
        
        # Step 2: Clean the data
        cleaned_df = clean_nba_data(all_games_df)
        
        # Step 3: Validate the data
        validate_data(cleaned_df)
        
        # Step 4: Save the cleaned data
        processed_dir = 'data/processed'
        os.makedirs(processed_dir, exist_ok=True)
        cleaned_file = os.path.join(processed_dir, f"nba_games_clean_{timestamp}.csv")
        cleaned_df.to_csv(cleaned_file, index=False)
        print(f"\nCleaned data saved to: {cleaned_file}")
    else:
        print("No data was collected. Please check for errors.")
    
    print("\nNBA Game Data Collection and Cleaning Completed")

if __name__ == "__main__":
    main()