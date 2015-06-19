#!/usr/bin/python
import mechanize,re,bs4,sys,requests,wikibox

def get_song_details(query=""):
	br=mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent','Firefox')]
	base_url='http://en.wikipedia.org'
	songDetails = {'Title':"",'Artist':"",'Album':"",'Year':"",'Artwork':""}
	try:
		br.open('https://en.wikipedia.org/wiki/Main_Page')
	except:
		print "Please check your internet connection"
		exit()
	br.form=list(br.forms())[0]
	br['search']=query
	searchResults = br.submit()
	#######################################################
	#TODO :- If article duplicates exist, choose best match
	#######################################################
	article_finder = bs4.BeautifulSoup(searchResults.read())
	URL=""
	if article_finder.find('h1').text.strip()=='Search results':
		required_ul=None
		for ul in article_finder.select('ul'):
			if 'class' in ul.attrs:
				if ul.attrs['class'][0]=='mw-search-results':
					required_ul=ul
		URL=base_url+required_ul.find('li').find('a').attrs['href']
	else:
		URL=searchResults.geturl()
	try:
		final_data_list=wikibox.extractWikiBoxes(URL)[0]
	except:
		print "No boxes found."
		exit()
	if final_data_list==None:
		print "Please give appropriate input."
		exit()
	songDetails['Title']=final_data_list[0][:-1]
	songDetails['Artist']=final_data_list[1][final_data_list[1].find('by')+3:-1]
	songDetails['Album']=final_data_list[2][final_data_list[2].find('album')+6:-1]
	songDetails['Artwork']=final_data_list[-1]
	dateRE=re.compile(r'Released,.+(\d\d\d\d)')
	for test in final_data_list:
		result = dateRE.search(test)
		if result!=None:
			songDetails['Year']=result.group(1)
	return songDetails;
	
"""
query=""
for part in sys.argv[1:]:
	query=query+part+' '
query=query[:len(query)-1]
if query.strip()=="":
	print "Please write a query."
	exit()
songDetails = get_song_details(query);
for item in songDetails.items():
		item[0].strip()
		item[1].strip()
		print item[0] + " : " + item[1]
"""
