#!python3
# -*- coding: utf-8 -*-
import json
import time

from src.interpretation.common import get_soup, is_url, scrape_definitions

data = []
definitions = []

current_url = ""  # insert source url start

while current_url:
    time.sleep(1)
    soup = get_soup(current_url)

    inline_list = soup.find('div', {'class': 'defnblock'})

    inline_list_rows = inline_list.find_all('dt')

    title_index = soup.find('h1', {'class': 'term'}).text

    title_div = soup.find('div', {'class': 'defn'})
    title = title_div.text if title_div else None

    print(f'\n\nscraping page: {current_url}')

    for index, dt in enumerate(inline_list_rows):
        # noinspection DuplicatedCode
        if index == len(inline_list_rows) - 1:
            next_page_anchors = dt.find_all('a')
            reverse_counter = 1
            while not next_page_anchors:
                next_page_anchors = inline_list_rows[index - reverse_counter].find_all('a')
                reverse_counter += 1

                if reverse_counter > 100:
                    print('reverse_counter exceeded 100, exiting')
                    exit(1)

            if not next_page_anchors:
                current_url = None

            current_url = next_page_anchors[-1]['href']
            break

        text = dt.get_text()

        for definition_anchor in dt.find_all('a'):
            definition_url = definition_anchor['href']

            if not is_url(definition_url):
                print(f'malformed definition url: {definition_url}')
                continue

            print(f'scraping definition: {definition_url}')

            scraped_definition = scrape_definitions(definition_url)
            if scraped_definition:
                definitions.append(scraped_definition)

            time.sleep(1)

        data.append({
            'text': text,
            'definitions': definitions.copy(),
        })
        definitions.clear()

    with open(f'{title_index} - {title}.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    data.clear()
