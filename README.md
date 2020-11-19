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
When you execute a script, a "csv" folder will be created in 
the folder path you want. <br>
You can use the script 3 different ways

- #### Scrape the entire website: <br>
    Execute the script.py file with the folder path you want as
    argument<br>
    `python script.py <my_folder_path>` <br>
    
    A folder for each category will be created in the "csv" folder. 
    The .csv file and images associated will be created 
    in each category folder.

- #### Scrape a specified category <br>
    Execute the scrapeCategory.py file with the folder path
    and the category url you want as arguments <br>
    `python scrapeCategory.py <my_folder_path> <my_category_url>` <br>
    
    A folder named after the category will be created in the
    "csv" folder. The .csv file and images associated will be 
    created in the category folder.

- #### Scrape a specified product
    Execute the scrapeBook.py file with the folder path and the
    product url you want as arguments <br>
    `python scrapeBook.py <my_folder_path> <my_book_url>` <br>
    
    The .csv file and image associated will be created in the 
    "csv" folder.

