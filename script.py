import requests
from bs4 import BeautifulSoup
import csv
import time

i = 0
links = []

while True:
    i += 1
    urls = 'http://books.toscrape.com/catalogue/category/books/fantasy_19/page-' + str(i) + '.html'
    response = requests.get(urls)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        urlBooks = soup.findAll('div', {'class': 'image_container'})
        classNext = soup.find('li', {'class': 'next'})

        for urlBook in urlBooks:
            a = urlBook.find('a')
            link = a['href']
            links.append('http://books.toscrape.com/catalogue/' + link[9:])

    if not response.ok:
        break

with open('urlsBooks.csv', 'w') as outp:
    books = csv.writer(outp, delimiter=',')
    for link in links:
        outp.write(link + '\n')

with open('urlsBooks.csv', 'r') as inf:
    with open('books.csv', 'w', encoding='ISO-8859-1') as outf:
        booksFile = csv.writer(outf, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")

        outf.write('product_page_url, universal_product_code, title, '
                   'price_including_tax, price_excluding_tax, number_available,'
                   'product_description, category, review_rating, image_url\n')

        for row in inf:
            url = row.strip()
            responseBooks = requests.get(url)

            if responseBooks.ok:
                soup = BeautifulSoup(responseBooks.text, 'html.parser')
                trs = soup.findAll('tr')

                upc = trs[0].find('td')
                priceIncl = trs[3].find('td')
                priceExcl = trs[2].find('td')

                nbrAvailable = trs[5].find('td')
                nbr = int(''.join(filter(str.isdigit, nbrAvailable.text)))

                title = soup.find('h1')
                description = soup.find('p', {'class': ''})

                category = soup.findAll('li')[2]
                rating = soup.find('p', {'class': 'star-rating'}).get('class')

                urlImgRaw = soup.find('div', {'class': 'item active'}).find('img')
                urlImg = urlImgRaw.get('src')[6:]

                outf.write(url + ',' + upc.text + ',' + '"' + title.text + '"' + ',' + priceIncl.text[1:] + ',' +
                           priceExcl.text[1:] + ',' + str(nbr) + ',' + '"' + description.text.replace('"', '""') + '"' + ',' +
                           category.text[1:-1] + ',' + ' '.join(rating)[12:] + ',' +
                           'http://books.toscrape.com/' + urlImg + '\n')