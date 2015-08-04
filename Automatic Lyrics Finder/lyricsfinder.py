#!/usr/bin/python
import mechanize,sys,re,bs4,requests,time
def getlyrics(query=""):
    br = mechanize.Browser()
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    try:
        br.open('http://search.azlyrics.com/search.php?q='+query);
    except:
        return "Please check your internet connection."
    links=[]
    for l in br.links():
        for i in l.attrs:
        	if i[0]=='href':
        		desiredFormat = re.compile(r'http://www\.azlyrics\.com/lyrics.*');
        		output = desiredFormat.search(i[1])
        		if output!=None:
        			links.append(i[1]);             
    print links[0]
    response = br.open(links[0])
    #res = requests.get(links[0])
    """
    br.open('http://www.4everproxy.com')
    for form in br.forms():
        if 'id' in form.attrs and form.attrs['id']=='foreverproxy_url-form':
            br.form=form
            break
    br['u']=links[0]
    print str(br.form) + "," + br['u']
    response = br.submit()
    """
    finalpage = bs4.BeautifulSoup(response.read())
    for div in finalpage.select('div'):
        print div.text
    	if div.attrs=={} and len(div.text)>100:
    		return div.text
    
    

query=""
i=0
for part in sys.argv[1:]:
    query=query+part+'+'
query=query[:len(query)-1]
if query.strip()=="":
    print "Please write a query."
    exit()
print getlyrics(query)