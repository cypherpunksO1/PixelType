import pprint

import requests


response = requests.post('https://pixeltype.egoryolkin.ru/api/v1/post/create/', params={
    'title': '123'
})
result = response.json()
pprint.pprint(result)
