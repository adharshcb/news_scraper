# Scraping News from websites using Python
#### This Python script scrapes news articles from the news website and saves them to a SQLite database. The script uses the requests module to get the HTML content of the website and BeautifulSoup to parse the HTML and extract the news article links. It then uses selenium to navigate to each news article page and extract the title, content, and date information.

### Requirements
This script requires the following Python modules:

* requests
* bs4 (BeautifulSoup)
* selenium
* sqlite3

You can install them using the following commands:
```
pip install requests
pip install bs4
pip install selenium
```
### Usage
Clone the repository or download the script news_scraper.py.

Install the required modules as mentioned above.

Run the script using the following command:
```
python news_scraper.py
```
The script will create a SQLite database named mydatabase.db in the same directory and save the news articles in a table named news.


## Note
#### * This script is for educational purposes only. Scraping websites may be against their terms of service, so use it at your own risk.
#### * The HTML structure of websites may change over time, so the script may not work as expected in the future.
