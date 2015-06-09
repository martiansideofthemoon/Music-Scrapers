import sys
from selenium import webdriver
query=""
i=0
for part in sys.argv[1:]:
	query=query+part+'+'
query=query[:len(query)-1]
browser = webdriver.Firefox()
browser.get('http://search.azlyrics.com/search.php?q='+query)
table = browser.find_element_by_class_name('table-condensed')
link = table.find_element_by_tag_name('a')
browser.get(link.get_attribute('href'))
container = browser.find_element_by_class_name('col-lg-8')
container = container.find_elements_by_tag_name('div')
print container[9].text
browser.quit()

