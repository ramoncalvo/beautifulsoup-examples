#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
index = 'machine_learning_projects_showcase'
es.indices.create(index=index, ignore=400)

r = requests.get('https://ml-showcase.com/')

page = BeautifulSoup(r.content, 'html.parser')
pfitems = page.find_all('div', class_='portfolio-title')
for item in pfitems:
    links = item.find_all('a')
    title = links[0].string
    link = links[0]['href']
    short_desc = links[1].string

    doc = {
        'title': title,
        'short_desc': short_desc,
        'url': link
    }
    print(doc)
    es.index(index=index, doc_type='projects', body=doc)
