import logging
import requests
from os import system
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',level=logging.INFO)

proxies = {
   'http': 'http://proxy.example.com:8080',
   'http': 'http://ip:port',
   'http': 'http://10.10.10.10:8000',
   'https': 'http://secureproxy.example.com:8090',
}

def readDB(filename):
	with open(filename, )

def crawl(url):
	html = requests.get(url, proxies=proxies).text
	soup = BeautifulSoup