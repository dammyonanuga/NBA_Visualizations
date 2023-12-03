import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    csv_file = 'combined_basketball_data.csv'  # Replace with the path to your dataset
    df = pd.read_csv(csv_file)

    # Convert 'Age' and 'PER' to numeric, if they are not already
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['PER'] = pd.to_numeric(df['PER'], errors='coerce')

    # Drop rows with missing values
    df.dropna(subset=['Age', 'PER', 'Player'], inplace=True)

    # Find LeBron James' data
    lebron = df[df['Player'] == 'LeBron James']

    # Remove LeBron James from the original dataframe for the general heatmap
    df = df[df['Player'] != 'LeBron James']

    # Plotting
    plt.figure(figsize=(12, 8))

    # Create a heatmap for all players
    sns.kdeplot(data=df, x='Age', y='PER', fill=True, cmap='Purples', thresh=0)

    # Overlay LeBron James in red
    plt.scatter(lebron['Age'], lebron['PER'], color='red', label='LeBron James', s=50, edgecolor='white')

    # Highlight LeBron James as the oldest player (assuming he is)
    if not lebron.empty:
        oldest_age = lebron['Age'].values[0]
        plt.axvline(x=oldest_age, color='red', linestyle='--', label='Oldest Player')

    plt.colorbar(label='Density')
    plt.xlabel('Age')
    plt.ylabel('Player Efficiency Rating (PER)')
    plt.title('Heatmap of Player Age vs PER - Highlighting LeBron James')
    plt.legend()
    plt.grid(False)
    plt.show()

if __name__ == '__main__':
    main()