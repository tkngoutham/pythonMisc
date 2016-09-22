import request

url = "http://192.168.10.100/upload"
files = {'file': open('/Users/djangod/text.txt', 'rb')}
r = requests.post(url, files=files)