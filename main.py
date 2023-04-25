import json
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
AMOUNT_OF_EXPAND: int = 3
PATH_TEST = "https://www.imdb.com/search/title/?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=66KC56830Z4J29ES4WAB&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_1"


def load_more(driver):
    for i in range(AMOUNT_OF_EXPAND):
        driver.implicitly_wait(1)
        # Find the element by class name
        button = driver.find_element(By.CLASS_NAME, "lister-page-next")
        # Click the element
        print("111")
        button.click()
        time.sleep(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome()
    driver.get(PATH_TEST)
    load_more(driver)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
