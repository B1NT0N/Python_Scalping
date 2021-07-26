from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

class Entertainment:

    def __init__(self,name,year,id,link):
        self.name = name
        self.year = year
        self.id = id
        self.link = link

#srh=input("Search:")
#srh=srh.replace(" ","+")
srh = "gun"
my_url = "https://www.imdb.com/find?q=assasin&s=tt&ttype=ft&ref_=fn_ft"

uClient = uRequest(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div",{ "class":"findSection"})

for x in range(len(containers)):
    header=containers[x].h3
    if header.text.strip() == "Titles":
        results=containers[x]

#info=results.table.tr.find("td",{"class":"result_text"})
#print(info.text.strip().split()[1])
#name
name=[]
links=[]
other=[]
info=results.table.findAll("tr")
for x in range(len(info)):
    name.append(info[x].find("td",{"class":"result_text"}).a.text)
    other.append(info[x].find("td",{"class":"result_text"}).text.split())
    links.append("https://www.imdb.com"+info[1].find("td",{"class":"result_text"}).a["href"])

#for link in links:
    uClient = uRequest("https://www.imdb.com/title/tt1560954/?ref_=fn_ft_tt_1")
    page_html_link = uClient.read()
    uClient.close()

    page_soup_link = soup(page_html_link, "html.parser")

    containers_link = page_soup.findAll("div",{ "class":"TitleBlock__Container"})

f_result=[]
#for x in range(len(other)):
#    f_result.append(Entertainment(name[x],year[x],"-----",links[x]))
#    print(f"Name:{f_result[x].name} | Year:{f_result[x].year} | ID:{f_result[x].id}")

#print(yearr)
#print(yearn1)
#print(yearn2)
print(containers_link)

#for i in range(len(data)):
#    print(f"Name:{data[i][0]} | Year:{data[i][1]}")
#.find("td",{"class":"result_text"})
#id=results.table.tr.td.a['href']






#https://warezcdn.net/listing.php?type=movies
#https://embed.warezcdn.net/filme/[id]
#https://www.imdb.com/find?q=[search]&s=tt&ref_=fn_al_tt_mr
#https://www.imdb.com/title/tt4154796/?ref_=tt_mv_close