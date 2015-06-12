import mechanize,bs4,os,sys,re

def checkInvalid(songDetails=None,checkCover=True,checkRemix=True,checkLength=True):
	songName=songDetails['songTitle']
	length=songDetails['songLength']
	isValid=True
	coverMatch = re.compile('cover',re.I)
	if length!=0 and length<=90 and checkLength==True:
		isValid=False
	if not coverMatch.search(songName)==None and checkCover==True:
		isValid=False
	remixMatch = re.compile('remix',re.I)
	if not remixMatch.search(songName)==None and checkRemix==True:
		isValid=False
	return isValid
def getSongDetails(query=""):
	
	return songDetail

query=""
for part in sys.argv[1:]:
	query=query+part+' '
query=query[:len(query)-1]
if query.strip()=="":
	print "Please write a query."
	exit()
br = mechanize.Browser()
br.set_handle_robots( False )
br.addheaders = [('User-agent', 'Firefox')]
try:
	br.open('http://mp3skull.cr')
except:
	print "Please check your internet connection. Or else, try again later."
	exit()
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
if maindivs==[]:
	print "Please enter valid queries."
	exit()
for maindiv in maindivs:
	songDetails = {'songTitle':"",'bitrate':0,'songLength':0,'filesize':0.0}
	songDetails['songTitle'] = maindiv.find('b').getText()
	for div in maindiv.select('div'):
		if 'class' in div.attrs and div.attrs['class'][0]=='left':
			#print div.getText().strip()
			informationFormat = re.compile(r'(\d+) kbps(\d+):(\d\d)(\d+)\.(\d+) mb')
			data = informationFormat.search(div.getText().strip())
			try:
				songDetails['bitrate']=int(data.group(1))
				songDetails['songLength']=int(data.group(2))*60+int(data.group(3))
				songDetails['filesize']=float(data.group(4))+(float(data.group(5))/100)
			except:
				pass
			break
	isValid = checkInvalid(songDetails,True,True)
	if isValid==True:
		links=maindiv.find_all('a')
		hyperlink = links[0].get('href').encode('ascii','ignore')
		wget = os.system("wget \""+hyperlink+"\" -P ~/Music/")
		if wget==0:
			break




 