import pyperclip
import requests
import json

TOKEN = ''

def remove_numbers(s):
	return ''.join(i for i in s if not i.isdigit())

if __name__ == '__main__':
	i = 139	
	response = requests.get('https://api-literature.edublock.ge/Chapter/Single', params={'creationId': 70, 'index': i}, headers={'Authorization': f'Bearer {TOKEN}'})
	content = json.loads(response.text)['content']
	result = content#remove_numbers(content)
	print(result)
	print(len(result))

	pyperclip.copy(result)
