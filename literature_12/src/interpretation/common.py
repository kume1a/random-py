#!python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_soup(url):
    response = None
    try:
        response = requests.get(url, timeout=30)
    except Exception:
        pass

    if not response or response.status_code == 403:
        return None

    return BeautifulSoup(response.text, "html.parser")


def get_file_soup(path):
    file = open(path, 'r', encoding='utf-8')
    file_content = file.read()
    file.close()

    return BeautifulSoup(file_content, "html.parser")


def scrape_definitions(url):
    soup = get_soup(url)

    if not soup:
        return None

    term_h1 = soup.find('h1', {'class': 'term'})
    term = term_h1.text if term_h1 else None

    defs_block = soup.find(class_='defnblock')
    defs = defs_block.find_all(class_='defn') if defs_block else None

    if not defs:
        return None

    return {
        'term': term.strip(),
        'definitions': list(map(lambda e: e.text.strip(), defs))
    }


def is_url(value):
    return re.match(URL_REGEX, value) is not None


def read_file_as_json(path):
    f = open(path, 'r')
    f_content = f.read()
    f.close()

    return json.loads(f_content)


def write_json_to_file(path, json_data):
    with open(path, 'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
