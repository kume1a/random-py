import os
import requests
import json

ACCESS_TOKEN = ''
URL = 'https://api-literature.edublock.ge'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


def upload_audio(chapter_id, audio_path):
    audio_file = open(audio_path, 'rb')

    files = {
        'AudioFile': (os.path.basename(audio_path), audio_file)
    }

    requests.patch(f'{URL}/Chapter/{chapter_id}', headers=headers, files=files)
    audio_file.close()


def get_episode_id(name):
    response = requests.get(f'{URL}/Episode',
                            params={'searchQuery': name, 'pageSize': 10, 'page': 1},
                            headers=headers)
    json_response = json.loads(response.text)
    assert len(json_response['data']) == 1
    return json_response['data'][0]['id']


def get_creation_id(name):
    response = requests.get(f'{URL}/Creation/All',
                            params={'searchQuery': name},
                            headers=headers)
    json_response = json.loads(response.text)
    assert len(json_response) == 1
    return json_response[0]['id']


def get_chapter_id(creation_id, index, episode_id):
    response = requests.get(f'{URL}/Chapter/Single',
                            params={'creationId': creation_id, 'index': index, 'episodeId': episode_id},
                            headers=headers)
    json_response = json.loads(response.text)
    return json_response['id']


def main():
    for entry in os.listdir('audio'):
        entry_path = 'audio/' + entry
        if os.path.isdir(entry_path):
            creation_id = get_creation_id(entry)
            for inner_entry in os.listdir(entry_path):
                inner_entry_path = entry_path + '/' + inner_entry
                if os.path.isdir(inner_entry_path):
                    episode_id = get_episode_id(inner_entry)
                    for inner_inner_entry in os.listdir(inner_entry_path):
                        chapter_id = get_chapter_id(creation_id, int(inner_inner_entry.split('.mp3')[0]), episode_id)
                        upload_audio(chapter_id, f'{inner_entry_path}/{inner_inner_entry}')
                        print(f'{entry}, {inner_entry}, {inner_inner_entry} OK')

                elif os.path.isfile(inner_entry_path):
                    chapter_id = get_chapter_id(creation_id, int(inner_entry.split('.mp3')[0]), None)
                    upload_audio(chapter_id, inner_entry_path)
                    print(f'{entry}, {inner_entry} OK')
        elif os.path.isfile(entry_path):
            print(f'{entry} OK')
            creation_id = get_creation_id(entry.split('.mp3')[0])
            chapter_id = get_chapter_id(creation_id, 0, None)
            upload_audio(chapter_id, entry_path)


if __name__ == '__main__':
    main()
