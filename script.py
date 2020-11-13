import requests
from bs4 import BeautifulSoup
import os.path
import scrapCategory

with open('config.txt', 'r') as conf:
    csvFolder = conf.read().strip(' \n')
    if csvFolder == '':
        currentFolder = os.getcwd()
        csvFolder = currentFolder + '/csv'
        if not os.path.exists(currentFolder):
            os.mkdir(csvFolder)
    else:
        if not os.path.exists(csvFolder):
            os.mkdir(csvFolder)

url = 'http://books.toscrape.com/'
response = requests.get(url)

if response.ok:
    soupCtg = BeautifulSoup(response.text, 'html.parser')
    menuCtg = soupCtg.findAll('ul', {'class': 'nav nav-list'})
    categories = menuCtg[0].find('ul').findAll('li')

    scrapCategory.getCategories(categories, url, csvFolder)
