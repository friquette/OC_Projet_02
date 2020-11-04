import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/avatar-the-last-airbender-smoke-and-shadow-part-3-smoke-and-shadow-3_881/index.html'

response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.findAll('tr')
    upc = trs[0].find('td')
    priceIncl = trs[3].find('td')
    priceExcl = trs[2].find('td')
    nmbrAvailable = trs[5].find('td')
    title = soup.find('h1')
    paragraph = soup.find('p', {'class': ''})
    li = soup.findAll('li')

    rating = soup.find('p', {'class': 'star-rating'}).get('class')

    print(' '.join(rating))
    print(url)
    print(upc.text)
    print(title.text)
    print(priceIncl.text)
    print(priceExcl.text)
    print(nmbrAvailable.text)
    print(paragraph.text)
    print(li[2].text)


    #
    # for tr in trs:
    #     tr = soup.find('td')
    #     upc = tr[0]
