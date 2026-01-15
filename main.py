import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import time

infolist=[]
print("Please input your airline name")
airlinename=input()
print("Please input the url of the game rankings")
url=input()
print("Please input the daylength of the game in minutes")
daylength=input()
while True:
    with urllib.request.urlopen(url) as file:
        soup = BeautifulSoup(file, 'html.parser')
        timetag=soup.find("div", id="gametime")
        #print(soup.prettify())
    #htmlstring=soup.prettify()
    #with open("htmltext.txt", "w", encoding="utf-8") as file:
        #file.write(htmlstring)
    # Find the text "Dontis Airlines" and get its parent <td>
        text_node = soup.find(string=airlinename)
        if text_node:
            rankheader =     text_node.find_parent('td')
            print(f"Start tag: {rankheader}")
        
        # Traverse siblings to find the next <td> or <a> tags
            curr = rankheader
            while curr:
                curr = curr.next_sibling
                if curr and curr.name:
                    print(f"Checking tag: {curr.name}")
                    text =             curr.get_text(strip=True)
                    infolist.append(text)
                
                # Stop if we hit an 'a' tag (next player)
                    if curr.name == "a":
                        break
    
    
    # Find the 6th <td> before given airline name
    target_td = None
    if text_node:
        # Get all <td> elements in the same row
        parent_tr = text_node.find_parent('tr')
        if parent_tr:
            tds = parent_tr.find_all('td')
            # Find index of the <td> containing given airline name
            dontis_td = text_node.find_parent('td')
            try:
                idx = tds.index(dontis_td)
                # If there aren't enough TDs before, just take the first one available
                if idx > 0:
                    target_idx = max(0, idx - 6)
                    target_td = tds[target_idx]
                    print(f"Target <td> (index {target_idx}): {target_td.get_text(strip=True)}")
                else:
                    print(f"Genshin is already the first TD at index {idx}")
            except ValueError:
                pass

    with open("data.txt", "a", encoding="utf-8") as file:
        if timetag:
            file.write("Time: " + timetag.get_text(strip=True) + "\n")
        
        if target_td:
            file.write("rank:" + target_td.get_text(strip=True) + "\n")
        
        # Filtering empty strings and logos to get meaningful data
        clean_info = [x for x in infolist if x]
        print(clean_info)
        if len(clean_info) >= 3:
            file.write("alliance: " + clean_info[0] + "\n")
            file.write("destination number: " + clean_info[1] + "\n")
            file.write("fleet number: " + clean_info[2] + "\n")
            file.write("hub number: " + clean_info[3] + "\n")
            file.write("daily flights : " + clean_info[4] + "\n")
            file.write("daily paxs : " + clean_info[5] + "\n")
            file.write("daily distance : " + clean_info[6] + "\n")
            file.write("valuation : " + clean_info[7] + "\n")
            file.flush()
            file.close()
    infolist=[]
    cleandata=[]
    print("waiting for next day")
    time.sleep(int(daylength)*60)
    
