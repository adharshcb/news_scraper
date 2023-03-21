

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import sqlite3



# website url
url="https://www.webpage.com/"



# Connect to database or create it if it doesn't exist
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create a table to store data
c.execute('''CREATE TABLE IF NOT EXISTS news
             (id INTEGER PRIMARY KEY, date TEXT, title TEXT, content TEXT)''')

source=requests.get(url)

# BeautifulSoup is used for getting HTML structure from requests response.(craete your soup)
soup=BeautifulSoup(source.text,'html.parser')

for link in soup.find_all('a', attrs={'class':'item-title'}):#this class is specific for the specified webpage

    news = requests.get(link.get('href'))

    soup2 = BeautifulSoup(news.text,'html.parser')

    title = soup2.find('title').get_text()
    content = soup2.find('p').get_text()
    try:
        date = soup2.find('span', attrs={'itemprop':"dateModified"}).get_text().split('Updated: ')[1]#attrs is specific for this webpage
    except:
        date = 'not found'

    c.execute("INSERT INTO news (date, title, content) VALUES (?, ?, ?)", (date,title,content))
    conn.commit()

conn.close()
