"""This module scrapes a category webpage."""
import requests
from bs4 import BeautifulSoup
import csv
import os.path
import scrapeBook


def getLinkBooks(urlBooks, url, outp, categoryPath):
    """Retrieves urls of all books in the pages

    Retrieves url of each book in all books urls of the pages.
    Calls the writeContent function of the scrapeBook module.
    Parameters:
    urlsBooks -- list of all books urls
    url -- url of the page to scrape
    outp -- name of the csv file to write in
    categoryPath -- path of the folder to save the files in

    """

    for urlBook in urlBooks:
        aBooks = urlBook.find('a')
        linkBook = aBooks['href']
        linkBooks = url + 'catalogue/' + linkBook[9:]

        scrapeBook.writeContent(outp, categoryPath, linkBooks, url)


def browsePages(urlCategories, csvFolder, url):
    """Browses all the pages of the category

    Parses the page.
    If the tag class 'next' isn't in the page, calls the getLinkBooks function.
    If the tag class 'next' is in the page, increment the 'page-x' part of the url while
    the condition is true. Then calls the getLinkBooks function.
    Parameters:
    urlCategories -- list of all categories urls
    csvFolder -- the path the files will be saved into
    url -- url of the page to scrape

    """

    responseBooks = requests.get(urlCategories)
    if responseBooks.ok:
        soupBooks = BeautifulSoup(responseBooks.text, 'html.parser')
        urlBooks = soupBooks.findAll('div', {'class': 'image_container'})

        classNext = soupBooks.find('li', {'class': 'next'})
        nameCategory = urlCategories[51:-1].strip('_0123456789')

        if not classNext:
            categoryPath = csvFolder + '/' + nameCategory
            if not os.path.exists(categoryPath):
                os.makedirs(categoryPath)

            with open(categoryPath + '/' + nameCategory + '.csv', 'w', encoding='utf-8') as outp:
                csv.writer(outp, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
                outp.write('product_page_url, universal_product_code, title, '
                           'price_including_tax, price_excluding_tax, number_available,'
                           'product_description, category, review_rating, image_url\n')

                getLinkBooks(urlBooks, url, outp, categoryPath)

        else:
            i = 0
            categoryPath = csvFolder + '/' + nameCategory
            if not os.path.exists(categoryPath):
                os.mkdir(categoryPath)

            with open(categoryPath + '/' + nameCategory + '.csv', 'w', encoding='utf-8') as outp:
                csv.writer(outp, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
                outp.write('product_page_url, universal_product_code, title, '
                           'price_including_tax, price_excluding_tax, number_available,'
                           'product_description, category, review_rating, image_url\n')
                while True:
                    i += 1
                    urlPages = urlCategories + 'page-' + str(i) + '.html'
                    responsePages = requests.get(urlPages)

                    if responsePages.ok:
                        soupPages = BeautifulSoup(responsePages.text, 'html.parser')
                        urlBooks = soupPages.findAll('div', {'class': 'image_container'})

                        getLinkBooks(urlBooks, url, outp, categoryPath)

                    if not responsePages.ok:
                        break


def main(url):
    """Used if the module is executed as a script.

    Reads the config.txt file to find the path where the results will be saved (the project root
    folder by default).
    Calls the browsePages function.
    Parameter:
    url -- the page url to scrape

    """

    mainUrl = 'http://books.toscrape.com/'

    with open('config.txt', 'r') as conf:
        csvFolder = conf.read().strip(' \n')
        if csvFolder == '':
            currentFolder = os.getcwd()
            csvFolder = currentFolder + '/csv'
            if not os.path.exists(csvFolder):
                os.makedirs(csvFolder)
        else:
            if not os.path.exists(csvFolder):
                os.mkdir(csvFolder)

        response = requests.get(url)
        if response.ok:
            browsePages(url, csvFolder, mainUrl)


if __name__ == '__main__':
    with open('url.txt', 'r') as urlConf:
        url = urlConf.read().strip('\n')[:-10]
        if url == '':
            print('Please enter a valid url')
        else:
            main(url)
