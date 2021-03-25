import requests, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--term', dest='term', help='Term code')
parser.add_argument('--file',dest='file',help='File to write output to')
args = parser.parse_args()

r = requests.get('https://prd-xereg.temple.edu/StudentRegistrationSsb/ssb/term/search', params={'term':args.term})
jar = r.cookies

pageSize = 500
offset = 0
r = requests.get('https://prd-xereg.temple.edu/StudentRegistrationSsb/ssb/searchResults', params={'txt_term':args.term, 'pageOffset': offset, 'pageMaxSize':pageSize},cookies=jar)
content = r.json()
total = content['totalCount']
results = content['data']
offset += pageSize

while offset < total:
    r = requests.get('https://prd-xereg.temple.edu/StudentRegistrationSsb/ssb/searchResults', params={'txt_term':args.term, 'pageOffset': offset, 'pageMaxSize':pageSize},cookies=jar)
    results += r.json()['data']
    offset += pageSize

with open(args.file,'w') as file:
    json.dump(results,file)
