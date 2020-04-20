# Nama	: Fikra Hadi Ramadhan
# NIM	: 13518036
# Hal   : Tugas Kecil 4 - Strategi Algoritma "15-Puzzle"
# Judul	: Ekstraksi Informasi dari Artikel Berita dengan Algoritma Pencocokan String
import re

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
	args[0] = str(input("Nama File: "))
	args[1] = str(input("Keyword: "))
	File = open(args[0], "r")
	text = File.read()
	posn = kmpMatch(args[0], args[1])
	if (posn == - 1):
		print("Keyword not found")
	else:
		#print("Pattern starts at posn " + str(posn))
		kal = kalimatRegex(text, args[1], args[0])

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
	args[0] = str(input("Nama File: "))
	args[1] = str(input("Keyword: "))
	File = open(args[0], "r")
	text = File.read()
	posn = bmMatch(text, args[1])
	if (posn == -1):
		print("Keyword not found")
	else:
		#print("Pattern starts at posn " + str(posn))
		kalimat = kalimatRegex(text, args[1], args[0])
		jumlahRegex(text, kal)

#def jumlahRegex(text, kal):
#	x = len(kal)
#	for i in range(x):
#		jumlah_regex = re.compile(r'

#def waktuRegex(text, kal):
#	x = len(kal)
#	for i in range(x):
#		waktu_regex = re.compile(r'
					
def kalimatRegex(text, pattern, filename):
	kalimat_regex = re.compile(r'(?:^|[\.\n] )(.*?' + pattern + r'.*?)(?=[\.\n])', re.I)
	kal = kalimat_regex.findall(text)
	#print(kal[0] + '.' + " (" + str(filename) + ")")
	#print(kal[1] + '.' + " (" + str(filename) + ")")
	return kal
	
#Main Program
args = [0 for args in range(2)]
#mainKMP(args)
mainBM(args)
