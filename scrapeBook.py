"""This module parses a book page."""
import requests
from bs4 import BeautifulSoup
import csv
import shutil
import os.path


def getContent(myPath, linkBooks, url):
    """Gets the content of a book page.

    Parses the page of a book and store various information in variables.
    Parameters:
    myPath -- the path the files will be saved into
    linkBooks -- the page url to scrape
    url -- the homepage url
    Returns:
    linkBooks -- page url of the book
    upc -- universal product code
    title -- the book's title
    priceIncl -- price including taxes
    priceExl -- price excluding taxes
    nbr -- number of books available
    descriptionBook -- the book's description
    bookCategory -- the book's category
    rating -- the review rating of the book
    responseImage -- the request of the image url
    imagePath -- the path the image is saved into

    """
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
            rating, responseImage, imagePath)


def dlImage(func):
    """Saves the image of the book."""
    if func[9].ok:
        func[9].raw.decode_content = True
        with open(func[10], 'wb') as f:
            shutil.copyfileobj(func[9].raw, f)
    else:
        print('Image not found')


def writeFile(nameOutput, func):
    """Writes the content in the file

    Writes the return values of the getContent function in a file.
    Parameters:
    nameOutput -- the name of the file the return values will be write into
    func -- the function the return values are taken from

    """
    nameOutput.write(func[0] + ',' + func[1].text + ',' + '"' + func[2].text + '"' + ',' + func[3].text[2:] + ',' +
                     func[4].text[2:] + ',' + str(func[5]) + ',' + '"' + func[6].replace('"', '""') + '"' + ',' +
                     func[7].text[1:-1] + ',' + ' '.join(func[8])[12:] + ',' + func[10] + '\n')


def writeContent(outp, categoryPath, linkBooks, url):
    """Writes all the information in the file

    Calls the writeFile and the dlImage functions.
    Parameters:
    outp -- the name of file the information will be written into
    categoryPath -- the path the files will be saved into
    linkBooks -- the page url to scrape
    url -- the homepage url

    """

    writeFile(outp, getContent(categoryPath, linkBooks, url))
    dlImage(getContent(categoryPath, linkBooks, url))


def main(url):
    """Used if the module is executed as a script.

    Reads the config.txt file to find the path where the results will be saved (the project root
    folder by default).
    Calls the writeContent function.
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
