#!python3
# -*- coding: utf-8 -*-
import re
import time
import os
import json

from src.interpretation.common import get_soup, is_url, scrape_definitions, read_file_as_json, write_json_to_file

DIR = 'ვეფხისტყაოსანი'
if not os.path.exists(DIR):
    os.mkdir(DIR)

os.chdir(DIR)


def get_current_url(dt, inline_list_rows, index):
    next_page_anchors = dt.find_all('a')
    reverse_counter = 1
    while not next_page_anchors:
        next_page_anchors = inline_list_rows[index - reverse_counter].find_all('a')
        reverse_counter += 1

        if reverse_counter > 100:
            print('reverse_counter exceeded 100, exiting')
            exit(1)

    if not next_page_anchors:
        return None

    return next_page_anchors[-1]['href']


def main():
    title = ''
    lines = []
    data = []
    definitions = []
    i = 47

    current_url = "http://www.nplg.gov.ge/saskolo/index.php?a=term&d=18&t=21030" # insert start url here

    while current_url:
        time.sleep(1)
        soup = get_soup(current_url)

        nested_inline_list_rows = map(
            lambda li: li.find('div', {'class': 'gwusg'}).find_all('dt'),
            soup.find('ol', {'class': 'defnblock'}).find_all('li')
        )

        inline_list_rows = [item for sublist in nested_inline_list_rows for item in sublist]

        print(f'\n\nscraping page title number {i} url = {current_url}')

        for index, dt in enumerate(inline_list_rows):
            if index == len(inline_list_rows) - 1:
                current_url = get_current_url(dt, inline_list_rows, index)
                break

            text = dt.get_text()

            if re.match('\\d', text):
                title = dt.get_text()
                continue

            if not re.match('\\(.+\\)', text):
                continue

            sanitized_line_text = re.sub('\\(.+\\) ', '', text.replace('იხ. ტაეპის განმარტებანი', ''))

            current_scraped_text = '\n\n'.join(list(map(lambda e: e['text'], data))) \
                                   + ('\n\n' if data  else'') \
                                   + "\n".join(lines) \
                                   + ('\n' if lines else '')

            start_index = len(current_scraped_text)
            elucidation_anchors = dt.find_all('a', recursive=False)

            # print(f'start_index = {start_index}')

            for definition_anchor in elucidation_anchors:
                if definition_anchor.text == 'იხ. ტაეპის განმარტებანი':
                    continue

                definition_url = definition_anchor['href']

                if not is_url(definition_url):
                    print(f'malformed definition url: {definition_url}')
                    continue

                print(f'scraping definition: {definition_url}')

                scraped_definitions = scrape_definitions(definition_url)


                should_trim_anchor_text = sanitized_line_text== 'ზედა დავსვი ტახტსა ჩემსა, შევეკვეთე, გავესულე.'# for edge cases
                elucidation_start_index = sanitized_line_text.index(
                    definition_anchor.text.lstrip() if should_trim_anchor_text else definition_anchor.text
                )
                elucidation_end_index = elucidation_start_index + len(definition_anchor.text)

                if elucidation_end_index + start_index == 925:
                    print(1)

                if scraped_definitions:
                    definitions.append({
                        'term': scraped_definitions['term'],
                        'definitions': scraped_definitions['definitions'],
                        'termStartPosition': start_index + elucidation_start_index,
                        'termEndPosition': start_index + elucidation_end_index
                    })

                # time.sleep(1)

            lines.append(sanitized_line_text)

            if len(lines) == 4:
                block = "\n".join(lines)
                data.append({
                    'title': title,
                    'text': block,
                    'definitions': definitions.copy(),
                })

                lines.clear()
                definitions.clear()
                title = ''

        with open(f'{i}.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        i += 1

        data.clear()


def normalize(write=False):
    files = os.listdir('.')
    all_blocks = []
    elucidations = []

    for file in files:
        blocks = read_file_as_json(file)

        content = "\n\n".join(map(lambda e: e['text'], blocks))

        for definitions in map(lambda e: e['definitions'], blocks):
            elucidations.extend(definitions)

        all_blocks.append({
            'index': int(file.strip('.json')) - 1,
            'content': content,
            'elucidations': elucidations.copy()
        })

        elucidations.clear()

    if write:
        write_json_to_file(f'../normalized/ვეფხისტყაოსანი.json', all_blocks)


# main()
normalize(write=True)
