import requests
from bs4 import BeautifulSoup
import csv
import os.path
import scrapBook

def getCategories(categories, url, csvFolder):
    for category in categories:
        i = 0

        a = category.find('a')
        link = a['href']
        links = url + link

        urlCategories = links[0:-10]
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

                    for urlBook in urlBooks:
                        aBooks = urlBook.find('a')
                        linkBook = aBooks['href']
                        linkBooks = url + 'catalogue/' + linkBook[9:]

                        scrapBook.writeContent(outp, categoryPath, linkBooks, url)
            else:
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

                            for urlBook in urlBooks:
                                aBooks = urlBook.find('a')
                                linkBook = aBooks['href']
                                linkBooks = url + 'catalogue/' + linkBook[9:]

                                scrapBook.writeContent(outp, categoryPath, linkBooks, url)

                        if not responsePages.ok:
                            break