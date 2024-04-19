from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from .data import full_link, USER_AGENT


def get_page_html():
    options = Options()

    options.add_argument('--headless')
    options.add_argument(f"user-agent={USER_AGENT}")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('log-level=3')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                            options=options)
    driver.get(full_link)

    blocks = driver.find_element(By.ID, "property-result")
    html_page = blocks.get_attribute("innerHTML")
    
    # we get the "Next page" button
    next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")
    
    # click counter
    click_count = 0
    
    while next_button and click_count < 6:
        next_button.click()
        # update HTML blocks
        blocks = driver.find_element(By.ID, "property-result")
        html_page += blocks.get_attribute("innerHTML")

        # check if the "Next page" button is available
        next_button = driver.find_element(By.CSS_SELECTOR, "li.next a") if driver.find_elements(By.CSS_SELECTOR, "li.next a") else None
        click_count += 1
    
    driver.quit()
    
    bs4_page = BeautifulSoup(html_page, "html.parser")
    return bs4_page