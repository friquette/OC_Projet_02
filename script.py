import requests
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com/catalogue/avatar-the-last-airbender-smoke-and-shadow-part-3-smoke-and-shadow-3_881/index.html'

response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')

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

    # print(url)
    # print(upc.text)
    # print(title.text)
    # print(priceIncl.text[1:])
    # print(priceExcl.text[1:])
    # print(nbr)
    # print(description.text)
    # print(category.text[1:-1])
    # print(' '.join(rating)[12:])
    # print('http://books.toscrape.com/' + urlImg)
    # print(description.text)

    with open('books.csv', 'w') as outf:
        booksFile = csv.writer(outf, delimiter=";")
        outf.write('product_page_url; universal_product_code; title; '
                   'price_including_tax; price_excluding_tax; number_available;'
                   'product_description; category; review_rating; image_url\n')

        outf.write(url + ';' + upc.text + ';' + title.text + ';' + priceIncl.text[1:] + ';' + priceExcl.text[1:] +
                   ';' + str(nbr) + ';' + description.text + ';' + category.text[1:-1] + ';' + ' '.join(rating)[12:] +
                   ';' + 'http://books.toscrape.com/' + urlImg)