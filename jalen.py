from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc

# Function to draw the basketball court
def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so radius is 9"
    hoop = Circle((0, 0), radius=9, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # Create the inner box of the paint, width=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')

    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    # List of the court elements to be drawn
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

# Get player data
player_dict = players.get_players()
jalen_green = [player for player in player_dict if player['full_name'] == 'Jalen Green'][0]
player_id = jalen_green['id']

# Get shot chart data
shot_chart = shotchartdetail.ShotChartDetail(team_id=0, player_id=player_id, season_nullable='2022-23', season_type_all_star='Regular Season')
shots = shot_chart.get_data_frames()[0]

# Separate shots into categories
shots_3pt_made = shots[(shots.SHOT_TYPE == '3PT Field Goal') & (shots.SHOT_MADE_FLAG == 1)]
shots_3pt_attempted = shots[(shots.SHOT_TYPE == '3PT Field Goal') & (shots.SHOT_MADE_FLAG == 0)]
shots_2pt_made = shots[(shots.SHOT_TYPE == '2PT Field Goal') & (shots.SHOT_MADE_FLAG == 1)]
shots_2pt_attempted = shots[(shots.SHOT_TYPE == '2PT Field Goal') & (shots.SHOT_MADE_FLAG == 0)]

# Plot the shot chart data
sns.set_style('white')
sns.set_color_codes()
plt.figure(figsize=(12, 11))

# Plot 3PT shots
plt.scatter(shots_3pt_made.LOC_X, shots_3pt_made.LOC_Y, s=20, marker='o', color='green', label='3PT Shots Made')
plt.scatter(shots_3pt_attempted.LOC_X, shots_3pt_attempted.LOC_Y, s=20, marker='o', color='lime', label='3PT Shots Attempted')

# Plot 2PT shots
plt.scatter(shots_2pt_made.LOC_X, shots_2pt_made.LOC_Y, s=20, marker='s', color='blue', label='2PT Shots Made')
plt.scatter(shots_2pt_attempted.LOC_X, shots_2pt_attempted.LOC_Y, s=20, marker='s', color='skyblue', label='2PT Shots Attempted')

# Draw the court
draw_court(outer_lines=True)

# Adjust plot limits to just show half court
plt.xlim(-250, 250)
plt.ylim(422.5, -47.5)

# Add labels and title
plt.xlabel('Court X Coordinate')
plt.ylabel('Court Y Coordinate')
plt.title('Jalen Green Shot Chart 2022-2023 Season')

# Add a legend
plt.legend(loc='upper right')

# Show the plot
plt.show()
