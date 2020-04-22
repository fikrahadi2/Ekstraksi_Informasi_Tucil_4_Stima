# Nama	: Fikra Hadi Ramadhan
# NIM	: 13518036
# Hal   : Tugas Kecil 4 - Strategi Algoritma
# Judul	: Ekstraksi Informasi dari Artikel Berita dengan Algoritma Pencocokan String
import re
from os import listdir
from os.path import isfile, join

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
	
def mainKMP(text, keyword, filename, hasil2):
	waktuArtikel = getWaktuArtikel(text)
	low = text.lower()
	pattern = keyword.lower()
	posn = kmpMatch(low, pattern)
	if (posn == -1):
		print("Keyword not found")
	else:
		kalimat = kalimatRegex(text, keyword)
		span = searchSpanPattern(kalimat, keyword)
		waktu = waktuRegex(kalimat, waktuArtikel)
		jumlah = jumlahRegex(kalimat, keyword, span)
		for i in range(len(kalimat)):
			data = {}
			data['jumlah'] = jumlah[i]
			data['waktu'] = waktu[i]
			data['kalimat'] = kalimat[i]
			data['filename'] = filename
			hasil2.append(data)

def bmMatch(text, pattern):
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
		
def mainBM(text, keyword, filename, hasil2):
	waktuArtikel = getWaktuArtikel(text)
	low = text.lower()
	pattern = keyword.lower()
	posn = bmMatch(low, pattern)
	if (posn == -1):
		print("Keyword not found")
	else:
		kalimat = kalimatRegex(text, keyword)
		span = searchSpanPattern(kalimat, keyword)
		waktu = waktuRegex(kalimat, waktuArtikel)
		jumlah = jumlahRegex(kalimat, keyword, span)
		for i in range(len(kalimat)):
			data = {}
			data['jumlah'] = jumlah[i]
			data['waktu'] = waktu[i]
			data['kalimat'] = kalimat[i]
			data['filename'] = filename
			hasil2.append(data)

def jumlahRegex(kal, pattern, span):
	x = len(kal)
	jumlah = [0 for x in range(x)]
	for i in range(x):
		jumlahnya = []
		jumlah_regex = re.compile(r'(?:^|(?<=\s| ))(\d+(\.\d{3})?)(?=\s)', re.I)
		jumlahnya = jumlah_regex.search(kal[i])
		if (jumlahnya != None):
			min = span[i] - jumlahnya.span()[1]
			temp = jumlahnya.group()
			for match in jumlah_regex.finditer(kal[i]):
				if(min >= (span[i] - match.span()[1])):
					min = span[i] - match.span()[1]
					temp = match
			jumlah[i] = temp.group()
	return jumlah

def searchSpanPattern(kalimat, pattern):
	pat = re.compile(r'(' + pattern + r')', re.I)
	spanPat = []
	for i in range(len(kalimat)):
		posn = pat.search(kalimat[i])
		for match in pat.finditer(kalimat[i]):
			spanPat.append(match.span()[1])
	return spanPat
			
def waktuRegex(kal, waktuArtikel):
	x = len(kal)
	waktu = [0 for waktu in range(x)]
	for i in range(x):
		#Asumsi waktu/tanggalnya sesuai seperti contoh text
		#dimana ada 'Hari' lalu tanggal bebas, lalu ada "Jam" + WIB/WITA/WIT (asumsi juga waktu di Indonesia)
		waktu_regex = re.compile(r'((Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Minggu)?[\,\s]?\(?\d+[\/\-\s](\d+|Januari|Jan|Februari|Feb|Maret|Mar|April|Apr|Mei|Juni|Jun|Juli|Jul|Agustus|Agus|Agu|Ags|September|Sep|Oktober|Okt|November|Nov|Desember|Des)[\/\-\s]\d+\)?([,]?[ ]?Pukul|pukul)?(\s[\d]{1,2}[.:][\d]{2}\sWIB|WITA|WIT?)?)', re.I)
		waktunya = waktu_regex.search(kal[i])
		if (waktunya == None):
			waktu[i] = waktuArtikel
		else:
			waktu[i] = waktunya.group()
	return waktu
					
def kalimatRegex(text, pattern):
	kalimat_regex = re.compile(r'(?:^|[\.\n]\s)(.*?' + pattern + r'.*?)(?=\.\s|\n)', re.I)
	kal = kalimat_regex.findall(text)
	return kal
	
def getWaktuArtikel(text):
	waktu_artikel = re.compile(r'((Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Minggu)?[\,\s]?\s?\(?\d+[\/\-\s](\d+|Januari|Jan|Februari|Feb|Maret|Mar|April|Apr|Mei|Juni|Jun|Juli|Jul|Agustus|Agus|Agu|Ags|September|Sep|Oktober|Okt|November|Nov|Desember|Des)[\/\-\s]\d+\)?([,]?[ ]?Pukul|pukul)?(\s[\d]{1,2}[.:][\d]{2}\sWIB|WITA|WIT?)?)', re.I)
	waktu = waktu_artikel.search(text)
	return waktu.group()
				
def mainRegex(text, keyword, filename, hasil2):
	waktuArtikel = getWaktuArtikel(text)
	low = text.lower()
	pattern = keyword.lower()
	posn = searchSpanPattern(low, pattern)
	if (len(posn) < 0):
		print("Keyword not found")
	else:
		kalimat = kalimatRegex(text, keyword)
		span = searchSpanPattern(kalimat, keyword)
		waktu = waktuRegex(kalimat, waktuArtikel)
		jumlah = jumlahRegex(kalimat, keyword, span)
		for i in range(len(kalimat)):
			data = {}
			data['jumlah'] = jumlah[i]
			data['waktu'] = waktu[i]
			data['kalimat'] = kalimat[i]
			data['filename'] = filename
			hasil2.append(data)

def openApp(upDir, pattern, opsi):
	files = [f for f in listdir(upDir) if isfile(join(upDir, f))]
	artikel = []
	for op in files:
		upPath = upDir + '/' + op
		f = open(upPath, "r")
		artikel_2 = f.read()
		artikel.append({"artikel": artikel_2, "filename": op})
		
	hasil = []
	for berita in artikel:
		text = berita["artikel"]
		filename = berita["filename"]
		if (opsi == "opsi1"):
			mainKMP(text, pattern, filename, hasil)
		elif (opsi == "opsi2"):
			mainBM(text, pattern, filename, hasil)
		elif (opsi == "opsi3"):
			mainRegex(text, pattern, filename, hasil)
	return hasil
