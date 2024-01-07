from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import json

OUTPUT_DIR = "web_out"
FILE = "data.json"

driver = webdriver.Remote("http://localhost:4444", options=webdriver.ChromeOptions())

with open(os.path.join(OUTPUT_DIR, FILE), "r") as file:
  json_data = file.read()
        
data_dict = json.loads(json_data)

wait = WebDriverWait(driver, 10)

for page, links in data_dict.items():
  i = 0
  for url in links:
    try:
      
      # Navigate to the question url
      driver.get(url)
      
      id = f"{page}_{str(i)}"
      
      topic_tags = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "content-topic-tags")))
      
      topic_tags = topic_tags.text.split("\n")
      
      content_question = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "question")))
    
      
    
      i = i + 1
      
    except Exception as e:
      # Handle any exceptions that may occur
      print(f"An error occurred: {e}")
      continue
      
driver.quit()
        
      
        

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
    wait = WebDriverWait(driver, 10)

    # Navigate to the URL
    driver.get(url_parms)
    
    # Get the Maximum page number
    pages = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "pagination-page-v2")))
    page = pages[-1].text
    page = int(page)
    
    links = {}
    for i in range(page):
        if i != 0:
            PARAMS['page'] = i + 1
            url_parms = f"{URL}{PATH}?{'&'.join([f'{k}={v}' for k,v in PARAMS.items()])}"
            driver.get(url_parms)

        # Wait until all the elements with class "topic-advice-question-card" are present
        topic_questions = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "topic-advice-question-card")))

        # Loop through each "topic-question" element
        questions = []
        for topic_question in topic_questions:
            # Find all elements with class "block-link" within the current "topic-question" element
            block_link = topic_question.find_element(By.CLASS_NAME, "block-link")

            # Print the text content of each "block-link" element
            href = block_link.get_attribute("href")
            
            if href:
                questions.append(href)
                
        links[f"page_{i+1}"] = questions
        
    folder_path = os.path.join(os.getcwd(), OUTPUT_DIR)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    json_data = json.dumps(links)

    with open(os.path.join(folder_path, "data.json"), "w") as file:
        file.write(json_data)
    

except Exception as e:
    # Handle any exceptions that may occur
    print(f"An error occurred: {e}")

finally:
    # Close the browser window
    driver.quit()


