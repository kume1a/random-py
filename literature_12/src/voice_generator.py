import requests
import json

URL = 'https://app.micmonster.com'

cookie = '_gcl_au=1.1.809002848.1671126146; _gid=GA1.2.1540256434.1671126146; _fbp=fb.1.1671126146368.1531720691; LaVisitorId_bWljbW9zdGVyLmxhZGVzay5jb20v=px5c95qn4ydnn4oguex4ftwcjjet0; ci_session=n2eqsome5n4jd8mhrqkp5nn7et9ra58e; _ga=GA1.1.28140613.1671126146; LaSID=k74o6czv71f4uvhm4wgusxoy58wn0; cid=email; cpass=pass; _ga_VHHE5NCHJL=GS1.1.1671126145.1.1.1671126403.0.0.0'

s = requests.session()
s.cookies.set('Cookie', cookie)
# res = s.post(f'{URL}/generate-voice', data={
#     'text': 'ტესტი ტესტი',
#     'language': 'Georgian (Georgia)',
#     'language_code': 'ka-GE',
#     'voice': 'ka-GE-EkaNeural',
#     'voice_gender': 'Female',
#     'project_id': 'aae935f2-263a4100-b58c7ae7-ddf8b443',
#     'project_id_plain': '31402',
#     'humanname': 'Eka',
#     'tts_type': 'MS',
#     'voice_style': '',
#     'msspeed': '0',
#     'mspitch': '0',
#     'csrf_test_name': '99027dc3b293475d37c90e89fae744f5',
#     'featureType': 'generate',
#     'user_voice_name': 'ტესტ',
# })
#
# print(res.status_code)
# print(res.text)

# list_res = s.post(f'{URL}/list-voices', data={
#     'start': '0',
#     'limit': '25',
#     'search': '',
#     'sortBy': 'created_at',
#     'sortOrder': 'DESC',
#     'project_id': 'aae935f2-263a4100-b58c7ae7-ddf8b443',
#     'project_id_plain': '31402',
#     'csrf_test_name': '643294190f7551d15d411b51867b5374',
# })
#
# for voice in json.loads(list_res.content.decode('utf-8'))['voices']:
#     voice_data = s.get(f'{URL}/download-voice/{voice["id"]}')
#
#     with open(f'{voice["user_voice_name"]}_{voice["id"]}.mp3', 'wb') as f:
#         f.write(voice_data.content)
#     print(voice['id'])

res = requests.post(f'{URL}/login', json={'email': 'email', 'password': 'password'})
print(res.status_code)
print(len(res.cookies))
for cookie in res.cookies:
    print(cookie.value)