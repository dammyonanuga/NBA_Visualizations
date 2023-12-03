import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    csv_file = 'combined_basketball_data.csv'  # Replace with the path to your dataset
    df = pd.read_csv(csv_file)

    # Convert 'TS%' and 'PER' to float
    # Assuming TS% is already in decimal form as '.530'
    df['TS%'] = pd.to_numeric(df['TS%'], errors='coerce')
    df['PER'] = pd.to_numeric(df['PER'], errors='coerce')

    # Drop rows with missing values
    df.dropna(subset=['PER', 'TS%', 'Pos'], inplace=True)

    # Plotting
    plt.figure(figsize=(12, 8))

    # Create a scatter plot
    sns.scatterplot(data=df, x='TS%', y='PER', hue='Pos', alpha=0.6, edgecolor=None)

    # Create a KDE plot
    sns.kdeplot(data=df, x='TS%', y='PER', hue='Pos', fill=True, palette='cool', alpha=0.5)

    plt.title('Player Efficiency Rating (PER) vs True Shooting Percentage (TS%) by Position')
    plt.xlabel('True Shooting Percentage (TS%)')
    plt.ylabel('Player Efficiency Rating (PER)')
    plt.legend(title='Position')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
