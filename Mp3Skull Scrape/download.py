#!/usr/bin/python
import mechanize,bs4,os,sys,re,getopt,eyed3,song_details
from os.path import expanduser

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

def putDetails(fileName="",fileLocation="/",songDetails=[],imageName=""):
	print songDetails
	audioFile = eyed3.Mp3AudioFile(fileLocation+fileName)
	tag = audioFile.getTag()
	tag.setArtist(songDetails['Artist'])
	tag.setAlbum(songDetails['Album'])
	tag.setTitle(songDetails['Title'])

	#tag.addImage(0x08,fileLocation+imageName)
	tag.update()
	os.system("eyed3 -Y "+songDetails['Year']+" --add-image=/"+fileLocation+"\""+imageName+"\":FRONT_COVER "+fileLocation+"\""+fileName+"\"")
	#os.system("rm \""+fileLocation+imageName+"\"")
	return
try:
	opts,args = getopt.getopt(sys.argv[1:],'rcs',['remix','cover','short'])
except:
	usage()
	exit()
query=""
for part in args:
	query=query+part+' '
query=query[:len(query)-1]
if query.strip()=="":
	print "Please write a query."
	exit()
checkCover=True
checkRemix=True
checkLength=True
for opt,arg in opts:
	if opt in ['-r','--remix']:
		checkRemix=False
		query=query+' remix'
	elif opt in ['-c','--cover']:
		checkCover=False
		query=query+' cover'
	elif opt in ['-s','short']:
		checkLength=False

br = mechanize.Browser()
br.set_handle_robots( False )
br.addheaders = [('User-agent', 'Firefox')]
#try:
br.open('http://mp3skull.is')
#except:
#	print "Please check your internet connection. Or else, try again later."
#	exit()
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
	print "Please enter valid queries / No results found."
	exit()
downloadOccured=False
fileName=""
fileLocation=expanduser('~')+'/Music/'
for maindiv in maindivs:
	isValid=True
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
				isValid=False
			break
	if isValid==True:
		isValid = checkInvalid(songDetails,checkCover,checkRemix,checkLength)
	if isValid==True:
		links=maindiv.find_all('a')
		hyperlink = links[0].get('href').encode('ascii','ignore')
		wget = os.system("wget \""+hyperlink+"\" -P "+fileLocation)
		if wget==0:
			downloadOccured=True
			fileRegex = re.compile(r'/([^/]+)$')
			fileName = fileRegex.search(hyperlink).group(1)
			break
if downloadOccured==False:
	print "No file matched criteria. Please change some flags."
	exit()
songDetails = song_details.get_song_details(query)
wget = os.system("wget \""+songDetails['Artwork']+"\" -P "+fileLocation)
imageName=""
if wget==0:
	fileRegex = re.compile(r'/([^/]+)$')
	imageName = fileRegex.search(hyperlink).group(1)
print fileName
putDetails(fileName,fileLocation,songDetails,imageName)




 