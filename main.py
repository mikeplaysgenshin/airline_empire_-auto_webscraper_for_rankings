from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import time
month=input("please input the month of the airline starting time in numbers")
day=input("please input the day of the airline starting time")
year=input("please input the year of the airline starting time")
timestr1 = datetime(month,day,year)
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
         if timetag:
        timestr = timetag.get_text(strip=True)
        # Format example: "Jan 15 2026"
        month=timestr[0:3]
        #convert month to number
        if month=="Jan":
            month="1"
        if month=="Feb":
            month="2"
        if month=="Mar":
            month="3"
        if month=="Apr":
            month="4"
        if month=="May":
            month="5"
        if month=="Jun":
            month="6"
        if month=="Jul":
            month="7"
        if month=="Aug":
            month="8"
        if month=="Sep":
            month="9"
        if month=="Oct":
            month="10"
        if month=="Nov":
            month="11"
        if month=="Dec":
            month="12"
        day=timestr[4:6]
        #remove the comma from the day
        tempstr=""
        for char in day:
            if char!=",":
                tempstr+=char
        day=tempstr
        #reverse the string to get the year at the end
        timestr = timestr[::-1]
        year=timestr[0:4]
        #reverse the year string back to normal
        year=year[::-1]
        #reverse the timestr back to normal for printing
        timestr=timestr[::-1]
        print(month+"/"+day+"/"+year)
        timestr2=datetime(int(year),int(month),int(day))
        print(month+"/"+day+"/"+year)
        diff = timestr2 - timestr1
        print("days since the game started:", diff.days+1)
    else:
        print("Could not find game timestr")
        continue
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
            file.write("days since the game started: " + str(diff.days+1) + "\n")
        if target_td:
            file.write("rank:" + target_td.get_text(strip=True) + "\n")
        
        # Filtering empty strings and logos to get meaningful data
        clean_info = [x for x in infolist if x]
        if len(clean_info) >= 8:
            labels = [
                "alliance", "destination number", "fleet number",
                "hub number", "daily flights", "daily paxs",
                "daily distance", "valuation"
            ]
            for label, value in zip(labels, clean_info):
                f.write(f"{label}: {value}\n")

        f.write("\n")

    print("Scraped info:", clean_info)
    print("Sleeping...\n")

    time.sleep(19.98 * 60)

    
