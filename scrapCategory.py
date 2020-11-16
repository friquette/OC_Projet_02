import requests
from bs4 import BeautifulSoup
import csv
import os.path
import scrapBook


def getLinkBooks(urlBooks, url, outp, categoryPath):
    for urlBook in urlBooks:
        aBooks = urlBook.find('a')
        linkBook = aBooks['href']
        linkBooks = url + 'catalogue/' + linkBook[9:]

        scrapBook.writeContent(outp, categoryPath, linkBooks, url)


def browsePages(urlCategories, csvFolder, url):
        responseBooks = requests.get(urlCategories)
        if responseBooks.ok:

            soupBooks = BeautifulSoup(responseBooks.text, 'html.parser')
            urlBooks = soupBooks.findAll('div', {'class': 'image_container'})

            classNext = soupBooks.find('li', {'class': 'next'})
            nameCategory = urlCategories[51:-1].strip('_0123456789')

            if not classNext:
                categoryPath = csvFolder + '/' + nameCategory
                print(csvFolder)
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
