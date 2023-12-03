from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats, commonteamroster
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Step 1: Get the list of NBA teams
nba_teams = teams.get_teams()

# Step 2: Fetch the number of wins for each team in the 2022-2023 season
team_wins = {}
for team in nba_teams:
    stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team['id'], season_type_all_star='Regular Season')
    year_stats = stats.get_data_frames()[0]
    current_season_stats = year_stats[year_stats['YEAR'] == '2022-23']
    # Make sure there's data for the current season
    if not current_season_stats.empty:
        team_wins[team['full_name']] = current_season_stats['WINS'].iloc[0]

# Step 3: Find the youngest player for each team and their position
team_youngest_players = {}
positions = {'Guard': 'Green', 'Forward': 'Blue', 'Center': 'Red', 'Forward-Center': 'Purple', 'Forward-Guard': 'Cyan', 'Guard-Forward': 'Yellow'}
position_colors = {}

for team in nba_teams:
    roster = commonteamroster.CommonTeamRoster(team_id=team['id'])
    players = roster.get_data_frames()[0]
    youngest_player = players.loc[players['AGE'].idxmin()]
    team_youngest_players[team['full_name']] = youngest_player['PLAYER']
    position_colors[youngest_player['PLAYER']] = positions.get(youngest_player['POSITION'], 'Black') # Default to 'Black' if position not found

# Step 4: Create the bar chart
fig, ax = plt.subplots(figsize=(20, 10)) # Adjusted for better visibility
teams = list(team_wins.keys())
wins = list(team_wins.values())

# Create a color map for the teams
colors = plt.cm.viridis(np.linspace(0, 1, len(teams)))

bars = ax.bar(teams, wins, color=colors)

# Step 5: Annotate each bar with the youngest player's name and position color, writing vertically
for bar, team in zip(bars, teams):
    y_val = bar.get_height()
    player = team_youngest_players[team]
    color = position_colors[player]
    # Write the player's name inside the bar vertically
    plt.text(bar.get_x() + bar.get_width()/2, y_val / 2, player, ha='center', va='center', rotation='vertical', color='white')

# Step 6: Add a legend for positions
legend_patches = [mpatches.Patch(color=color, label=position) for position, color in positions.items()]
plt.legend(handles=legend_patches, title='Player Positions', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add labels and title
plt.xlabel('Teams')
plt.ylabel('Wins')
plt.title('NBA Team Wins and Youngest Players (2022-2023 Season)')

# Show the plot
plt.xticks(rotation=90, ha='center')
plt.tight_layout()
plt.show()
