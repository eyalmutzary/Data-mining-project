import json
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import asyncio


AMOUNT_OF_EXPAND: int = 19
PATH = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
START_LINK = "https://www.imdb.com"

movie_list: List[List[str]] = []


def get_links_list_of_movies_categories():
    links = []
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(PATH)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    for bar in soup.find_all("div", {"class": "aux-content-widget-2"}):
        for category_tag in bar.find_all('a'):
            links.append(START_LINK + category_tag['href'])
    return links[8::]


def get_movies_links(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    for bar in soup.find_all("h3", {"class": "lister-item-header"}):
        for category_tag in bar.find_all('a'):
            movie_list.append([START_LINK + category_tag['href']])


def get_all_links_category(driver):
    get_movies_links(driver)
    for i in range(AMOUNT_OF_EXPAND):

        driver.implicitly_wait(1)

        # Find the element by class name
        button = driver.find_element(By.CLASS_NAME, "lister-page-next")
        # Click the element
        button.click()
        get_movies_links(driver)
        time.sleep(1)


def get_data_from_single_category(cat_link):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(cat_link)
    get_all_links_category(driver)


def export_to_csv():
    # field names
    category = 'movie_link'
    file_name = 'output1.csv'

    with open(file_name, 'w', newline='') as csv_file:
        # Create a CSV writer object
        writer = csv.writer(csv_file)

        # Write the category as the first row in the CSV file
        writer.writerow([category])

        # Write the list of rows to the CSV file
        writer.writerows(movie_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    category_link = get_links_list_of_movies_categories()
    for lnk in category_link:
        try:
            print(lnk)
            get_data_from_single_category(lnk)
        except:
            continue
    print(movie_list)
    print(len(movie_list))

    export_to_csv()


