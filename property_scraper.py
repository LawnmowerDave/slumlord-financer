import requests
import urllib

print('start')
URL = 'https://www.loopnet.com/'
# page = requests.get(URL, timeout=5)
page = urllib.request.urlopen(URL)

print(page)