from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from elasticsearch import Elasticsearch

r = requests.get('https://www.patreon.com/explore?ru=%2F')
soup = BeautifulSoup(r.content, 'html.parser')
for category_item in soup.find_all(attrs={'data-tag': 'category-item'}):
    cat_name = category_item['data-menu-item']
    cat_uri = category_item.find('a')['href']
    cat_url = urljoin('https://www.patreon.com/', cat_uri)
    if cat_name == 'All':
        continue
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    es.index(index=cat_name, doc_type='creators', body={'url': cat_url, 'creators': []})
