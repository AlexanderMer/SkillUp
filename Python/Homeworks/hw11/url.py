import urllib.request

html_content = urllib.request.urlopen('''http://www.yahoo.com''').read().decode()

temp = html_content.split('<a href="')
links = []
for l in range(1, len(temp)):
	links.append(temp[l][:temp[l].find('"')])
for l in links:
	print(l)
