from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

#srh=input("Search:")
#srh=srh.replace(" ","+")
srh = "fast+and+furious"
my_url = f"https://www.imdb.com/find?q={srh}&ref_=nv_sr_sm"

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
name=[]
data=[[]]
other=[]
info=results.table.findAll("tr")
for x in range(len(info)):
    name.append(info[x].find("td",{"class":"result_text"}).a.text)
    other.append(info[x].find("td",{"class":"result_text"}).text.strip())

#print(name)
print(other)
#for i in range(len(data)):
#    print(f"Name:{data[i][0]} | Year:{data[i][1]}")
#.find("td",{"class":"result_text"})
#id=results.table.tr.td.a['href']






#https://warezcdn.net/listing.php?type=movies
#https://embed.warezcdn.net/filme/[id]
#https://www.imdb.com/find?q=[search]&s=tt&ref_=fn_al_tt_mr
#https://www.imdb.com/title/tt4154796/?ref_=tt_mv_close