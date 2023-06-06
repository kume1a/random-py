import requests

API_URL = 'http://localhost:5029'

ACCESS_TOKEN = ''
REFRESH_TOKEN = ''

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


def refresh():
    res = requests.post(f'{API_URL}/Authentication/Refresh', json={'refreshToken': REFRESH_TOKEN})

    print(res.text)


def sign_in(email, password):
    res = requests.post(f'{API_URL}/Authentication/SignIn', json={'email': email, 'password': password})

    print(res.text)


if __name__ == '__main__':
    sign_in('email', 'password')
