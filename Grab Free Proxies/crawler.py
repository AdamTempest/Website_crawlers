import logging
import requests
from os import system
from bs4 import BeautifulSoup
from random import choice, randint
from urllib.parse import urljoin

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',level=logging.INFO)

proxyList = {
    'http': {},
    'https':{}
}

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

def getProxy():
    proxies = {
    'http':'',
    'https':''}
    http_country = choice([i for i in proxyList['http'].keys()])
    https_country = choice(list(proxyList['https'].keys()))

    http_length = len(proxyList['http'][http_country])
    https_length = len(proxyList['https'][https_country])

    http_max = http_length-1 if http_length>0 else http_length
    https_max = https_length-1 if https_length>0 else https_length

    proxies['http'] = proxyList['http'][http_country][randint(0,http_max)]
    proxies['https'] = proxyList['https'][https_country][randint(0,https_max)]

    return proxies


# read file with the following format: https http://125.125.125.125:80 UA
def addToProxyList(filename):
    with open(filename,'r') as f:
        data = f.readlines()
    
    for i in range(0,len(data)):
        l = data[i].split()
        try:
            proxyList[l[0]][l[2]].append(l[1])
        except KeyError as error:
            proxyList[l[0]][l[2]] = [l[1]]
        # ['http'][LocationCode].append('http://ip:port')
        # LocationCode examples: UA, RU, NL, FR etc


# main function
def crawl(url):
    proxies=getProxy()
    logging.info(f'Using {proxies} to crawl {url}')
    html = requests.get(url, proxies=proxies, timeout=3).text  # download_url
    
    logging.info(f'Successfully crawled {url} using {proxies}')

    soup = BeautifulSoup(html, 'html.parser')

    file = 'proxies_Fried_With_proxies'
    with open(file,'a') as f:
        logging.info(f'Initiated the database: {file}')
        for data in soup.find_all('tr'):
            column = [] # ip, port, code, country, provider, google, https, other
            if (isProxyData(str(data))):
                for col in data.find_all('td'):
                    content = getThecontent(str(col))
                    column.append(content)
                    
                logging.info(f'Cleaning the data: {column}')
                head = "https" if column[6] == "yes" else "http"
                f.write(f'{head} http://{column[0]}:{column[1]} {column[2]}\n')


if __name__ == '__main__':
    try:
        url = 'https://free-proxy-list.net/'
        logging.info(f'Crawling: {url}')
        addToProxyList("proxies_Fried_With_proxies")
        crawl(url)
    except Exception:
        logging.exception(f'Failed to crawl: {url}')