import requests, json, math

from requests.api import request

term = '202103'
r = requests.get('https://prd-xereg.temple.edu/StudentRegistrationSsb/ssb/term/search', params={'term':term})
jar = r.cookies

pageSize = 500
offset = 0
r = requests.get('https://prd-xereg.temple.edu/StudentRegistrationSsb/ssb/searchResults', params={'txt_term':term, 'pageOffset': offset, 'pageMaxSize':pageSize},cookies=jar)
content = r.json()
total = content['totalCount']
results = content['data']
offset += pageSize

while offset < total:
    r = requests.get('https://prd-xereg.temple.edu/StudentRegistrationSsb/ssb/searchResults', params={'txt_term':term, 'pageOffset': offset, 'pageMaxSize':pageSize},cookies=jar)
    results += r.json()['data']
    offset += pageSize

with open(f'testing/temple-{term}.json','w') as file:
    json.dump(results,file)
