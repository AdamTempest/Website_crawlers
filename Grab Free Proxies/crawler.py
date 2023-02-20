import logging
import sqlite3
import requests
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',level=logging.INFO)

# See if the row has ip address or not
def isProxyData(row):
    i = 4
    while row[i] != '>':
        i+=1
    for i in range(i+1,i+5):
        if (row[i] == '.'):
            return True
    return False

# extract content inside html tags; <tag> content </tag>
def getThecontent(tag):
    i = 0
    while tag[i] != '>':
        i+=1
    return tag[i+1:-5]

def space_this_properly(a,b,c,d):
    
    while len(a) < 18:
        a += ' '
    while len(b) < 7:
        b += ' '
    while len(c) < 9:
        c += ' '

    return " "+a + b + c + d

def showData(c):
    logging.info('Data inside the database:')
    data = c.execute('SELECT * FROM Proxies ORDER BY port')
    for row in data:
        d = space_this_properly(str(row[0]),str(row[1]),str(row[2]),str(row[3]))
        logging.info(d)

# main function
def crawl(url):
    db_name='proxies.sqlite'
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS Proxies')
    cur.execute('CREATE TABLE Proxies (ip TEXT, port INTEGER, head TEXT, location TEXT)')
    
    logging.info(f'Initiated the database: {db_name}')

    html = requests.get(url).text  # download_url
    soup = BeautifulSoup(html, 'html.parser')
    logging.info(f'Successfully crawled {url}')

    for data in soup.find_all('tr'):
        column = [] 
        # ip, port, code, country, provider, google, https, other
        if (isProxyData(str(data))):
            for col in data.find_all('td'):
                content = getThecontent(str(col))
                column.append(content)

            head = "https" if column[6] == "yes" else "http"
            command = f"""INSERT INTO Proxies VALUES ("{column[0]}", "{column[1]}", "{head}", "{column[3]}");"""
            cur.execute(command)

            
    showData(cur)
    con.commit()
    cur.close()

if __name__ == '__main__':
    try:
        url = 'https://free-proxy-list.net/'
        logging.info(f'Crawling: {url}')
        crawl(url)
    except Exception:
        logging.exception(f'Failed to crawl: {url}')