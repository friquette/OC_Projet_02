# OC_Projet_02
Projet 2 - Utilisez les bases de Python pour l'analyse de marché

## What is the script for?
This script allows you to scrape the 
[books.toscrape.com](http://books.toscrape.com/) website.

There's 3 ways you can use the script :
- Scrape the entire website
- Scrape a specified category
- Scrape a specified product

It will save a csv file by category and the image of each product.

## Set up the project
This project runs in python 3 <br>

Make a copy of this project on your hard drive <br>
`git clone https://github.com/friquette/OC_Projet_02.git`

Go in the root project and create a virtual environment <br>
`cd OC_Projet_02` <br>
`python -m venv env`

Activate your virtual environment <br>
- On windows `env\Scripts\activate.bat`
- On Mac OS/Linux `source env/bin/activate`

Install the packages <br>
`pip install -r requirements.txt`

## How to use it
You can use the script 3 different ways

>#### Scrape the entire website: <br>
> Simply execute the script.py file <br>
>`python script.py` 

>#### Scrape a specified category <br>
>Execute the scrapeCategory.py file with the category url you want as argument <br>
>`python scrapeCategory.py <my_category_url>`

>#### Scrape a specified product
>Execute the scrapeBook.py file with the product url you want as argument <br>
>`python scrapeBook.py <my_book_url>`

You can specify the path where you want to save the files, in the config.txt file.
By default a csv folder will be created in the root project folder.