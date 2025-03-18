# NBA Teams Data Dictionary

This document provides detailed information about all fields in the NBA teams dataset used in our prediction system.

## Data Source
Team data is collected from the NBA API using two endpoints:
- Basic team information from `nba_api.stats.static.teams`
- Conference affiliation from `nba_api.stats.endpoints.leaguestandings`

## Data Fields

| Column | Data Type | Description | Business Meaning | Added In Version |
|--------|-----------|-------------|-----------------|------------------|
| id | Integer | Unique team identifier assigned by the NBA | Primary key used to link team data across different datasets | Initial collection |
| full_name | String | Complete official team name (e.g., "Boston Celtics") | The formal name used in official NBA communications | Initial collection |
| abbreviation | String | 2-3 letter team code (e.g., "BOS") | Short code used in schedules, statistics, and visual displays | Initial collection |
| nickname | String | Team nickname without city/location (e.g., "Celtics") | The portion of the team name that identifies the mascot/identity | Initial collection |
| city | String | City where the team is based | Geographic location information - may affect travel distance and home court advantage | Initial collection |
| state | String | State where the team is based | Geographic grouping information - may reveal regional patterns | Initial collection |
| year_founded | Integer | Year the franchise was established | Indicates franchise age and stability - potentially relevant for organizational factors | Initial collection |
| Conference | String | "East" or "West" designation | Primary competitive grouping that determines playoff qualification and seeding | Enhanced collection |

## Usage Notes

- Teams are assigned to one of two conferences: Eastern or Western
- Conference affiliation affects scheduling (teams play more games within their conference)
- Teams compete primarily within their conference for playoff positions
- Historical performance patterns may differ between conferences

## Data Transformation History
- **Initial Collection**: Basic team attributes from `teams.get_teams()`
- **Enhanced Collection**: Added Conference information by incorporating data from `leaguestandings.LeagueStandings()`

## Related Datasets
This teams dataset serves as a foundation for:
- Historical game analysis
- Team performance metrics
- Win probability predictions
- Player performance in team context

## Update Frequency
Team data is relatively static during a season but should be refreshed:
- At the beginning of each NBA season
- After any franchise relocations or expansions