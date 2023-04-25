# import json
# import time
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# from typing import List, Dict
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import asyncio
#
# START_LINK = "https://www.indiegogo.com"
#     PATH = "https://www.indiegogo.com/explore/home?project_type=campaign&project_timing=all&sort=trending"
# AMOUNT_OF_EXPAND: int = 70
# DOLLAR: float = 3.61
#
# """
#     selenium func that loads more cards
# """
#
#
# def load_more(driver):
#     for i in range(AMOUNT_OF_EXPAND):
#         driver.implicitly_wait(2)
#         # Find the element by class name
#         button = driver.find_element(By.CLASS_NAME, "i-cta-1.ng-binding.ng-isolate-scope")
#         # Click the element
#         button.click()
#         time.sleep(1)
#
#
# """
#     create a list of links to all pages
# """
#
#
# def get_links_list_from_html():
#     # Get the HTML source of the page
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get(PATH)
#     load_more(driver)
#     html = driver.page_source
#     soup = BeautifulSoup(html, "html.parser")
#     cards = soup.find_all("div", {"class": "discoverableCard"})
#
#     links = []
#     # Add the links content of each card
#     for card in cards:
#         a_tag = card.find("a")
#         if a_tag:
#             links.append(START_LINK + a_tag["href"])
#     return links
#
#
# """
#     putting the data fron a single page to a dictionary
# """
#
#
# async def one_page_to_dict(link: str, driver):
#     driver.get(link)
#     html = driver.page_source
#     data: Dict = {}
#     soup = BeautifulSoup(html, "html.parser")
#     try:
#
#         data["Creator"] = soup.find("div", {"class": "campaignOwnerName-tooltip"}).text.strip()
#         data["Title"] = soup.find("div", {"class": "basicsSection-title"}).text.strip()
#         data["Text"] = soup.find("div", {"class": "basicsSection-tagline"}).text.strip()
#         data["DollarsPledged"] = int(int(soup.find("span", {"class": "basicsGoalProgress-amountSold"})
#                                          .text.strip().replace('₪', '').replace(',', '')) / DOLLAR)
#         data["FlexibleGoal"] = "Flexible Goal" in soup.text
#         page_type = soup.find("div", {"class": "basicsSection-statusLabel"}).text.strip()
#
#         if page_type == "Funding":
#             data["DollarsGoal"] = int(int((soup.find("span", {
#                 "class": "basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOr"
#                          "InitiallyRaised"}).text.strip().split('₪')[
#                                                1].replace(',', ''))) / DOLLAR)
#             data["NumBackers"] = int(soup.find("span", {"class": "basicsGoalProgress-claimedOrBackers"}).find \
#                                          ("span", {"class": "t-weight--medium"}).text.strip().replace(',', ''))
#             data["DaysToGo"] = int(
#                 soup.find("div", {"class": "basicsGoalProgress-progressDetails-detailsTimeLeft"}).find \
#                     ("span", {"class": "t-weight--medium"}).text.strip().replace(',', ''))
#
#         elif page_type == "Indemand":
#             data["DollarsGoal"] = int(int(soup.find("span", {
#                 "class": "basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOr"
#                          "InitiallyRaised"}).text.strip().split(' ')[
#                                               0].replace('₪', '').replace(',',
#                                                                           '')) / DOLLAR)
#             data["NumBackers"] = int(soup.find("span", {"class": "basicsGoalProgress-claimedOrBackers"})
#                                      .text.strip().split(' ')[1].replace(',', ''))
#             data["DaysToGo"] = None
#
#         elif page_type == "Closed":
#             data["DollarsGoal"] = int(int(soup.find("span", {
#                 "class": "basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOr"
#                          "InitiallyRaised"}).text.strip().split('₪')[
#                                               1].replace(',', '')) / DOLLAR)
#             data["NumBackers"] = int(soup.find("span", {
#                 "class": "basicsGoalProgress-claimedOrBackers"}).find \
#                 ("span", {
#                     "class": "t-weight--medium"}).text.strip().replace(
#                 ',', ''))
#             data["DaysToGo"] = None
#     except:
#         # we decided to ignore other pages (not the classic Funding/Indemand/Closed)
#         # print("FAILED")
#         return None
#     return data
#
#
# """
#     going over the links and saing the data in a list
# """
#
#
# async def get_all_data_from_links(links):
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     driver = webdriver.Chrome(options=chrome_options)
#     tasks = []
#     for link in links:
#         single_page = asyncio.ensure_future(one_page_to_dict(link, driver))
#         if single_page is not None:
#             tasks.append(single_page)
#
#     results = await asyncio.gather(*tasks)
#     driver.quit()
#     return results
#
#
# """
#     getting all the data from all the pages
# """
#
#
# def scrape_data():
#     links: List[str] = get_links_list_from_html()
#     loop = asyncio.get_event_loop()
#     results = loop.run_until_complete(get_all_data_from_links(links))
#     loop.close()
#     return results
#
#
# if __name__ == "__main__":
#     results: List[Dict] = scrape_data()
#
#     # Write the list to a JSON file
#     with open("data3.json", "w") as f:
#         json.dump(results, f)
