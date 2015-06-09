import mechanize,bs4,os,sys
query=""
i=0
for part in sys.argv[1:]:
	query=query+part+' '
query=query[:len(query)-1]
br = mechanize.Browser()
br.set_handle_robots( False )
br.addheaders = [('User-agent', 'Firefox')]
br.open('http://mp3skull.cr')
for form in br.forms():
	if form.attrs['id']=='f1':
		br.form = form
		break
br['q'] = query
response = br.submit()
finalpage = bs4.BeautifulSoup(response.read())
maindiv=None
for div in finalpage.select('div'):
	if 'class' in div.attrs and div.attrs['class'][0]=='show1':
		maindiv=div
		break
links=maindiv.find_all('a')
os.system("wget \""+links[0].get('href')+"\"")