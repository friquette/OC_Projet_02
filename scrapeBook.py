"""This module parses a book page."""
import requests
from bs4 import BeautifulSoup
import csv
import shutil
import sys
import utility


def get_content(my_path, link_books, url):
    """Gets the content of a book page.

    Parses the page of a book and store various information in variables.
    Parameters:
    my_path -- the path the files will be saved into
    link_books -- the page url to scrape
    url -- the homepage url
    Return:
    book_info -- a dictionary with all the useful variables

    """
    response_content = requests.get(link_books)
    soup_content = BeautifulSoup(response_content.text, 'lxml')

    trs = soup_content.findAll('tr')
    upc = trs[0].find('td')
    price_incl = trs[3].find('td')
    price_excl = trs[2].find('td')

    nbr_available = trs[5].find('td')
    nbr = int(''.join(filter(str.isdigit, nbr_available.text)))

    title = soup_content.find('h1')

    description = soup_content.find('p', {'class': ''})
    description_book = description.text if description else ''

    book_category = soup_content.findAll('li')[2]
    rating = soup_content.find('p', {'class': 'star-rating'}).get('class')

    url_img_raw = soup_content.find('div', {'class': 'item active'}).find('img')
    url_img = url_img_raw.get('src')[6:]
    url_img_full = url + url_img

    response_image = requests.get(url_img_full, stream=True)

    image_name = url_img_full.split('/')[-1]
    image_path = my_path + '/' + image_name

    book_info = {'link_books': link_books, 'upc': upc, 'title': title, 'price_incl': price_incl,
                 'price_excl': price_excl, 'nbr': nbr, 'description_book': description_book,
                 'book_category': book_category, 'rating': rating, 'response_image': response_image,
                 'url_image_full': url_img_full, 'image_path': image_path}

    return book_info


def dl_image(book_info):
    """Saves the image of the book.

    Get the response_image of the book_info dictionary and create a binary file to store the image
    into.
    Parameter:
    book_info -- a dictionary containing the different information of the book webpage
    """
    if book_info['response_image'].ok:
        book_info['response_image'].raw.decode_content = True
        with open(book_info['image_path'], 'wb') as f:
            shutil.copyfileobj(book_info['response_image'].raw, f)
    else:
        print('Image not found for this book: ' + book_info['title'])


def write_file(name_output, book_info):
    """Writes the file

    Writes the values of the get_content function dictionary in a file.
    Parameters:
    name_output -- the name of the file the return values will be write into
    book_function -- a dictionary containing the different information of the book webpage

    """
    name_output.write(book_info['link_books'] + ',' + book_info['upc'].text + ',' + '"' + book_info['title'].text + '"' +
                      ',' + book_info['price_incl'].text[2:] + ',' + book_info['price_excl'].text[2:] +
                      ',' + str(book_info['nbr']) + ',' + '"' + book_info['description_book'].replace('"', '""') +
                      '"' + ',' + book_info['book_category'].text[1:-1] + ',' + ' '.join(book_info['rating'])[12:] +
                      ',' + book_info['url_image_full'] + ',' + book_info['image_path'] + '\n')


def write_content(out_file, category_path, link_books, url):
    """Writes all the information in the file

    Calls the write_file and the dl_image functions.
    Parameters:
    out_file -- the name of the file the information will be written into
    category_path -- the path the files will be saved into
    link_books -- the page url to scrape
    url -- the homepage url

    """

    write_file(out_file, get_content(category_path, link_books, url))
    dl_image(get_content(category_path, link_books, url))


def main(url):
    """Used if the module is executed as a script.

    Calls the get_path_user function of the utility module to get the path the user entered in the console.
    Creates the file the information will be store into.
    Calls the write_content function.
    Parameter:
    url -- the page url to scrape entered by the user

    """

    utility.get_path_user()

    main_url = 'http://books.toscrape.com/'

    response = requests.get(url)
    file = utility.get_path_user() + '/book.csv'

    if response.ok:
        with open(file, 'w', encoding='utf-8') as out_file:
            csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_NONE, quotechar="")
            out_file.write('product_page_url, universal_product_code, title, '
                           'price_including_tax, price_excluding_tax, number_available,'
                           'product_description, category, review_rating, image_url, image_path \n')

            write_content(out_file, utility.get_path_user(), url, main_url)


if __name__ == '__main__':
    url_user_arg = sys.argv
    if len(url_user_arg) == 3:
        if 'http://books.toscrape.com' in url_user_arg[2]:
            user_response = requests.get(url_user_arg[2])
            if user_response.ok:
                if '/catalogue/' in url_user_arg[2] and '/category/books/' not in url_user_arg[2]:
                    main(url_user_arg[2])
            else:
                print('Please enter a book url. '
                      'Example: http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
        else:
            print('Please enter a valid url')
    else:
        print('Please enter a path folder and a url')
