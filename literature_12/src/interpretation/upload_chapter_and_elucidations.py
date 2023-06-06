import requests
import json

from src.interpretation.common import read_file_as_json, write_json_to_file

DEVELOPMENT_ADMIN_BEARER = ''
PRODUCTION_ADMIN_TOKEN = ''

DEV_API_URL = 'http://localhost:5029'
PRODUCTION_API_URL = 'https://api-literature.edublock.ge'

API_URL = PRODUCTION_API_URL

HEADERS = {
    'Authorization': f'Bearer {PRODUCTION_ADMIN_TOKEN}'
}

chapter_index_to_id = {
    0: 2333, 1: 2334, 2: 2335, 3: 2336, 4: 2337, 5: 2338, 6: 2339, 7: 2340, 8: 2341,
    9: 2342, 10: 2343, 11: 2344, 12: 2345, 13: 2346, 14: 2347, 15: 2348, 16: 2349,
    17: 2350, 18: 2351, 19: 2352, 20: 2353, 21: 2354, 22: 2355, 23: 2356, 24: 2357,
    25: 2358, 26: 2359, 27: 2360, 28: 2361, 29: 2362, 30: 2363, 31: 2364, 32: 2365,
    33: 2366, 34: 2367, 35: 2368, 36: 2369, 37: 2370, 38: 2371, 39: 2372, 40: 2373,
    41: 2374, 42: 2375, 43: 2376, 44: 2377, 45: 2378, 46: 2379, 47: 2380, 48: 2381,
    49: 2382, 50: 2383, 51: 2384, 52: 2385, 53: 2386, 54: 2387, 55: 2388, 56: 2389,
    57: 2390, 58: 2391, 59: 2392, 60: 2393, 61: 2394, 62: 2395, 63: 2396,
}


def upload_chapter_with_elucidations():
    chapters = read_file_as_json('./normalized/ვეფხისტყაოსანი.json')

    for chapter in chapters:
        chapter_index = chapter["index"]

        if chapter_index not in chapter_index_to_id.keys():
            print(f'skipping index {chapter_index}')
            continue

        start_index = 8
        end_index = 8

        if chapter_index < start_index or chapter_index > (end_index):
            continue

        print(f'updating index {chapter_index}, id = {chapter_index_to_id[chapter_index]}')

        body = {
            # 'title': chapter['title'],
            # 'index': chapter['index'],
            'content': chapter['content'],
            # 'creationId': creation_id
        }

        # upsert_elucidations(chapter['elucidations'])

        for index, elucidation in enumerate(chapter['elucidations']):
            body[f'elucidations[{index}][termSearchQuery]'] = elucidation['term']
            body[f'elucidations[{index}][termStartPosition]'] = elucidation['termStartPosition']
            body[f'elucidations[{index}][termEndPosition]'] = elucidation['termEndPosition']

            for elucidation_value_index, elucidation_value in enumerate(elucidation['definitions']):
                body[f'elucidations[{index}][valuesSearchQuery][{elucidation_value_index}]'] = \
                    elucidation['definitions'][elucidation_value_index]

        res = requests.patch(
            f'{API_URL}/Chapter/{chapter_index_to_id[chapter_index]}',
            data=body,
            headers=HEADERS
        )

        print('ok' if res.ok else res.text)
        if not res.ok:
            break


def upsert_elucidations(elucidations):
    not_found_elucidations = []
    for elucidation in elucidations:
        params = {
            'term': elucidation['term'],
            'values': elucidation['definitions']
        }

        elucidation_search_res = requests.get(
            f'{API_URL}/Elucidation/All',
            params=params,
            headers=HEADERS
        )

        elucidations_search = json.loads(elucidation_search_res.text)

        elucidation_already_added = any([
            e['term'] == elucidation['term'] and \
            e['values'] == elucidation['definitions'] \
            for e in not_found_elucidations
        ])

        if not elucidations_search and not elucidation_already_added:
            not_found_elucidations.append(params)
            print(f'not found {elucidation["term"]}')

    upload_elucidations(not_found_elucidations)


def upload_elucidations(elucidations):
    elucidation_errors = []
    for elucidation in elucidations:
        print(f'creating {elucidation["term"]}')

        res = requests.post(
            f'{API_URL}/Elucidation',
            json={
                'term': elucidation['term'],
                'values': elucidation['values']
            },
            headers=HEADERS
        )

        if not res.ok:
            elucidation_errors.append({
                'message': res.text,
                'term': elucidation['term'],
                'values': elucidation['values']
            })
            print(res.text)

        write_json_to_file('./elucidation_errors.json', elucidation_errors)


upload_chapter_with_elucidations()
