"""
NBA Team Data Collection

This script connects to the NBA API and retrieves basic information about all NBA teams.
It demonstrates how to use the nba_api package and save data in a structured format.
"""

import os
import json
from datetime import datetime
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings
import pandas as pd

def get_all_teams():
    """
    Retrieves a list of all NBA teams with their basic information.
    
    Returns:
        pandas.DataFrame: DataFrame containing team information
    """
    print("Retrieving NBA teams data...")
    all_teams = teams.get_teams()
    teams_df = pd.DataFrame(all_teams)
    print(f"Retrieved information for {len(teams_df)} NBA teams")
    return teams_df

def get_conference_data():
    """
    Retrieves conference information for NBA teams from league standings.
    
    Returns:
        pandas.DataFrame: DataFrame with team IDs and their conferences
    """
    print("Retrieving conference data from league standings...")
    standings = leaguestandings.LeagueStandings()
    standings_df = standings.get_data_frames()[0]
    
    # Select only the relevant columns
    conference_df = standings_df[['TeamID', 'Conference']]
    print(f"Retrieved conference data for {len(conference_df)} teams")
    return conference_df

def enrich_team_data(teams_df, conference_df):
    """
    Combines basic team data with conference information.
    
    Args:
        teams_df (pandas.DataFrame): Basic team information
        conference_df (pandas.DataFrame): Conference information
    
    Returns:
        pandas.DataFrame: Enriched team information
    """
    print("Combining team data with conference information...")
    
    # Rename columns to match between dataframes
    conference_df = conference_df.rename(columns={'TeamID': 'id'})
    
    # Merge the dataframes on team ID
    enriched_df = pd.merge(teams_df, conference_df, on='id', how='left')
    
    # Check if any teams are missing conference data
    missing_conf = enriched_df['Conference'].isna().sum()
    if missing_conf > 0:
        print(f"Warning: {missing_conf} teams are missing conference data")
    
    return enriched_df

def save_data(df, filename):
    """
    Saves the DataFrame to a CSV file in the data/raw directory.
    
    Args:
        df (pandas.DataFrame): The DataFrame to save
        filename (str): Name of the file (without directory path)
    """
    # Create data directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Full path for the output file
    output_path = os.path.join('data/raw', filename)
    
    # Save the DataFrame to CSV
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
    
    # Also save as JSON for reference
    json_path = output_path.replace('.csv', '.json')
    df.to_json(json_path, orient='records', indent=4)
    print(f"Data also saved to {json_path}")

def main():
    """Main function to execute the data collection process."""
    print("NBA Team Data Collection Started")
    
    # Get timestamp for the data collection
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get basic team data
    teams_df = get_all_teams()
    
    # Get conference data
    conference_df = get_conference_data()
    
    # Combine the datasets
    enriched_teams_df = enrich_team_data(teams_df, conference_df)
    
    # Display data summary
    print("\nData Summary:")
    print(f"Number of teams: {len(enriched_teams_df)}")
    print("\nFirst few teams with conference information:")
    print(enriched_teams_df[['full_name', 'Conference']].head())
    
    # Count teams by conference
    print("\nTeams per conference:")
    print(enriched_teams_df['Conference'].value_counts())
    
    # Save enriched data with timestamp
    save_data(enriched_teams_df, f"nba_teams_{timestamp}.csv")
    
    print("\nNBA Team Data Collection Completed")

if __name__ == "__main__":
    main()