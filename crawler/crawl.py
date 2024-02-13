import os
import os.path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3  # Import SQLite library

# Constant variables
BASE_PORTAL_URI = "https://pureportal.coventry.ac.uk/en/organisations/ihw-centre-for-health-and-life-sciences-chls"
INDEX_PATH = "./storage/"
DB_FILE = "./storage/publications.db"
# create the INDEX_PATH directory if it does not exist
if not os.path.exists(INDEX_PATH):
    os.mkdir(INDEX_PATH)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create a sqlite table to store publication information
cursor.execute('''CREATE TABLE IF NOT EXISTS publications 
                (title TEXT PRIMARY KEY, author TEXT, year TEXT, publication_url TEXT, author_profile_url TEXT)''')

# fetch data from the Coventry University Research Centre for Health and Life Sciences (RCHL) portal using BS4

# Fetch the page containing the list of publications
response = requests.get(BASE_PORTAL_URI)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract publication information using bs4 find
for div_publication_tag in soup.find_all('div', class_='result-container'):
    h3_title_tag = div_publication_tag.find('h3', class_="title")

    if h3_title_tag:
        title = h3_title_tag.get_text(strip=True)
    else:
        title = "N/A"

    a_link_person_tag = div_publication_tag.find_all('a', class_='link person')
    authors = [author.text.strip()
               for author in a_link_person_tag] if a_link_person_tag else ["N/A"]

    span_date_tag = div_publication_tag.find('span', class_='date')
    year = span_date_tag.text.strip() if span_date_tag else "N/A"

    a_title_tag = div_publication_tag.find('a', class_='title')
    publication_url = urljoin(
        BASE_PORTAL_URI, a_title_tag['href']) if a_title_tag else "N/A"

    a_link_person_tag = div_publication_tag.find(
        'a', class_='link person')
    author_profile_url = urljoin(
        BASE_PORTAL_URI, a_link_person_tag['href']) if a_link_person_tag else "N/A"

    try:
        # Insert data into SQLite table
        print(f"Inserting: {title}")
        cursor.execute("INSERT OR REPLACE INTO publications VALUES (?, ?, ?, ?, ?)",
                       (title, ",".join(authors), year, publication_url, author_profile_url))

    except Exception as e:
        print(f"Error: {e}")
print("Committing please wait...")
conn.commit()
conn.close()
# Commit changes to the index
print("Finished")
