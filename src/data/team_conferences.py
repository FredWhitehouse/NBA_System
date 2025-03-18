## used to validate theory that conference data is stored in NBA_API somewhere

from nba_api.stats.endpoints import leaguestandings
import pandas as pd

# Fetch NBA Standings (includes conference information)
standings = leaguestandings.LeagueStandings(season="2023-24").get_data_frames()[0]

# Select relevant columns
df = standings[['TeamCity', 'TeamName', 'Conference']]

# Rename columns for clarity
df.columns = ['City', 'Team', 'Conference']

# Combine City and Team Name for full team name
df["Team Name"] = df["City"] + " " + df["Team"]

# Drop redundant columns
df = df[['Team Name', 'Conference']]

# Display the data
print(df)
