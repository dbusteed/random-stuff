from bs4 import BeautifulSoup as bs
from requests import get

page = get("https://catalog.byu.edu/majors").text

ppage = bs(page, 'html.parser')

main_div = ppage.find(class_="view-content")

links = main_div.find_all('a')

majors = []

for l in links:
    majors.append(l.text)

for m in majors:
    print('{}'.format(m))