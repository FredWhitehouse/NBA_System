# NBA_System
## Data Collection Evolution

The team data collection process was enhanced during development:
- Initial version: Basic team attributes collected from NBA API
- Enhanced version: Added conference information by integrating the leaguestandings endpoint

The most recent CSV file in `data/raw/` contains the complete dataset with conference information.

## Data Collection Process

The data collection pipeline consists of two main scripts:

1. `collect_teams.py` - Retrieves information about all 30 NBA teams including their conference affiliation.

2. `collect_nba_games.py` - Collects and cleans comprehensive game data from the 2017-18 through 2023-24 NBA seasons. This script:
   - Retrieves complete game data from the NBA API
   - Filters to include only official NBA teams
   - Removes preseason, All-Star, and exhibition games
   - Validates the data against expected game counts for each season
   - Produces a clean dataset containing only regular season and playoff games

*Note: This represents a consolidation of several iterative scripts developed during the learning process. The earlier versions have been archived.*