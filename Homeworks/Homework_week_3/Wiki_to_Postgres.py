import requests
from bs4 import BeautifulSoup
import psycopg2

# Function to scrape the links from a Wikipedia page and return them as a list
def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    return [(link.get('href'), link.text) for link in links]

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password='mySecurePassword'
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Create a table to store the pages
cur.execute('''CREATE TABLE pages
               (id SERIAL PRIMARY KEY,
                title TEXT,
                url TEXT);''')

# Scrape the links from the Wikipedia homepage
homepage_links = scrape_links('https://en.wikipedia.org/wiki/Main_Page')

# Loop through the links and scrape all pages on the English version of Wikipedia
for link, title in homepage_links:
    if link.startswith('/wiki/'):
        page_url = 'https://en.wikipedia.org' + link
        page_links = scrape_links(page_url)
        cur.execute("INSERT INTO pages (title, url) VALUES (%s, %s);", (title, page_url))
        for link, title in page_links:
            if link.startswith('/wiki/'):
                subpage_url = 'https://en.wikipedia.org' + link
                cur.execute("INSERT INTO pages (title, url) VALUES (%s, %s);", (title, subpage_url))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
