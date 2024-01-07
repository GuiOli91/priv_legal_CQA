# import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

URL = "https://www.avvo.com"
PATH = "/topics/bankruptcy/advice"
# URL = "https://www.avvo.com/topics/bankruptcy/advice?utf8=✓&search_topic_advice_search[state]=CA&search_topic_advice_search[content_type]=question&ajax=1"

PARAMS = {'utf8':'✓',
          'search_topic_advice_search[state]':'CA',
          'search_topic_advice_search[content_type]':'question',
          'ajax':'1',
          }

url_parms = f"{URL}{PATH}?{'&'.join([f'{k}={v}' for k,v in PARAMS.items()])}"

# options = webdriver.FirefoxOptions()
# driver = webdriver.Firefox(options=options)

driver = webdriver.Remote("http://localhost:4444", options=webdriver.ChromeOptions())

try:
    # Set a timeout for waiting for elements to load (e.g., 10 seconds)
    wait = WebDriverWait(driver, 5)

    # Navigate to the URL
    driver.get(url_parms)
    
    # Get the Maximum page number
    pages = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "pagination-page-v2")))
    page = pages[-1].text
    page = int(page)
    
    links = []
    for i in range(page):
        if i == 0:
            continue
        else:
            PARAMS['page'] = i + 1
            url_parms = f"{URL}{PATH}?{'&'.join([f'{k}={v}' for k,v in PARAMS.items()])}"
            driver.get(url_parms)

        # Wait until all the elements with class "topic-advice-question-card" are present
        topic_questions = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "topic-advice-question-card")))

        # Loop through each "topic-question" element
        for topic_question in topic_questions:
            # Find all elements with class "block-link" within the current "topic-question" element
            block_link = topic_question.find_element(By.CLASS_NAME, "block-link")

            # Print the text content of each "block-link" element
            href = block_link.get_attribute("href")
            if href:
                links.append(href)

except Exception as e:
    # Handle any exceptions that may occur
    print(f"An error occurred: {e}")

finally:
    # Close the browser window
    driver.quit()


