import requests


url = 'http://192.168.1.110:9999/robotservice/parameter/export'
res = requests.request("GET", url)
print(res.json()[0]['groups'])