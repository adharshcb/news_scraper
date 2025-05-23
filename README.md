# News Scraper from Webpages using Python

#### This Python script (`main.py`) scrapes news articles from a specified website and saves them to a SQLite database. It uses the `requests` module to fetch HTML content and `BeautifulSoup` to parse it, extracting article links, titles, content, and dates.

### Features
*   **Modular Code:** Well-structured with functions for clarity and maintainability.
*   **Robust Error Handling:** Implements `try-except` blocks for network operations, content parsing, and database interactions, logging issues for easier debugging.
*   **Configurable Target URL:** The website URL to scrape can be provided as a command-line argument.
*   **Comprehensive Logging:** Utilizes the `logging` module (INFO level) to provide insights into the script's execution and any encountered problems.
*   **Respectful Scraping Practices:**
    *   Sets a custom `User-Agent` string to identify the script.
    *   Incorporates a 1-second delay between fetching individual article details to minimize server load.

### Requirements
This script requires the following Python modules:

*   `requests`
*   `beautifulsoup4` (often imported as `bs4`)

The `sqlite3` (for database interaction) and `argparse` (for command-line arguments) modules are part of the Python standard library and do not require separate installation.

You can install the necessary modules using the `requirement.txt` file:
```bash
pip install -r requirement.txt
```
Alternatively, you can install them individually:
```bash
pip install requests beautifulsoup4
```

### Usage
1.  Clone the repository or download the `main.py` script.
2.  Install the required modules as described above.
3.  Run the script from your terminal:
    ```bash
    python main.py [URL]
    ```
    *   `[URL]` is an optional argument. If you provide a URL (e.g., `https://www.example-news.com/`), the script will attempt to scrape news from that address.
    *   If `[URL]` is not provided, the script will default to scraping `https://www.webpage.com/`.

    **Example with a custom URL:**
    ```bash
    python main.py https://www.anothernewssite.com/
    ```
    **Example using the default URL:**
    ```bash
    python main.py
    ```
4.  The script will create a SQLite database file named `mydatabase.db` in the same directory. This database will contain a table named `news` with the scraped articles.

## Note
*   This script is intended for educational purposes. Always ensure you have permission to scrape a website, and be mindful of its terms of service. Responsible scraping is crucial.
*   The HTML structure of websites can change frequently. This may require updates to the parsing logic within the script (e.g., the CSS class `item-title` for links, or `itemprop="dateModified"` for dates) to ensure continued functionality.
