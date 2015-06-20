import bs4,requests,re

def extractWikiBoxes(wikiurl=""):
	try:
		res = requests.get(wikiurl)
		wikipage = bs4.BeautifulSoup(res.text)
		info_tables=[]
		for table in wikipage.select('table'):
			if 'class' in table.attrs:
				if 'vevent' in table.attrs['class']:
					info_tables.append(table)
		if info_tables==[]:
			#print "No box found."
			return
		else:
			final_data_strings=[]
			final_data_list=[]
			data_string=""
			for table in info_tables:
				for tr in table.select('tr'):
					to_print=""
					for element in tr.text.splitlines(tr.text.count('\n')):
						if element == u'\n':
							continue
						to_print+=element.strip().strip('"')+","
					if to_print!="":
						data_string+=to_print[:-1]+"\n"
				for img in table.select('img'):
					img_url = img.attrs['src']
					http_format = re.compile(r'http://.+')
					if http_format.search(img_url)==None:
						img_url='http:'+img_url
				data_string+=img_url
				final_data_strings.append(data_string)
				final_data_list.append(data_string.splitlines(data_string.count('\n')))
			return final_data_list
	except:
		print "Something went wrong. Please check your internet connection."
		return
#print extractWikiBoxes('https://en.wikipedia.org/wiki/Burn_It_Down_(Linkin_Park_song)')
