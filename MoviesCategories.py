from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PATH = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
START_LINK = "https://www.imdb.com"


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
    return links


if __name__ == "__main__":
    print(get_links_list_of_movies_categories())
