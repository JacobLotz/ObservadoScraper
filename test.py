from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException




def test(url):
    pathdriver = "/data/localhome/jelotz/Documents/WebDriver/chromedriver"
    wait_for_element = 30  # wait timeout in seconds
    browser = webdriver.Chrome(executable_path = pathdriver)
    browser.get(url)

    try:
        WebDriverWait(browser, wait_for_element).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "leaflet-zoom-animated")))
    except TimeoutException as e:
        print("Wait Timed out")
        print(e)

    PageSoup = soup(browser.page_source, "html.parser")
    print(PageSoup)

#if __name__ == '__main__':
#    test("http://www.python.org")

link = "https://old.waarneming.nl/soort/maps/227?from=2020-07-17&to=2021-07-17"



test(link)