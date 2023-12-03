import os
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def parse_html_to_dataframe(html_content):
    """ Parse HTML content and return a list of DataFrames for each table in the HTML. """
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    dataframes = []

    for table in tables:
        # Use StringIO to simulate a file object
        table_html = str(table)
        df = pd.read_html(StringIO(table_html))[0]
        dataframes.append(df)

    return dataframes


def main():
    folder = 'basketball_reference_html'
    all_dfs = []  # List to hold all dataframes

    for filename in os.listdir(folder):
        if filename.endswith('.html'):
            file_path = os.path.join(folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                dfs = parse_html_to_dataframe(html_content)
                all_dfs.extend(dfs)  # Add the list of dataframes to the main list

    # Combine all dataframes
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Saving the combined data to a CSV file
    combined_df.to_csv('combined_basketball_data.csv', index=False)


if __name__ == '__main__':
    main()
