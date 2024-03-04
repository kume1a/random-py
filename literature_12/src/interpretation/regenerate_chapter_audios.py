import requests
import json

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6Imt1bWVsYTAxMUBnbWFpbC5jb20iLCJVc2VySWQiOiI2IiwibmJmIjoxNjk4MzMzODM3LCJleHAiOjE3MDA5MjU4MzcsImlhdCI6MTY5ODMzMzgzN30.aVUIjVYRJJndcA9DKUAvR5XhWIFR7BkLHJUEWneo4ff0kS1PywPZTK0hP0Mzw442zzlAVw8WgZfjD3rKEqUtsQ'
}

chapters = requests.get('https://api-literature.edublock.ge/Chapter/All?creationId=69', headers=headers)
chapters_json = json.loads(chapters.text)

for chapter in chapters_json:
    chapter_id = chapter['id']
    chapter_title = chapter['title']
    chapter_index = chapter['index']

    if chapter_index <= 32:
        continue

    regenerate_audio_res = requests.patch(f'https://api-literature.edublock.ge/Chapter/{chapter_id}/RegenerateAudio',
                                          headers=headers)

    print(
        f'chapter id={chapter_id}, title={chapter_title}, index={chapter_index} -- {regenerate_audio_res.status_code}')

    if not regenerate_audio_res.ok:
        print(regenerate_audio_res.text)
        # break
