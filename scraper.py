import urllib
import lxml
import re
import csv
import json

from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner

def download(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"}) 
    con = urllib.request.urlopen(req)
    return con.read()


def clean(content):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    result = cleaner.clean_html(content)
    return result


def beautify(content):
    soup = BeautifulSoup(content, 'html.parser')
    result = ' '.join(soup.findAll(text=True))
    result = result.replace('\n', '').replace('#', '').strip()
    result = ''.join([i for i in result if not i.isdigit()])
    result = ' '.join(result.split())
    return result


def to_words(content):
    result = re.sub('[^\w]', ' ',  content).split()
    result = [x.lower() for x in result]
    result = list(filter(lambda x: len(x) > 1, result))
    return result


def to_document(url):
    words = to_words(beautify(clean(download(url))))
    return ' '.join(words)


def write_data(positive, negative, name):
    data = [['words', 'adult']]
    for i in positive:
        data.append([';'.join(i), 'yes'])


    for i in negative:
        data.append([';'.join(i), 'no'])


    with open(name, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def append_data(positive, negative, name):
    data = []
    for i in positive:
        data.append([';'.join(i), 'yes'])


    for i in negative:
        data.append([';'.join(i), 'no'])


    with open(name, 'a') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def scrap_sensitve_data():
    print('Loading negative')        
    data = json.load(open('sensitive_sites.json'))
    negative = []
    for x in data['data']:
        try:
            content = to_words(beautify(clean(download(x))))
            negative.append(content)
            print('Done: ' + x)
        except: 
            print('Pass: ' + x)
            pass


    print('Storing data')
    append_data([], negative, 'input2.csv')
    print('Done')


def main():
    print('Loading positive')
    data = json.load(open('adult_sites.json'))
    positive = []
    for x in data['data']:
        try:
            content = to_words(beautify(clean(download(x))))
            positive.append(content)
            print('Done: ' + x)
        except: 
            print('Pass: ' + x)
            pass
        

    print('Loading negative')        
    data = json.load(open('normal_sites.json'))
    negative = []
    for x in data['data']:
        try:
            content = to_words(beautify(clean(download(x))))
            negative.append(content)
            print('Done: ' + x)
        except: 
            print('Pass: ' + x)
            pass


    print('Storing data')
    write_data(positive, negative, 'input.csv')
    print('Done')
