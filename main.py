

from bs4 import BeautifulSoup
import requests
import sqlite3
import logging # Added for logging
import argparse # Added for command-line arguments
import time # Added for respectful scraping delays

# Removed selenium import as it's not used
# Removed sys import as it's no longer needed

USER_AGENT = "NewsScraperBot/1.0 (Educational project; contact: your_email@example.com or project_url)"

def init_db(db_name="mydatabase.db"):
    """
    Initializes the SQLite database and creates the news table if it doesn't exist.
    Returns the connection and cursor objects.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (id INTEGER PRIMARY KEY, date TEXT, title TEXT, content TEXT)''')
    return conn, c

def scrape_article_links(page_url):
    """
    Fetches the page content and returns a list of article URLs.
    """
    try:
        source = requests.get(page_url, headers={'User-Agent': USER_AGENT})
        source.raise_for_status() # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching page {page_url}: {e}")
        return []

    soup = BeautifulSoup(source.text, 'html.parser')
    links_found = soup.find_all('a', attrs={'class': 'item-title'})

    if not links_found:
        logging.warning(f"No article links found on {page_url} with class 'item-title'.")
        return []

    article_links = []
    for link in links_found:
        article_links.append(link.get('href'))
    return article_links

def scrape_article_details(article_url):
    """
    Fetches article details (title, content, date) from the article URL.
    Returns a dictionary with the scraped details or None if scraping fails.
    """
    try:
        news = requests.get(article_url, headers={'User-Agent': USER_AGENT})
        news.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching article {article_url}: {e}")
        return None # Return None if the page fetch fails

    soup2 = BeautifulSoup(news.text, 'html.parser')

    title_element = soup2.find('title')
    if title_element:
        title = title_element.get_text()
    else:
        title = 'not found'
        logging.warning(f"Title not found for article {article_url}")

    content_element = soup2.find('p')
    if content_element:
        content = content_element.get_text()
    else:
        content = 'not found'
        logging.warning(f"Content not found for article {article_url}")

    date = 'not found' # Default date
    try:
        date_element = soup2.find('span', attrs={'itemprop': "dateModified"})
        if date_element:
            date_text = date_element.get_text()
            # Attempt to split, handle potential errors if 'Updated: ' is not present
            if 'Updated: ' in date_text:
                 date = date_text.split('Updated: ')[1]
            else:
                date = date_text # Use the whole text if 'Updated: ' is not present
                logging.warning(f"'Updated: ' prefix not found in date string for {article_url}. Using full date string: {date_text}")
        else:
            logging.warning(f"Date element not found for article {article_url}")
    except Exception as e: # Catch any other unexpected error during date processing
        logging.warning(f"Could not parse date for article {article_url}. Error: {e}")
        # date remains 'not found'

    return {'title': title, 'content': content, 'date': date}

def save_article_to_db(cursor, title, content, date):
    """
    Saves the article details to the database.
    """
    try:
        cursor.execute("INSERT INTO news (date, title, content) VALUES (?, ?, ?)", (date, title, content))
    except sqlite3.Error as e:
        logging.error(f"Error saving article to database: {e}")
        logging.error(f"Article details: Title='{title}', Date='{date}'")


def main():
    """
    Main function to orchestrate the scraping and database operations.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description="Scrapes news articles from a website and saves them to a SQLite database.")
    parser.add_argument("url", nargs='?', default="https://www.webpage.com/",
                        help="The base URL of the news website to scrape. Defaults to https://www.webpage.com/")
    args = parser.parse_args()

    # Use the URL from command-line arguments
    url = args.url
    logging.info(f"Starting scraper for URL: {url}")

    conn, c = init_db()
    if conn is None: # Check if db initialization failed
        logging.critical("Database could not be initialized. Exiting.") # Changed to critical
        return

    article_urls = scrape_article_links(url)

    if not article_urls:
        logging.info("No articles found to process. Exiting.") # Changed to info
        conn.close()
        return

    articles_processed_count = 0
    for article_url in article_urls:
        if not article_url: # Skip if URL is None or empty
            logging.warning(f"Empty or None article URL found. Skipping.")
            continue
        logging.info(f"Scraping article: {article_url}")
        details = scrape_article_details(article_url)
        if details: # Proceed only if details were successfully scraped
            save_article_to_db(c, details['title'], details['content'], details['date'])
            articles_processed_count +=1
            logging.info(f"Successfully scraped and initiated save for: {article_url}")
        else:
            logging.warning(f"Skipping article from {article_url} due to previous errors during scraping.")
        
        logging.info("Waiting for 1 second before next request...")
        time.sleep(1) # Wait for 1 second

    if articles_processed_count > 0:
        try:
            conn.commit()  # Commit once after all articles are processed
            logging.info(f"Successfully processed and saved {articles_processed_count} articles.")
        except sqlite3.Error as e:
            logging.error(f"Error committing changes to database: {e}")
    else:
        logging.info("No articles were successfully processed and saved to the database.")

    conn.close()
    logging.info("Scraping process finished.")

if __name__ == '__main__':
    main()
