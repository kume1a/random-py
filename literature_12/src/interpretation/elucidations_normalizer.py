#!python3
# -*- coding: utf-8 -*-

import csv
import os
import re

from src.interpretation.common import read_file_as_json, write_json_to_file


def read_csv(path):
    f = open(path, 'r')

    reader = csv.reader(f)

    rows = []
    for row in reader:
        rows.append(row)

    f.close()

    return rows


def normalize_initial(write=True):
    source_folders = []

    for folder in source_folders:
        files = os.listdir(folder)

        all_blocks = []
        elucidations = []
        no_matches = []
        error_terms = []
        elucidation_intersects = []

        for file in files:
            blocks = read_file_as_json(f'./{folder}/{file}')

            content = "\n".join(map(lambda e: e['text'], blocks))

            for definitions in map(lambda e: e['definitions'], blocks):
                definitions.sort(key=lambda e: len(e['term']), reverse=True)

                for definition in definitions:
                    term = definition['term']

                    if not term:
                        continue

                    try:
                        term_pattern = re.compile(term)
                    except re.error:
                        error_terms.append(definition)
                        continue

                    match = None

                    already_found_match_count = len(list(filter(
                        lambda e: e['termSearchQuery'] == term,
                        elucidations)
                    ))

                    matches = term_pattern.finditer(content)
                    for m in matches:
                        if already_found_match_count != 0:
                            already_found_match_count -= 1
                            continue
                        match = m
                        break

                    if not match:
                        no_matches.append(definition)
                        continue

                    elucidations.append({
                        'termSearchQuery': term,
                        'termStartPosition': match.span()[0],
                        'termEndPosition': match.span()[1],
                        'definitions': definition['definitions']
                    })

            intersects = []
            for e_index, elucidation in enumerate(elucidations):
                elucidation_span = (
                    elucidation['termStartPosition'],
                    elucidation['termEndPosition']
                )

                for e_iter_index, elucidation_iter in enumerate(elucidations):
                    if e_index == e_iter_index:
                        continue

                    elucidation_iter_span = (
                        elucidation_iter['termStartPosition'],
                        elucidation_iter['termEndPosition']
                    )

                    if range_intersect(elucidation_span, elucidation_iter_span):
                        elucidations.remove(elucidation)
                        print(
                            f'removing intersect {elucidation["termSearchQuery"]} | {elucidation_iter["termSearchQuery"]}')
                        intersects.append(elucidation)
                        break

            title = file.strip('.json')
            if intersects:
                elucidation_intersects.append({
                    'title': title,
                    'elucidation_intersections': intersects.copy()
                })
                intersects.clear()

            all_blocks.append({
                'title': title,
                'index': 0,
                'content': content,
                'elucidations': elucidations.copy()
            })

            elucidations.clear()

        if write:
            write_json_to_file(f'./normalized/{folder}.json', all_blocks)
            write_json_to_file(f'./no_matches/{folder}.json', no_matches)
            write_json_to_file(f'./error_terms/{folder}.json', error_terms)
            write_json_to_file(f'./elucidation_intersects/{folder}.json', elucidation_intersects)


def normalize_elucidations():
    elucidations = []

    for file in os.listdir('./normalized'):
        file_data = read_file_as_json(f'./normalized/{file}')

        for chapter in file_data:
            for chapter_elucidation in chapter['elucidations']:
                elucidation_map = {
                    'term': chapter_elucidation['termSearchQuery'],
                    'values': chapter_elucidation['definitions']
                }

                if elucidation_map in elucidations:
                    continue

                elucidations.append({
                    'term': chapter_elucidation['termSearchQuery'],
                    'values': chapter_elucidation['definitions']
                })

    write_json_to_file('elucidations.json', elucidations)


def print_elucidation_duplicates():
    elucidations = read_file_as_json('./elucidations.json')

    elucidation_terms = list(map(lambda e: e['term'], elucidations))
    term_duplicates = set([e for e in elucidation_terms if elucidation_terms.count(e) > 1])

    print(term_duplicates)


def range_intersect(r1, r2):
    return range(max(r1[0], r2[0]), min(r1[1], r2[1])) or None

# print_elucidation_duplicates()
# normalize_initial(write=True)
# normalize_elucidations()
# upload_elucidations()
