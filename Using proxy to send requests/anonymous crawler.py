import logging
import requests
from os import system
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',level=logging.INFO)

proxies = {
   'http': 'http://10.10.10.10:8000',
   'https': 'http://secureproxy.example.com:8090'
}

def readDB(filename):
   cleaned = []
   with open(filename, 'r') as f:
      data = f.readlines()
   for i in range(0,len(data)):
      cleaned.append(data[i][:-2].split(':'))
   

def crawl(url):
	html = requests.get(url, proxies=proxies).text
	soup = BeautifulSoup