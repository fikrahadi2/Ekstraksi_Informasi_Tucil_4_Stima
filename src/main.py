# Nama	: Fikra Hadi Ramadhan
# NIM	: 13518036
# Hal   : Tugas Kecil 4 - Strategi Algoritma "15-Puzzle"
# Judul	: Ekstraksi Informasi dari Artikel Berita dengan Algoritma Pencocokan String


def kmpMatch(text, pattern):
	n = len(text)
	m = len(pattern)
	fail = []
	fail = computeFail(pattern)
	i = 0
	j = 0
	
	while (i < n):
		if (pattern[j] == text[i]):
			if (j == m - 1):
				return (i - m + 1) #cocok
			i += 1
			j += 1
		elif (j > 0):
			j = fail[j-1]
		else:
			i += 1
	return -1 #tidak cocok

def computeFail(pattern):
	fail = [0 for fail in range(len(pattern))]
	fail[0] = 0
	
	m = len(pattern)
	j = 0
	i = 1
	
	while (i < m):
		if (pattern[j] == pattern[i]): # cocok untuk j+1 chars
			fail[i] = j + 1
			i += 1
			j += 1
		elif (j > 0): #j mengikuti kecocokan prefix
			j = fail[j-1]
		else:
			fail[i] = 0
			i += 1
	
	return fail
	
def mainKMP(args):
	args[0] = str(input("Text: "))
	args[1] = str(input("Pattern: "))
	
	posn = kmpMatch(args[0], args[1])
	if (posn == - 1):
		print("Pattern not found")
	else:
		print("Pattern starts at posn " + str(posn))

def bmMatch(text, pattern):
	last = []
	last = buildLast(pattern)
	n = len(text)
	m = len(pattern)
	i = m - 1
	
	if (i > n-1):
		return -1 #tidak match jika pattern lebih panjang dari text
	
	j = m-1
	while (i <= n-1):
		if (pattern[j] == text[i]):
			if (j == 0):
				return i #cocok
			else: #looking-glass technique
				i -= 1
				j -= 1
		else: #character jump technique
			lo = last[ord(text[i])] #last occ
			i = i + m - min(j, 1+lo)
			j = m - 1
			
		if (i > n-1):
			break
	
	return -1 #tidak ada yang cocok
	
def buildLast(pattern):
	last = [-1 for last in range(128)]

	for i in range (len(pattern)):
		last[ord(pattern[i])] = i
	
	return last
		
def mainBM(args):
	args[0] = str(input("Text: "))
	args[1] = str(input("Pattern: "))
	
	posn = bmMatch(args[0], args[1])
	if (posn == -1):
		print("Pattern not found")
	else:
		print("Pattern starts at posn " + str(posn))
			
		
#Main Program
args = [0 for args in range(2)]
#mainKMP(args)
mainBM(args)
