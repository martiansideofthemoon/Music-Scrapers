import mechanize,sys,re,bs4,requests
query=""
i=0
for part in sys.argv[1:]:
	query=query+part+'+'
query=query[:len(query)-1]
br = mechanize.Browser()
br.set_handle_robots( False )
br.addheaders = [('User-agent', 'Firefox')]
try:
    br.open('http://search.azlyrics.com/search.php?q='+query);
    links=[]
    for l in br.links():
        for i in l.attrs:
        	if i[0]=='href':
        		desiredFormat = re.compile(r'http://www\.azlyrics\.com/lyrics.*');
        		output = desiredFormat.search(i[1])
        		if output!=None:
        			links.append(i[1]);
    try:                
        #print links[0]
        res = requests.get(links[0])
        finalpage = bs4.BeautifulSoup(res.text)
        for div in finalpage.select('div'):
        	if div.attrs=={}:
        		print div.text
    except:
        print "Lyrics not found. Please check your input."
except:
    print "Please check your internet connection."