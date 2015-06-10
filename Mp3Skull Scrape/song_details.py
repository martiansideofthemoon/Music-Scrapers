import mechanize,re,bs4,sys

query=""
for part in sys.argv[1:]:
	query=query+part+' '
query=query[:len(query)-1]

br=mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Firefox')]
base_url='http://en.wikipedia.org'
songDetails = {'search_query':query}
br.open('https://en.wikipedia.org/wiki/Main_Page')
br.form=list(br.forms())[0]
br['search']=query
searchResults = br.submit()
article_finder = bs4.BeautifulSoup(searchResults.read())
required_ul=None
for ul in article_finder.select('ul'):
	if 'class' in ul.attrs:
		if ul.attrs['class'][0]=='mw-search-results':
			required_ul=ul
request=br.open(base_url+required_ul.find('li').find('a').attrs['href'])
required_page = bs4.BeautifulSoup(request.read())
info_table=None
for table in required_page.select('table'):
	if 'class' in table.attrs:
		if 'vevent' in table.attrs['class']:
			info_table=table
for tr in info_table.select('tr'):
	if tr.find('td')==None:
		print tr.text
		continue
	if tr.find('th')!=None:
		to_print=""
		if tr.find('td').find('ul')!=None:
			to_print=tr.find('th').text+" : " 
			for li in tr.find('td').find('ul').select('li'):
				to_print+=li.text+", "
			to_print=to_print[:len(to_print)-2]
		else:
			to_print=tr.find('th').text+" : "+tr.find('td').text
		print to_print
