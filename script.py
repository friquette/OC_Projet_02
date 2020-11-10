import requests
from bs4 import BeautifulSoup
import csv
import os.path
import shutil

currentFolder = os.getcwd()
csvFolder = currentFolder + '/csv'
if not os.path.exists(csvFolder):
    os.mkdir(csvFolder)


def getContent(myPath):
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
        if description:
            descriptionBook = description.text
        else:
            descriptionBook = ''

        bookCategory = soupContent.findAll('li')[2]
        rating = soupContent.find('p', {'class': 'star-rating'}).get('class')

        urlImgRaw = soupContent.find('div', {'class': 'item active'}).find('img')
        urlImg = urlImgRaw.get('src')[6:]

        outp.write(linkBooks + ',' + upc.text + ',' + '"' + title.text + '"' + ',' + priceIncl.text[2:] + ',' +
                   priceExcl.text[2:] + ',' + str(nbr) + ',' + '"' + descriptionBook.replace('"', '""') + '"' + ',' +
                   bookCategory.text[1:-1] + ',' + ' '.join(rating)[12:] + ',' +
                   'http://books.toscrape.com/' + urlImg + '\n')

        urlImgFull = url + urlImg
        responseImage = requests.get(urlImgFull, stream=True)
        imageName = urlImgFull.split('/')[-1]

        if responseImage.ok:
            responseImage.raw.decode_content = True
            with open(myPath + '/' + imageName, 'wb') as f:
                shutil.copyfileobj(responseImage.raw, f)
        else:
            print('Image not found')


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
                categoryPath = csvFolder + '/' + nameCategory
                if not os.path.exists(categoryPath):
                    os.makedirs(categoryPath)

                with open(categoryPath + '/' + nameCategory + '.csv', 'w', encoding='utf-8') as outp:
                    booksFile = csv.writer(outp, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
                    outp.write('product_page_url, universal_product_code, title, '
                               'price_including_tax, price_excluding_tax, number_available,'
                               'product_description, category, review_rating, image_url\n')

                    getContent(categoryPath)

            else:
                categoryPath = csvFolder + '/' + nameCategory
                if not os.path.exists(categoryPath):
                    os.mkdir(categoryPath)

                with open(categoryPath + '/' + nameCategory + '.csv', 'w', encoding='utf-8') as outp:
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

                            getContent(categoryPath)

                        if not responsePages.ok:
                            break
