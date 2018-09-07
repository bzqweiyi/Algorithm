import urllib.request

url = r'http://www.baidu.com/'
res = urllib.request.urlopen(url)
html = res.read().decode('utf-8')
print(html)