import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_wordcloud(names, title):
    """ Create and display a word cloud from a list of names. """
    # Convert all names to strings (to handle any non-string values)
    names_str = [str(name) for name in names if isinstance(name, str)]
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(names_str))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()

def main():
    csv_file = 'combined_basketball_data.csv'  # Replace with your CSV file path
    name_column = 'Player'  # Replace with the column name that contains full names

    # Read CSV file
    df = pd.read_csv(csv_file)

    # Extract first and last names
    df[name_column].dropna(inplace=True)
    names_split = df[name_column].str.split()
    first_names = names_split.str[0]
    last_names = names_split.str[-1]

    # Filter out the word "Player" from first names
    first_names = first_names[first_names != "Player"]
    last_names = last_names[last_names != "Player"]
    last_names = last_names[last_names != "Jr."]

    # Create word clouds
    create_wordcloud(first_names, 'Word Cloud of First Names')
    create_wordcloud(last_names, 'Word Cloud of Last Names')

    # Find and print the most popular names
    most_popular_first_name = first_names.value_counts().idxmax()
    count_most_popular_first = first_names.value_counts().max()
    most_popular_last_name = last_names.value_counts().idxmax()
    count_most_popular_last = last_names.value_counts().max()

    print(f"The most popular first name is '{most_popular_first_name}' with {count_most_popular_first} occurrences.")
    print(f"The most popular last name is '{most_popular_last_name}' with {count_most_popular_last} occurrences.")

if __name__ == '__main__':
    main()
