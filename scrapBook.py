import requests
from bs4 import BeautifulSoup
import csv
import shutil
import os.path


def getContent(myPath, linkBooks, url):
    responseContent = requests.get(linkBooks)
    soupContent = BeautifulSoup(responseContent.text, 'lxml')

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
    urlImgFull = url + urlImg

    responseImage = requests.get(urlImgFull, stream=True)

    imageName = urlImgFull.split('/')[-1]
    imagePath = myPath + '/' + imageName

    return (linkBooks, upc, title, priceIncl, priceExcl, nbr, descriptionBook, bookCategory,
            rating, urlImg, myPath, responseImage, imagePath)


def dlImage(func):
    if func[11].ok:
        func[11].raw.decode_content = True
        with open(func[12], 'wb') as f:
            shutil.copyfileobj(func[11].raw, f)
    else:
        print('Image not found')


def writeFile(nameOutput, func):
    nameOutput.write(func[0] + ',' + func[1].text + ',' + '"' + func[2].text + '"' + ',' + func[3].text[2:] + ',' +
                     func[4].text[2:] + ',' + str(func[5]) + ',' + '"' + func[6].replace('"', '""') + '"' + ',' +
                     func[7].text[1:-1] + ',' + ' '.join(func[8])[12:] + ',' + func[12] + '\n')


def writeContent(outp, categoryPath, linkBooks, url):
    writeFile(outp, getContent(categoryPath, linkBooks, url))
    dlImage(getContent(categoryPath, linkBooks, url))


def main(url):
    mainUrl = 'http://books.toscrape.com/'
    with open('config.txt', 'r') as conf:
        csvFolder = conf.read().strip(' \n')
        if csvFolder == '':
            currentFolder = os.getcwd()
            csvFolder = currentFolder + '/csv'
            if not os.path.exists(csvFolder):
                os.mkdir(csvFolder)
        else:
            if not os.path.exists(csvFolder):
                os.mkdir(csvFolder)

        response = requests.get(url)
        file = csvFolder + '/book.csv'

        if response.ok:
            with open(file, 'w', encoding='utf-8') as outp:
                csv.writer(outp, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
                outp.write('product_page_url, universal_product_code, title, '
                           'price_including_tax, price_excluding_tax, number_available,'
                           'product_description, category, review_rating, image_url\n')

                writeContent(outp, csvFolder, url, mainUrl)


if __name__ == '__main__':
    with open('url.txt', 'r') as urlConf:
        url = urlConf.read().strip('\n')
        if url == '':
            print('Please enter a valid url')
        else:
            main(url)
