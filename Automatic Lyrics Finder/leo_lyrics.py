import mechanize,bs4,sys
query=""
i=0
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
    br.open('http://www.leoslyrics.com');
except:
    print "Please check your internet connection."
for form in br.forms():
	if 'id' in form.attrs and form.attrs['id']=='cse-search-box':
		br.form = form 
print br.form
br['q']=query
response = br.submit()
print response.read()