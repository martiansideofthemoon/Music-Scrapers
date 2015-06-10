import mechanize,bs4,os,sys,re

def checkInvalid(songName=None,checkCover=True,checkRemix=True):
	isValid=True
	coverMatch = re.compile('cover',re.I)
	if not coverMatch.search(songName)==None and checkCover==True:
		isValid=False
	remixMatch = re.compile('remix',re.I)
	if not remixMatch.search(songName)==None and checkRemix==True:
		isValid=False
	return isValid
def getSongDetails(query=""):
	songDetails = {'search_query':query}
	return songDetail
query=""
i=0
for part in sys.argv[1:]:
	query=query+part+' '
query=query[:len(query)-1]
br = mechanize.Browser()
br.set_handle_robots( False )
br.addheaders = [('User-agent', 'Firefox')]
try:
	br.open('http://mp3skull.cr')
	for form in br.forms():
		if form.attrs['id']=='f1':
			br.form = form
			break
	br['q'] = query
	response = br.submit()
	finalpage = bs4.BeautifulSoup(response.read())
	maindivs=[]
	for div in finalpage.select('div'):
		desiredExpression = re.compile(r'show\d+')
		if 'class' in div.attrs:
			isFound = desiredExpression.search(div.attrs['class'][0])
			if not isFound == None:
				maindivs.append(div)
	for maindiv in maindivs:
		songTitle = maindiv.find('b').getText()
		isValid = checkInvalid(songTitle,True,True)
		if isValid==True:
			links=maindiv.find_all('a')
			wget = os.system("wget \""+links[0].get('href')+"\" -P ~/Music/")
			if wget==0:
				break
except:
	print "Please check your internet connection. Or else, try again later."



 