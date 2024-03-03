import json
import logging
import threading
from datetime import datetime
import csv

from bs4 import BeautifulSoup
import requests

TOTAL_PAGES = 62


# Generate a timestamp
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f'./logs/logfile_{current_time}.log'

# Configure logging to use the timestamped log file
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# fetch from string url 
def fetch_page(url):
    req = requests.get(url)
    return req

def extract_from_page(html_snippet):
    soup = BeautifulSoup(html_snippet, 'html.parser')
    publications = soup.find_all('div', class_='content-list-item no-feature')
    logging.info(f"Found {len(publications)} publications to process.")
    publications_data = {}

    for publication in publications:
        try:
            csl_entry = publication.find('div', class_='csl-entry').text
            logging.debug(f"Processing entry: {csl_entry[:30]}...")
            author_names, title_year = csl_entry.split('.”')[0].split('. “')
            title, year = title_year.rsplit(' ', 1)
            link = publication.find('a', href=True)['href']
            key = f"{title} - {author_names}"
            publications_data[key] = {
                "Author Names": author_names,
                "Title": title,
                "Link": link,
                "Year": year.strip()
            }
            logging.info(f"Successfully processed: {key}")
        except Exception as e:
            logging.error(f"Error processing entry: {e}")
            logging.error(f"Error on key:\t{key}")
    return publications_data


def extract_publications(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    publications = soup.find_all('div', class_='csl-entry')
    publications_data = {}

    for publication in publications:
        # Extracting author names
        author_names = publication.text.split('.')[0]

        # Extracting the title of the article
        title = publication.find('a').text

        # Extracting the link to the publication
        link = publication.find('a', href=True)['href']

        # Using title and author names as a unique key
        key = f"{title} - {author_names}"
        publications_data[key] = {
            "Author Names": author_names,
            "Title": title,
            "Link": link
        }
        

    return publications_data


def fetch_publication_page(page):
    url = f"https://ffcws.princeton.edu/publications?page={page}&order=asc&sort=author&filters%5Btype%5D%5Bjournal_article%5D=journal_article"
    response = requests.get(url)

    if response.status_code == 200:
        logging.info(f"Successfully retrieved page {page}")
        return response.text  # Return the HTML content
    else:
        logging.error(f"Failed to retrieve page {page}")
        return None

def fetch_and_write_all_publications():
    def worker(page):
        try:
            html_content = fetch_publication_page(page)
            if html_content:
                # Assuming extract_publications processes and returns data
                page_data = extract_from_page(html_content)
                publications_data.update(page_data)
        except Exception as e:
            logging.error(f"Error fetching page {page}: {e}")

    publications_data = {}
    page = 0
    max_workers = 10
    threads = []

    while True:
        for _ in range(max_workers):
            thread = threading.Thread(target=worker, args=(page,))
            threads.append(thread)
            thread.start()
            page += 1
            if page > TOTAL_PAGES:  # Assuming TOTAL_PAGES is the total number of pages
                break

        for thread in threads:
            thread.join()

        if page > TOTAL_PAGES:
            break

        threads = []  # Reset the list for the next batch of threads

    # After fetching all pages, write to CSV
    write_to_csv(publications_data)


def write_to_csv(publications_data):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f'publications_{current_time}.csv'
    
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Title', 'Author Names', 'Link'])
        
        for key, value in publications_data.items():
            csv_writer.writerow([value['Title'], value['Author Names'], value['Link']])

if __name__ == "__main__":
    # fetch_all_publications_concurrently()
    fetch_and_write_all_publications()
    