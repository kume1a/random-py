import requests
import os
import json
import base64

from src.upload_data.common import API_URL, headers


def read_content(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
        return json.loads(data)


def read_image(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        return base64.b64encode(data).decode('utf-8')


def upload_authors():
    authors = read_content('../../data/authors.json')
    for author in authors:
        image_path = 'data/author images/' + author['name'] + '.jpg'
        image = open(image_path, 'rb')

        body = {
            'Name': author['name'],
        }
        files = {
            'Image': (os.path.basename(image_path), image)
        }

        print('creating author ' + author['name'])
        requests.post(f'{API_URL}/Author', data=body, headers=headers, files=files)
        image.close()


def upload_creations():
    creations = read_content('../../data/creations.json')
    for creation in creations:
        image_path = 'data/creation images/' + creation['title'] + '.jpg'
        image = open(image_path, 'rb') if os.path.exists(image_path) else None

        body = {
            'Title': creation['title'],
            'AuthorId': 2,
            'GenreId': 1,
            'ReleaseDate': creation['release_date'],
            'ReleaseDateType': {'YEAR': 0, 'YEAR_RANGE': 1, 'CENTURY': 2}[creation['release_date_type']]
        }

        files = {
            'Image': (os.path.basename(image_path), image)
        } if image else None

        response = requests.post(f'{API_URL}/Creation', data=body, headers=headers, files=files)
        print(f'creating creation {creation["title"]}  response {response.status_code} {response.content}')

        if image:
            image.close()


def upload_creation_info_paragraphs():
    creations = list(
        map(lambda creation: {'id': creation['id'], 'title': creation['title']}, read_content(
            '../../data/creations.json')))
    real_creations = requests.get(f'{API_URL}/Creation/All', headers=headers)

    info_paragraphs = read_content('../../data/creation_info_paragraphs.json')
    for info_paragraph in info_paragraphs:
        body = {
            'Title': info_paragraph['title'],
            'Content': info_paragraph['data'],
            'Index': info_paragraph['index'] + 1,
            'CreationId': {
                creation['id']: [c['id'] for c in json.loads(real_creations.text) if c['title'] == creation['title']][0]
                for creation in creations
            }[info_paragraph['creation_id']]
        }

        requests.post(f'{API_URL}/InfoParagraph', headers=headers, json=body)


def upload_author_info_paragraphs():
    authors = read_content('../../data/authors.json')
    real_authors = requests.get(f'{API_URL}/Author/All', headers=headers)

    info_paragraphs = read_content('../../data/author_bio_paragraphs.json')
    for info_paragraph in info_paragraphs:
        body = {
            'Title': info_paragraph['title'],
            'Content': info_paragraph['data'],
            'Index': info_paragraph['index'] + 1,
            'AuthorId': {
                author['id']:
                    [a['id'] for a in json.loads(real_authors.text) if a['name'] == author['name']][0]
                for author in authors
            }[info_paragraph['author_id']]
        }

        requests.post(f'{API_URL}/InfoParagraph', headers=headers, json=body)


def upload_chapters():
    authors_response = requests.get(f'{API_URL}/Author/All', headers=headers)
    authors = json.loads(authors_response.text)

    creations = read_content('../../data/creations.json')
    real_creations = requests.get(f'{API_URL}/Creation/All', headers=headers)

    for author in authors:
        author_chapters = read_content('data/chapters/' + author['name'] + '.json')
        for chapter in author_chapters:
            if chapter['upper_chapter_id'] is not None:
                continue

            body = {
                'Title': chapter['title'],
                'Index': chapter['chapter'] + 1,
                'Content': chapter['data'],
                'CreationId': {
                    creation['id']:
                        [c['id'] for c in json.loads(real_creations.text) if c['title'] == creation['title']][0]
                    for creation in creations
                }[chapter['creation_id']]
            }

            res = requests.post(f'{API_URL}/Chapter', headers=headers, data=body)
            print(res.status_code)
            if res.status_code != 201:
                print(res.text)
                print(body)
                print('-' * 100)


def main():
    # upload_authors()
    # upload_creations()
    # upload_creation_info_paragraphs()
    # upload_author_info_paragraphs()
    # upload_chapters()

    # a = 0
    # for file in os.listdir('../../data/chapters'):
    #     content = read_content('../../data/chapters/' + file)
    #     a += len(content)
    # print(a)

    print('nothing executed')



if __name__ == '__main__':
    main()
