from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from .data import full_link, USER_AGENT, count_parse_page


def get_page_html():
    """
    Browser: chrome
    Options: 
        - run in the background (without a browser window)
        - user agent
        - turn off the display of pictures for productivity
    Clicking button "next", for getting new announcements
    """

    # Configure Selenium options
    options = Options()
    options.add_argument('--headless')  
    options.add_argument(f"user-agent={USER_AGENT}")  
    options.add_argument('--disable-blink-features=AutomationControlled')  
    options.add_argument('log-level=3') 

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(full_link)  

    # Find the HTML block containing the property results
    blocks = driver.find_element(By.ID, "property-result")
    html_page = blocks.get_attribute("innerHTML") 

    # Find the "Next page" button
    next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")

    # Initialize click counter
    click_count = 0

    # Loop to navigate through multiple pages
    while next_button and click_count < count_parse_page:
        next_button.click()  
        blocks = driver.find_element(By.ID, "property-result") 
        html_page += blocks.get_attribute("innerHTML") 

        # Check if the "Next page" button is still available
        next_button = driver.find_element(By.CSS_SELECTOR, "li.next a") if driver.find_elements(By.CSS_SELECTOR, "li.next a") else None
        click_count += 1  

    driver.quit() 

    # Parse the accumulated HTML content using BeautifulSoup
    bs4_page = BeautifulSoup(html_page, "html.parser")

    return bs4_page