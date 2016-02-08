def my_upper(s):
	new = ''
	for c in s:
		asci = ord(c)
		if asci <= 122 and asci >= 97:
			c = chr(asci - 32)		
			new += c
		else:
			new += c
	return new

def my_count(s, substr):
	counter = 0
	i = 0
	while i < len(s):
		if s[i] == substr[0] and s[i:i + len(substr)]  == substr:
			i += len(substr)
			counter += 1
		else:
			i += 1		
	return counter

def my_find(s, target):
    if target in s:
    	for i in range(len(s)):
    		if s[i:i+len(target)] == target:
    			return i
    return -1 

def my_isalpha(s):
	for c in s:
		asci = ord(c)
		if not((asci >= 65 and asci <= 90) or (asci >= 97 and asci <= 122)):
			return False
	return True

def my_join(sep, col):
	if len(col) == 0:
		return ''
	res = ''
	res += col[0]
	i = 1
	while  i < len(col):
		res += sep + col[i]
		i += 1
	return res

def my_split(word, sep = ' '):
	res = []
	tracker = 0
	for c in range(len(word)):
		if word[c] == sep[0]:
			if c + len(sep) < len(word) and word[c: c+ len(sep)] == sep:
				res.append(word[tracker : c])
				tracker = c + len(sep)
	if tracker > 0:
		res.append(word[tracker:])
	return res

#test
#print(my_upper('Hello'))
#print()
#print(my_find('the cat and a dog', 'cat'))
#print(my_join('@asdf', ['Hello', 'how', 'Are', 'You', '?']))
#for w in my_split('testing@athis@afunction', sep = '@a'):
#	print(w)


