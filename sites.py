import urllib
from bs4 import BeautifulSoup

def download(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"}) 
    con = urllib.request.urlopen(req)
    return con.read()


def scrap_positive():
    soup = BeautifulSoup(download('http://www.theporndude.com'), 'html.parser')
    links = soup.findAll('a', attrs={'class': 'link link-analytics'}, href=True)
    links = list(map(lambda x: x['href'], links))
    links = list(filter(lambda x: 'http' in x, links))
    return links


def scrap_negative():
    soup = BeautifulSoup(download('https://fossbytes.com/most-useful-websites-internet'), 'html.parser')
    content = soup.find('div', attrs={'class': 'td-post-content td-pb-padding-side'})
    links = content.findAll('a', href=True)
    links = list(map(lambda x: x['href'], links))
    links = list(filter(lambda x: 'http' in x, links))
    return links


# Websites that write about sex but not porn
def scrap_sensitive_negative():
    soup = BeautifulSoup(download('https://sexetc.org/blog/?pageNum=100'), 'html.parser')
    links = soup.findAll('a', attrs={'class': 'image-link'}, href=True)
    links = list(map(lambda x: x['href'], links))
    links = list(filter(lambda x: 'http' in x, links))
    return links

