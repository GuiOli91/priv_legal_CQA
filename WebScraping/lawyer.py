from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
import os


CONTAINER = "http://localhost:4444"
URL = "https://www.avvo.com/bankruptcy-debt-lawyer/ca.html"
OUTPUT_DIR = "web_out"
OUT_FILE = "lawyers_link.json"


def close_connection(driver):
    """Do the necessary steps to end the program

    Args:
        driver (selenium.webdriver): The driver to close
    """
    
    driver.quit()


driver = webdriver.Remote(CONTAINER, options=webdriver.ChromeOptions())

wait = WebDriverWait(driver, 5)

driver.get(URL)

try:

    lawyers_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lawyer-search-results")))

except Exception as e:
    print(e)
    close_connection(driver)
    exit()

try :    
    lawyers = lawyers_list.find_elements(By.CLASS_NAME, "gtm-profile-link")
    
except Exception as e:
    print(e)
    close_connection(driver)
    exit()
    
i = 0
lawyers_dict = dict()

for lawyer in lawyers:
    i += 1
    try:
        lawyer_link = lawyer.get_attribute("href")
        lawyers_dict[i] = lawyer_link
    except Exception as e:
        print(e)
        continue

if os.path.exists(os.path.join(OUTPUT_DIR, OUT_FILE)):
    with open(os.path.join(OUTPUT_DIR, OUT_FILE), "r") as file:
        json_decoded = json.loads(file.read())
else:
    json_decoded = {}

json_decoded.update(lawyers_dict)

with open(os.path.join(OUTPUT_DIR, OUT_FILE), "w") as file:
    file.write(json.dumps(json_decoded))

close_connection(driver)