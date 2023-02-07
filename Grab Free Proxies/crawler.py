import logging
import requests
from os import system
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
    return tag[i+1:-5] # <td>

# main function
def crawl(url):
    column = [] # ip, port, code, country, provider, google, https, other
    html = requests.get(url).text  # download_url
    soup = BeautifulSoup(html, 'html.parser')
    
    with open('proxy.list','a') as f:
        logging.info(f'Initiated database: proxy.list')
        for data in soup.find_all('tr'):
            if (isProxyData(str(data))):
                for col in data.find_all('td'):
                    content = getThecontent(str(col))
                    column.append(content)
                    logging.info(f'Adding to db: {content}')
                f.write(f'{column[6]} http://{column[0]}:{column[1]}')
                f.write('\n')
            else:
                pass


if __name__ == '__main__':
    url = 'https://free-proxy-list.net/'
    logging.info(f'Crawling: {url}')
    try:
        crawl(url)
    except Exception:
        logging.exception(f'Failed to crawl: {url}')