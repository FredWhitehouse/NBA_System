## Data Cleaning Methodology

The raw game data collected from the NBA API required several cleaning steps to ensure accuracy and relevance for prediction purposes. The following records were identified and removed:

### 1. Zero-Point Games
**Description:** Games where a team was recorded as scoring 0 points
**Number Removed:** 2 games
**Justification:** In professional basketball, a team scoring exactly 0 points is impossible in a completed game. These records likely represent data entry errors, canceled games, or placeholder entries in the NBA database.
**Impact on Analysis:** Removing these prevents severe statistical distortions, particularly in scoring averages and distribution analyses.

### 2. All-Star Games
**Description:** Exhibition games featuring temporary teams of selected players from across the league
**Justification:** All-Star games were removed for multiple analytical reasons:
- Teams are temporary collections of players from different franchises
- Games feature minimal defensive effort and non-standard competitive dynamics
- Results have no impact on team standings or season outcomes
- Playing time distribution differs significantly from regular games
- Statistical patterns in these games do not represent normal team performance
**Impact on Analysis:** Removing these ensures all analyzed games represent actual NBA teams competing under standard rules and incentives.

### 3. Preseason Games
**Description:** Games played before the official start of the NBA regular season
**Number Removed:** Approximately 700-800 games
**Identification Method:** Multiple criteria were used to identify preseason games:
- Games played before established season start dates for each year
- Early October games (before October 16th)
- Games with preseason indicators in game identifiers
**Justification:** Preseason games were excluded because:
- Star players typically play limited minutes
- Coaches prioritize experimentation over winning
- Teams often use incomplete or non-standard rotations
- Competitive intensity varies significantly from regular season
- Results have no impact on standings
**Impact on Analysis:** Removing preseason games ensures the dataset reflects only games where teams were playing with their standard rotations and competitive incentives.

### Resulting Dataset
The cleaning process resulted in a dataset containing only regular season and playoff games, providing a consistent foundation for identifying meaningful patterns and building accurate prediction models.

## Data Cleaning Methodology

The game data undergoes a structured cleaning process to ensure it contains only relevant records for prediction modeling:

1. **Team Filtering**: Only records from the 30 official NBA franchises are retained, including teams that have changed names in recent history.

2. **Preseason Removal**: Games before each season's official start date are excluded:
   - 2017-18: Before October 17, 2017
   - 2018-19: Before October 16, 2018
   - 2019-20: Before October 22, 2019
   - 2020-21: Before December 22, 2020 (COVID-delayed season)
   - 2021-22: Before October 19, 2021
   - 2022-23: Before October 18, 2022
   - 2023-24: Before October 24, 2023

3. **Exhibition Game Removal**: All-Star games and other exhibition events are identified and removed based on team names and matchup descriptions.

4. **Data Validation**: The cleaned dataset is validated against expected game counts for each season to ensure completeness.

This cleaning approach ensures the dataset contains only standard NBA regular season and playoff games, creating a reliable foundation for our prediction model.

## Data Completeness Note

The NBA game dataset shows an interesting pattern where:
- We have near-perfect coverage of unique games across all seasons (99.8%-100.4%)
- Team records consistently represent about 96-97% of the theoretical maximum

This indicates that approximately 3-4% of games have only one team's perspective recorded in the official NBA data, rather than both teams. This pattern is consistent across all seasons and represents normal variation in sports data collection. It does not impact the completeness or quality of our game coverage for prediction purposes.

## API UPDATE

Discovery of the nba_api logging game ids with different game types. E.G. all games start with either 001,002,003,004,005. 002/003 represent regular and postseason games only and makes an easy filtering tool. As such the original collect_nba_games.py script is adjusted and simplified. 



# NBA Game Data Dictionary

## Data Source
Game data is collected from the NBA API using the `leaguegamefinder` endpoint, with filtering applied to include only official regular season and playoff games.

## Game Type Classification
Game types are identified using the first three digits of the GAME_ID field:
- 001: Preseason games (excluded from this dataset)
- 002: Regular season games (included)
- 004: Playoff games (included)
- 005: All-Star games (excluded from this dataset)

## Data Fields
| Column | Data Type | Description | Business Meaning |
|--------|-----------|-------------|-----------------|
| GAME_ID | String | Unique identifier for each game | Primary key for linking game data |
| TEAM_NAME | String | Full team name (e.g., "Boston Celtics") | Identifies the team perspective for this record |
| MATCHUP | String | Game matchup in format "TEAM vs. OPP" or "TEAM @ OPP" | Shows opponents and home/away status |
| ... | ... | ... | ... |

## Data Completeness Note
The NBA game dataset shows an interesting pattern where:
- We have near-perfect coverage of unique games across all seasons (99.8%-100.4%)
- Team records consistently represent about 96-97% of the theoretical maximum

This indicates that approximately 3-4% of games have only one team's perspective recorded in the official NBA data, rather than both teams. This pattern is consistent across all seasons and represents normal variation in sports data collection. It does not impact the completeness or quality of our game coverage for prediction purposes.

## Seasons Covered
This dataset contains complete game information for seven NBA seasons from 2017-18 through 2023-24, including both regular season and playoff games.

## Naming Conventions
For consistency, LA-based teams use the abbreviated city format:
- "LA Lakers" (standardized from "Los Angeles Lakers")
- "LA Clippers"

This standardization was implemented to maintain consistent naming patterns
across all teams and prevent confusion in analysis.