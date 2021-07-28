from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

class Entertainment:

    def __init__(self,name,year,id,link,watch_link):
        self.name = name
        self.year = year
        self.id = id
        self.link = link
        self.watch_link = watch_link

chc = input("Chose Series/Animes or Movies (S/M)")
if chc.upper() == "M":
    srh = input("Input Movie name: ").replace(" ","%20").lower()
    my_url = f"https://www.imdb.com/find?q={srh}&s=tt&ttype=ft&ref_=fn_ft"
elif chc.upper() == "S":
    srh = input("Input Serie name: ").replace(" ","%20").lower()
    my_url = f"https://www.imdb.com/find?q={srh}&s=tt&ttype=tv&ref_=fn_tv"

uClient = uRequest(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div",{ "class":"findSection"})
results=[]
for x in range(len(containers)):
    header=containers[x].h3
    if header.text.strip() == "Titles":
        results=containers[x]
if len(results) == 0:
    print("No Results Found")
else:
    name=[]
    full_name=[]
    links=[]
    other=[]
    ID=[]
    id=[]

    info=results.table.findAll("tr")

    for x in range(len(info)):
        name.append(info[x].find("td",{"class":"result_text"}).a.text)
        full_name.append(info[x].find("td",{"class":"result_text"}).text)
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
    watch_link=[]

    for w_link in range(len(ID)):
        if chc.upper() == "M":
            watch_link.append(f"https://embed.warezcdn.net/filme/{id[w_link]}")
        elif chc.upper() == "S":
            watch_link.append(f"https://embed.warezcdn.net/serie/{id[w_link]}")
        
    f_result=[]
    for x in range(len(name)):
        for y in range(len(year)):
            if full_name[x].find(year[y]) != -1:
                f_result.append(Entertainment(name[x],year[y],id[x],links[x],watch_link[x]))
                break
            elif y == (len(year)-1):
                f_result.append(Entertainment(name[x],"-----",id[x],links[x],watch_link[x]))
            else:
                pass
        
    if len(f_result)>5:
        for x in range(5):
            print(f"Name:{f_result[x].name} | Year: {f_result[x].year} | ID: {f_result[x].id} | Link:{f_result[x].link} | Watch Link:{f_result[x].watch_link}")
    else:
        for x in range(len(f_result)):
            print(f"Name:{f_result[x].name} | Year: {f_result[x].year} | ID: {f_result[x].id} | Link:{f_result[x].link} | Watch Link:{f_result[x].watch_link}")

#Coments to do later