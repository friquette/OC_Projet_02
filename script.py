import requests
from bs4 import BeautifulSoup
import csv


def getContent():
    for urlBook in urlBooks:
        aBooks = urlBook.find('a')
        linkBook = aBooks['href']
        linkBooks = url + 'catalogue/' + linkBook[9:]

        responseContent = requests.get(linkBooks)
        soupContent = BeautifulSoup(responseContent.text, 'html.parser')

        trs = soupContent.findAll('tr')
        upc = trs[0].find('td')
        priceIncl = trs[3].find('td')
        priceExcl = trs[2].find('td')

        nbrAvailable = trs[5].find('td')
        nbr = int(''.join(filter(str.isdigit, nbrAvailable.text)))

        title = soupContent.find('h1')
        description = soupContent.find('p', {'class': ''})

        bookCategory = soupContent.findAll('li')[2]
        rating = soupContent.find('p', {'class': 'star-rating'}).get('class')

        urlImgRaw = soupContent.find('div', {'class': 'item active'}).find('img')
        urlImg = urlImgRaw.get('src')[6:]

        outp.write(linkBooks + ',' + upc.text + ',' + '"' + title.text + '"' + ',' + priceIncl.text[2:] + ',' +
                   priceExcl.text[2:] + ',' + str(nbr) + ',' + '"' + description.text.replace('"', '""') + '"' + ',' +
                   bookCategory.text[1:-1] + ',' + ' '.join(rating)[12:] + ',' +
                   'http://books.toscrape.com/' + urlImg + '\n')


url = 'http://books.toscrape.com/'
response = requests.get(url)

if response.ok:
    soupCtg = BeautifulSoup(response.text, 'html.parser')
    menuCtg = soupCtg.findAll('ul', {'class': 'nav nav-list'})
    categories = menuCtg[0].find('ul').findAll('li')

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
                with open('csv/' + nameCategory + '.csv', 'w', encoding='ISO-8859-1') as outp:
                    booksFile = csv.writer(outp, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
                    outp.write('product_page_url, universal_product_code, title, '
                               'price_including_tax, price_excluding_tax, number_available,'
                               'product_description, category, review_rating, image_url\n')

                    getContent()

            else:
                with open('csv/' + nameCategory + '.csv', 'w', encoding='ISO-8859-1') as outp:
                    booksFile = csv.writer(outp, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
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

                            getContent()

                        if not responsePages.ok:
                            break
