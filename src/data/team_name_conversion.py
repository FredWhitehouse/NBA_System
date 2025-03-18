import pandas as pd

# Check team naming standardization in cleaned dataset
print("---------- TEAM NAMING STANDARDIZATION CHECK ----------")
games_df=pd.read_csv("data/processed/nba_games_clean_20250318_114900.csv")
# 1. Get all unique team names in the dataset
unique_teams = sorted(games_df['TEAM_NAME'].unique())
print("All unique team names in the cleaned dataset:")
for team in unique_teams:
    print(f"- {team}")

# 2. Specifically check for the Lakers and Clippers names
lakers_format = [team for team in unique_teams if 'Lakers' in team]
clippers_format = [team for team in unique_teams if 'Clippers' in team]

print(f"\nLakers name format: {lakers_format}")
print(f"Clippers name format: {clippers_format}")

# 3. Check if standardization was applied
if 'LA Lakers' in unique_teams and 'LA Clippers' in unique_teams:
    print("\n✓ STANDARDIZATION SUCCESSFUL: Both teams use the 'LA' prefix format")
elif 'Los Angeles Lakers' in unique_teams and 'Los Angeles Clippers' in unique_teams:
    print("\n✓ STANDARDIZATION SUCCESSFUL: Both teams use the 'Los Angeles' full city name format")
elif 'Los Angeles Lakers' in unique_teams and 'LA Clippers' in unique_teams:
    print("\n✗ STANDARDIZATION NOT APPLIED: Inconsistent naming still exists")
    print("   - Lakers use 'Los Angeles' format")
    print("   - Clippers use 'LA' abbreviated format")
else:
    print("\n? UNEXPECTED NAMING PATTERN: Neither standard format was found")

# 4. Show counts to verify data completeness
if lakers_format:
    lakers_count = games_df[games_df['TEAM_NAME'] == lakers_format[0]].shape[0]
    print(f"\nFound {lakers_count} records for {lakers_format[0]}")
    
if clippers_format:
    clippers_count = games_df[games_df['TEAM_NAME'] == clippers_format[0]].shape[0]
    print(f"Found {clippers_count} records for {clippers_format[0]}")

print("--------------------------------------------------")