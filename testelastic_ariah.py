# from elasticsearch import Elasticsearch
from utils.ariah_elasticsearch import ElasticSearch as ariah

import json
import os

client = ariah()

# documents = [
#   { "index": { "_index": "jorge", "_id": "9780553351927"}},
#   {"name": "Snow Crash", "author": "Neal Stephenson", "release_date": "1992-06-01", "page_count": 470, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": False},
#   { "index": { "_index": "jorge", "_id": "9780441017225"}},
#   {"name": "Revelation Space", "author": "Alastair Reynolds", "release_date": "2000-03-15", "page_count": 585, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": False},
#   { "index": { "_index": "jorge", "_id": "9780451524935"}},
#   {"name": "1984", "author": "George Orwell", "release_date": "1985-06-01", "page_count": 328, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": False},
#   { "index": { "_index": "jorge", "_id": "9781451673319"}},
#   {"name": "Fahrenheit 451", "author": "Ray Bradbury", "release_date": "1953-10-15", "page_count": 227, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": False},
#   { "index": { "_index": "jorge", "_id": "9780060850524"}},
#   {"name": "Brave New World", "author": "Aldous Huxley", "release_date": "1932-06-01", "page_count": 268, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": False},
#   { "index": { "_index": "jorge", "_id": "9780385490818"}},
#   {"name": "The Handmaid's Tale", "author": "Margaret Atwood", "release_date": "1985-06-01", "page_count": 311, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": False},
# ]

# client.create_index(name="alicia", mapping={})

# OUTPUT_DIR = "web_out"
# FILE = "test.json"


# with open(os.path.join(OUTPUT_DIR, FILE), "r") as file:
#   json_data = file.read()

# data = json.loads(json_data)

# client.es.bulk(body=data, pipeline="ent-search-generic-ingestion")



# client.bulk(body=documents, pipeline="ent-search-generic-ingestion")


result = client.es.search(index="alicia", q="snow")

print(result)

# print(client.info())

# try:
#     response = client.create_index(name="my_search", mapping=json_data)
#     print("Data ingested successfully:", response)
# except Exception as e:
#     print("Error ingesting data:", e)
 