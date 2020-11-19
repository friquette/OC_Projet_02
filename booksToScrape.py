"""This module scrapes all the http://books.toscrape.com website."""
import requests
from bs4 import BeautifulSoup
import os.path
import scrapeCategory
import sys


def main():
    """Scrapes the website homepage.

    Get the path set by the user where the results will be saved.
    Parse the homepage and retrieves links of all categories.
    Calls the browse_pages function of the scrapCategory module.

    """

    path_user_arg = sys.argv
    csv_folder = os.getcwd() + '/csv'

    if len(path_user_arg) == 2:
        if os.path.isdir(path_user_arg[1]):
            csv_folder = path_user_arg[1] + '/csv'
            if not os.path.exists(csv_folder):
                os.makedirs(csv_folder)
        else:
            print('Please enter a valid path folder')
            exit()
    else:
        print('Please enter a path folder')
        exit()

    url = 'http://books.toscrape.com/'
    response = requests.get(url)

    if response.ok:
        soup_ctg = BeautifulSoup(response.text, 'lxml')
        menu_ctg = soup_ctg.findAll('ul', {'class': 'nav nav-list'})
        categories = menu_ctg[0].find('ul').findAll('li')

        for category in categories:
            a = category.find('a')
            link = url + a['href']

            scrapeCategory.browse_pages(link[0:-10], csv_folder, url)


if __name__ == '__main__':
    main()
