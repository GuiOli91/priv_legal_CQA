from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException
)

import os
import json
import re

OUTPUT_DIR = "web_out"
FILE = "data.json"
OUT = "qa.json"

driver = webdriver.Remote("http://localhost:4444", options=webdriver.ChromeOptions())

with open(os.path.join(OUTPUT_DIR, FILE), "r") as file:
  json_data = file.read()
        
data_dict = json.loads(json_data)

wait = WebDriverWait(driver, 10)

q_as = {}

for page, links in data_dict.items():
  i = 0
  q_as[f"{page}"] = {}
  for url in links:
    
    try:
      q_as[f"{page}"][f"{str(i)}"] = {}
      q_as[f"{page}"][f"{str(i)}"]["question"] = {}
      # Navigate to the question url
      driver.get(url)
      
      id = f"{page}_{str(i)}"
      
      topic_tags = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "content-topic-tags")))
      
      topic_tags = topic_tags.text.split("\n")
      q_as[f"{page}"][f"{str(i)}"]["question"]['topic_tags'] = topic_tags
      
      content_question = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "content-question")))
    
      q_title = content_question.find_element(By.TAG_NAME, "h1").text
      q_as[f"{page}"][f"{str(i)}"]["question"]['title'] = q_title
      q_body = content_question.find_element(By.ID, "question-body").text
      q_as[f"{page}"][f"{str(i)}"]["question"]['body'] = q_body
    
      header_details = content_question.find_element(By.CLASS_NAME, "header-details")
      
      location = header_details.find_element(By.TAG_NAME, "span").text
      q_as[f"{page}"][f"{str(i)}"]["question"]['location'] = location
      date = header_details.find_element(By.TAG_NAME, "time").accessible_name
      q_as[f"{page}"][f"{str(i)}"]["question"]['date'] = date
      answers = header_details.find_element(By.CLASS_NAME, "answers-count").text
      q_as[f"{page}"][f"{str(i)}"]["question"]['answers'] = answers
      
      answers = re.findall(r'\d+', answers)[0]
    
    except Exception as e:
      # Handle any exceptions that may occur
      print(f"An error occurred: {e}")
      continue
      
    if int(answers) > 0:
      q_as[f"{page}"][f"{str(i)}"]["answers"] = {}
      
      answers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "qa-answer")))
      
      for answer in answers:
        try:
          q_as[f"{page}"][f"{str(i)}"]["answers"][f"{answers.index(answer)}"] = {}
          
          lawyer = answer.find_element(By.CLASS_NAME, "lawyer-info")
          lawyer_name = lawyer.find_element(By.TAG_NAME, "h3").text
          q_as[f"{page}"][f"{str(i)}"]["answers"][f"{answers.index(answer)}"]['lawyer_name'] = lawyer_name
          
          answer_body = answer.find_element(By.CLASS_NAME, "answer-body").text
          q_as[f"{page}"][f"{str(i)}"][
            "answers"][f"{answers.index(answer)}"]['answer_text'] = answer_body
          
          cta_answer = answer.find_element(By.CLASS_NAME, "cta-qa-content")
          help_count = cta_answer.find_element(By.CLASS_NAME, "answer-upvote-section").text
          q_as[f"{page}"][f"{str(i)}"][
            "answers"][f"{answers.index(answer)}"]['help_count'] = help_count
          
          agree_lawyers = cta_answer.find_element(By.CLASS_NAME, "agrees-lawyers").text
          q_as[f"{page}"][f"{str(i)}"][
            "answers"][f"{answers.index(answer)}"]['agree_lawyers'] = agree_lawyers
          
        except NoSuchElementException:
          continue
        except Exception as e:
          print(f"An error occurred: {e}")
          break
    
    i = i + 1
      
driver.quit()
        
        
folder_path = os.path.join(os.getcwd(), OUTPUT_DIR)

if not os.path.exists(folder_path):
  os.makedirs(folder_path)

json_data = json.dumps(q_as)

with open(os.path.join(folder_path, OUT), "w") as file:
      file.write(json_data)


