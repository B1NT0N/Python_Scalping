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
my_url = "https://www.imdb.com/find?s=tt&q=13&ref_=nv_sr_sm"

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
ID=[]
id=[]
info=results.table.findAll("tr")
for x in range(len(info)):
    name.append(info[x].find("td",{"class":"result_text"}).text)
    other.append(info[x].find("td",{"class":"result_text"}).text.split())
    ID.append(info[x].find("td",{"class":"result_text"}).a["href"].split("/"))
    links.append("https://www.imdb.com"+info[x].find("td",{"class":"result_text"}).a["href"])

for x in range(len(ID)):
    id.append(ID[x][2])


date_filter=[]
year = []
for x in range(len(other)):
    for y in range(len(other[x])):
        if len(other[x][y]) == 6:
            date_filter.append(other[x][y].replace('(', '').replace(')', ''))
        elif other[x][y] == "development)":
            date_filter.append(other[x][y].replace('(', '').replace(')', ''))

for date in range(len(date_filter)):
    if date_filter[date].isnumeric() == True:
            year.append(date_filter[date])
    elif date_filter[date] == "development":
        year.append(date_filter[date])

f_result=[]
for x in range(len(name)):
    for y in range(len(year)):
        if name[x].find(year[y]) != -1:
            f_result.append(Entertainment(name[x],year[y],id[x],links[x]))
            break
        elif y == (len(year)-1):
            f_result.append(Entertainment(name[x],"-----",id[x],links[x]))
        else:
            pass
    print(f"Name:{f_result[x].name} | Year: {f_result[x].year} | ID: {f_result[x].id} | Link:{f_result[x].link}")

#print(id)
#print(yearn1)
#print(year)
#print(name)

#for i in range(len(data)):
#    print(f"Name:{data[i][0]} | Year:{data[i][1]}")
#.find("td",{"class":"result_text"})
#id=results.table.tr.td.a['href']






#https://warezcdn.net/listing.php?type=movies
#https://embed.warezcdn.net/filme/[id]
#https://www.imdb.com/find?q=[search]&s=tt&ref_=fn_al_tt_mr
#https://www.imdb.com/title/tt4154796/?ref_=tt_mv_close