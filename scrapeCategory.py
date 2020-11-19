"""This module scrapes a category webpage."""
import requests
from bs4 import BeautifulSoup
import csv
import os.path
import scrapeBook
import sys
import utility


def get_link_books(url_books, url, out_file, category_path):
    """Retrieves urls of all books in the pages

    Retrieves url of each book in all books urls of the pages.
    Calls the writeContent function of the scrapeBook module.
    Parameters:
    urls_books -- list of all books urls
    url -- url of the page to scrape
    out_file -- name of the csv file to write in
    category_path -- path of the folder to save the files in

    """

    for url_book in url_books:
        a_books = url_book.find('a')
        link_book = a_books['href']
        link_books = url + 'catalogue/' + link_book[9:]

        scrapeBook.write_content(out_file, category_path, link_books, url)


def browse_pages(url_categories, csv_folder, url):
    """Browses all the pages of the category

    Parses the page.
    If the tag class 'next' isn't in the page, calls the getLinkBooks function.
    If the tag class 'next' is in the page, increment the 'page-x' part of the url while
    the condition is true. Then calls the getLinkBooks function.
    Parameters:
    url_categories -- list of all categories urls
    csv_folder -- the path the files will be saved into
    url -- url of the page to scrape

    """

    response_books = requests.get(url_categories)
    if response_books.ok:
        soup_books = BeautifulSoup(response_books.text, 'lxml')
        url_books = soup_books.findAll('div', {'class': 'image_container'})

        class_next = soup_books.find('li', {'class': 'next'})
        name_category = url_categories[51:-1].strip('_0123456789')

        if not class_next:
            category_path = csv_folder + '/' + name_category
            if not os.path.exists(category_path):
                os.makedirs(category_path)

            with open(category_path + '/' + name_category + '.csv', 'w', encoding='utf-8') as out_file:
                csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
                out_file.write('product_page_url, universal_product_code, title, '
                               'price_including_tax, price_excluding_tax, number_available,'
                               'product_description, category, review_rating, image_url\n')

                get_link_books(url_books, url, out_file, category_path)

        else:
            i = 0
            category_path = csv_folder + '/' + name_category
            if not os.path.exists(category_path):
                os.mkdir(category_path)

            with open(category_path + '/' + name_category + '.csv', 'w', encoding='utf-8') as out_file:
                csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
                out_file.write('product_page_url, universal_product_code, title, '
                               'price_including_tax, price_excluding_tax, number_available,'
                               'product_description, category, review_rating, image_url\n')
                while True:
                    i += 1
                    url_pages = url_categories + 'page-' + str(i) + '.html'
                    response_pages = requests.get(url_pages)

                    if response_pages.ok:
                        soup_pages = BeautifulSoup(response_pages.text, 'lxml')
                        url_books = soup_pages.findAll('div', {'class': 'image_container'})

                        get_link_books(url_books, url, out_file, category_path)

                    else:
                        break


def main(url):
    """Used if the module is executed as a script.

    Reads the config.txt file to find the path where the results will be saved (the project root
    folder by default).
    Calls the browsePages function.
    Parameter:
    url -- the page url to scrape

    """
    utility.get_path_user()

    main_url = 'http://books.toscrape.com/'

    response = requests.get(url)
    if response.ok:
        print(utility.get_path_user())
        browse_pages(url, utility.get_path_user(), main_url)


if __name__ == '__main__':
    url_user_arg = sys.argv
    if len(url_user_arg) == 3:
        if 'http://books.toscrape.com' in url_user_arg[2]:
            user_response = requests.get(url_user_arg[2])
            if user_response.ok:
                if "/category/books/" in url_user_arg[2]:
                    main(url_user_arg[2][:-10])
                else:
                    print('Please enter a category url. '
                          'Example: http://books.toscrape.com/catalogue/category/books/travel_2/index.html')
            else:
                print('Please enter a valid url')
        else:
            print('Please enter a valid url')
    else:
        print('Please enter a path folder and a url')
