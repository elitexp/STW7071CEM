import os
import os.path
import time  # Import time module for delay
import re  # Import re module for regular expressions
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sqlite3  # Import SQLite library
from protego import Protego

# Constant variables
BASE_PORTAL_URI = "https://pureportal.coventry.ac.uk/en/organisations/ihw-centre-for-health-and-life-sciences-chls"
INDEX_PATH = "./storage/"
DB_FILE = "./storage/publications.db"
MAX_DEPTH = 3
# create the INDEX_PATH directory if it does not exist
if not os.path.exists(INDEX_PATH):
    os.mkdir(INDEX_PATH)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
visited_urls = set()  # Initialize an empty set to track visited URLs


def is_allowed_by_robots(robots_content, url):
    try:
        rp = Protego.parse(robots_content)
        return rp.can_fetch(url, "CRAWLER")
    except Exception as e:
        print(f"Error fetching robots.txt: {e}")
        return True  # Allow crawling if there's an error


# Create a sqlite table to store publication information
cursor.execute('''CREATE TABLE IF NOT EXISTS publications 
                (title TEXT PRIMARY KEY, author TEXT, year TEXT, publication_url TEXT)''')
# fetch data from the Coventry University Research Centre for Health and Life Sciences (RCHL) portal using BS4
# First fetch the robots.txt content
parsed_uri = urlparse(BASE_PORTAL_URI)
base_uri = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
robots_url = urljoin(base_uri, '/robots.txt')
robots_content = requests.get(robots_url).text
# Fetch the page containing the list of publications
if not is_allowed_by_robots(robots_content, BASE_PORTAL_URI):
    print("Crawling not allowed by robots.txt")
    exit()
# Delay before each request based on the specified Crawl-Delay in robots.txt
crawl_delay = 5  # Default crawl delay
matches = re.search(r'^Crawl-Delay:\s*(\d+)',
                    robots_content, re.MULTILINE | re.IGNORECASE)
if matches:
    crawl_delay = int(matches.group(1))


def fetch_publications(url, depth=1):
    print(f"{'-' * (depth-1)}Visiting: {url}")

    if url in visited_urls:
        print(f"{'-' * (depth-1)}URL {url} has already been visited.")
        return

    visited_urls.add(url)
    if (depth > MAX_DEPTH):
        print(f"{'-' * (depth-1)}MAX_DEPTH {MAX_DEPTH} reached.")
        return
    if not is_allowed_by_robots(robots_content, url):
        print(f"{'-' * (depth-1)}Crawling not allowed by robots.txt")
        return
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract publication information using bs4 find
    for div_publication_tag in soup.find_all('div', class_='result-container'):
        container_div_tag = div_publication_tag.find('div', class_='rendering')
        if container_div_tag:
            if 'rendering_person' in container_div_tag.get('class', []):
                # 'rendering_person' class is present in container_div_tag
                continue

        h3_title_tag = div_publication_tag.find('h3', class_="title")

        if h3_title_tag:
            title = h3_title_tag.get_text(strip=True)
        else:
            title = "N/A"

        a_link_person_tag = div_publication_tag.find_all(
            'a', class_='link person')
        authors = [author.text.strip()
                   for author in a_link_person_tag] if a_link_person_tag else ["N/A"]
        author_urls = [a_tag['href'] for a_tag in a_link_person_tag]

        span_date_tag = div_publication_tag.find('span', class_='date')
        year = span_date_tag.text.strip() if span_date_tag else "N/A"

        a_title_tag = div_publication_tag.find('a', class_='link')
        publication_url = urljoin(
            BASE_PORTAL_URI, a_title_tag['href']) if a_title_tag else "N/A"

        try:
            # Insert data into SQLite table
            # print(f"Publication: {title} with url {publication_url}")
            cursor.execute("INSERT OR REPLACE INTO publications VALUES (?, ?, ?, ?)",
                           (title, ",".join(authors), year, publication_url))
            conn.commit()
            for author_url in author_urls:
                fetch_publications(author_url,
                                   depth=depth+1)

        except Exception as e:
            print(f"Error: {e}")
        # Respect the time delay
        time.sleep(crawl_delay)


fetch_publications(BASE_PORTAL_URI)

conn.close()
# Commit changes to the index
print("Finished")
