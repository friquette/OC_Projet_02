import requests
from bs4 import BeautifulSoup
import shutil


def getContent(myPath, linkBooks, url):
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


def writeContent(outp, categoryPath, linkBooks, url):
    writeFile(outp, getContent(categoryPath, linkBooks, url))
    dlImage(getContent(categoryPath, linkBooks, url))