import matplotlib.pyplot as plt
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats
import numpy as np
import pandas as pd

# Helper function to get season stats
def get_season_stats(team_name, season='2022-23'):
    team_info = teams.find_teams_by_full_name(team_name)[0]
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_info['id'], season_type_all_star='Regular Season', per_mode_simple='Totals')
    season_stats = team_stats.get_data_frames()[0]
    season_stats = season_stats[season_stats['YEAR'] == season]
    return season_stats

# Fetch stats for both teams
nuggets_stats = get_season_stats('Denver Nuggets')
celtics_stats = get_season_stats('Boston Celtics')

# Get wins, losses, and total points
nuggets_wins = nuggets_stats['WINS'].values[0]
nuggets_losses = nuggets_stats['LOSSES'].values[0]
nuggets_points = nuggets_stats['PTS'].values[0]

celtics_wins = celtics_stats['WINS'].values[0]
celtics_losses = celtics_stats['LOSSES'].values[0]
celtics_points = celtics_stats['PTS'].values[0]

# Create a simple bar chart
fig, ax = plt.subplots(figsize=(10, 7))

# Set position of bar on X axis
bar_width = 0.35
ind = np.arange(2)

# Make the plot
ax.bar(ind, [nuggets_wins, celtics_wins], bar_width, label='Wins', color='green')
ax.bar(ind, [nuggets_losses, celtics_losses], bar_width, label='Losses', color='red', bottom=[nuggets_wins, celtics_wins])

# Add total points as text labels
ax.text(0, (nuggets_wins + nuggets_losses)/2, f'Total Points: {nuggets_points}', ha='center', color='white')
ax.text(1, (celtics_wins + celtics_losses)/2, f'Total Points: {celtics_points}', ha='center', color='white')

# Add some text for labels, title and axes ticks
ax.set_xlabel('Teams')
ax.set_ylabel('Number of Wins/Losses')
ax.set_title('2022/2023 Season Wins/Losses and Total Points')
ax.set_xticks(ind)
ax.set_xticklabels(['Denver Nuggets', 'Boston Celtics'])
ax.legend()

plt.show()
