import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time


def fetch_and_save_html(url, folder, delay=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
        file_name = os.path.join(folder, url.split('/')[-1] + '.html')
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(html_content)
        return html_content
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None
    finally:
        time.sleep(delay)  # Delay to avoid hitting the rate limit


def main():
    url = 'https://www.basketball-reference.com/playoffs/NBA_2023_advanced.html'
    folder = 'basketball_reference_html'
    os.makedirs(folder, exist_ok=True)

    main_page_html = fetch_and_save_html(url, folder)
    if main_page_html:
        soup = BeautifulSoup(main_page_html, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if href.startswith('/leagues/') and href.endswith('.html'):
                fetch_and_save_html('https://www.basketball-reference.com' + href, folder)


if __name__ == '__main__':
    main()
