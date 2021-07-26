from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

uClient = uRequest("https://www.imdb.com/title/tt1560954/?ref_=fn_ft_tt_1")
page_html_link = uClient.read()
uClient.close()

page_soup_link = soup(page_html_link, "html.parser")


containers_link1 = page_soup_link.findAll("div",{ "class":"TitleBlock__Container-sc-1nlhx7j-0 hglRHk"})

for container in containers_link1:  
    containers_link2=containers_link1[container].findAll("div",{ "class":"TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt"})
    containers_link3=containers_link2.findAll("div",{ "class":"TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"})

print(containers_link1)