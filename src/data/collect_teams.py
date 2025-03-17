"""
NBA Team Data Collection

This script connects to the NBA API and retrieves basic information about all NBA teams.
It demonstrates how to use the nba_api package and save data in a structured format.
"""

import os
import json
from datetime import datetime
from nba_api.stats.static import teams
import pandas as pd

def get_all_teams():
    """
    Retrieves a list of all NBA teams with their basic information.
    
    Returns:
        pandas.DataFrame: DataFrame containing team information
    """
    # Get all teams from the NBA API
    print("Retrieving NBA teams data...")
    all_teams = teams.get_teams()
    
    # Convert to DataFrame for easier manipulation
    teams_df = pd.DataFrame(all_teams)
    
    print(f"Retrieved information for {len(teams_df)} NBA teams")
    return teams_df

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
    
    # Get team data
    teams_df = get_all_teams()
    
    # Display data summary
    print("\nData Summary:")
    print(f"Number of teams: {len(teams_df)}")
    print("\nFirst few teams:")
    print(teams_df.head())
    
    # Save data with timestamp
    save_data(teams_df, f"nba_teams_{timestamp}.csv")
    
    print("\nNBA Team Data Collection Completed")

if __name__ == "__main__":
    main()