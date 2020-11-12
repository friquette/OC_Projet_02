import requests
from bs4 import BeautifulSoup
import csv
import os.path
import shutil

with open('config.txt', 'r') as conf:               #lecture du fichier config.txt pour récupérer le chemin de dossier
    csvFolder = conf.read().strip(' \n')
    if csvFolder == '':                             #si le fichier est vide, le chemin par défaut est à la racine du projet
        currentFolder = os.getcwd()
        csvFolder = currentFolder + '/csv'
        if not os.path.exists(currentFolder):
            os.mkdir(csvFolder)
    else:
        if not os.path.exists(csvFolder):
            os.mkdir(csvFolder)


def getContent(myPath):
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


url = 'http://books.toscrape.com/'
response = requests.get(url)

if response.ok:
    soupCtg = BeautifulSoup(response.text, 'html.parser')
    menuCtg = soupCtg.findAll('ul', {'class': 'nav nav-list'})
    categories = menuCtg[0].find('ul').findAll('li')                #récupération de toutes les catégories

    for category in categories:
        i = 0

        a = category.find('a')
        link = a['href']
        links = url + link                  #url complète de chaque catégorie dans la variable links

        urlCategories = links[0:-10]
        responseBooks = requests.get(urlCategories)

        if responseBooks.ok:
            soupBooks = BeautifulSoup(responseBooks.text, 'html.parser')
            urlBooks = soupBooks.findAll('div', {'class': 'image_container'})

            classNext = soupBooks.find('li', {'class': 'next'})
            nameCategory = urlCategories[51:-1].strip('_0123456789')

            if not classNext:                                   #si la catégorie n'a qu'une seule page
                categoryPath = csvFolder + '/' + nameCategory
                if not os.path.exists(categoryPath):
                    os.makedirs(categoryPath)

                with open(categoryPath + '/' + nameCategory + '.csv', 'w', encoding='utf-8') as outp:
                    booksFile = csv.writer(outp, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
                    outp.write('product_page_url, universal_product_code, title, '
                               'price_including_tax, price_excluding_tax, number_available,'
                               'product_description, category, review_rating, image_url\n')

                    for urlBook in urlBooks:
                        aBooks = urlBook.find('a')
                        linkBook = aBooks['href']
                        linkBooks = url + 'catalogue/' + linkBook[9:]

                        writeFile(outp, getContent(categoryPath))
                        dlImage(getContent(categoryPath))
            else:                                               #si la catégorie a plusieurs pages
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
                        urlPages = urlCategories + 'page-' + str(i) + '.html'   #tant que request renvoie une réponse on incrémente le numéro de la page dans l'url
                        responsePages = requests.get(urlPages)

                        if responsePages.ok:
                            soupPages = BeautifulSoup(responsePages.text, 'html.parser')
                            urlBooks = soupPages.findAll('div', {'class': 'image_container'})

                            for urlBook in urlBooks:
                                aBooks = urlBook.find('a')
                                linkBook = aBooks['href']
                                linkBooks = url + 'catalogue/' + linkBook[9:]

                                writeFile(outp, getContent(categoryPath))
                                dlImage(getContent(categoryPath))

                        if not responsePages.ok:
                            break
