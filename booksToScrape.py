"""This module scrapes all the http://books.toscrape.com website."""
import requests
from bs4 import BeautifulSoup
import os.path
import scrapeCategory


def main():
    """Scrapes the website homepage.

    Reads the config.txt file to find the path where the results will be saved (the project root
    folder by default).
    Parse the homepage and retrieves links of all categories.
    Calls the browsePages function of the scrapCategory module.

    """

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
        soupCtg = BeautifulSoup(response.text, 'lxml')
        menuCtg = soupCtg.findAll('ul', {'class': 'nav nav-list'})
        categories = menuCtg[0].find('ul').findAll('li')

        for category in categories:
            a = category.find('a')
            link = url + a['href']

            scrapeCategory.browsePages(link[0:-10], csvFolder, url)


if __name__ == '__main__':
    main()
