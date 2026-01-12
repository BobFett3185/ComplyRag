# here we need to just collect a bunch of documents from the federal register website 

# then from there we can embed them and put in a vector db
# actually the federal register is not ideal for collecting documents

# we will use this website which is the CFR (code of federal regulations) which is where all the regulations are stored and updated
# https://www.ecfr.gov/current/title-12

import requests
import time 
import os

date = "2026-01-04"
title = "12"
#part = '1'
chapter = "1"

endpoint = f"https://www.ecfr.gov/api/versioner/v1/full/{date}/title-{title}.xml"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

#this block makes a request to the endpoint and makes the file for the chapter of the CFR 
r = requests.get(endpoint, params={ "chapter": chapter})

os.makedirs("CFR_Chapters", exist_ok=True) # make a folder if it doesn't exist

if r.status_code == 200: # if success then write the content to a file 
    filename = f"CFR_Chapters/title_12_{chapter}.xml"

    with open(filename, "wb") as f:
            f.write(r.content)


'''
dont need to do this it somehow gives the whole title if you ask for a chapter




chapters = ["2","3","4","6","7","8","10","11","12","13","14","15","16","17","18"]

for chapterNumber in chapters:
    r = requests.get(endpoint, params={ "chapter": chapterNumber}, headers=headers)
    if r.status_code == 200: # if success
        filename = f"CFR_Chapters/title_12_chapter_{chapterNumber}.xml"

        with open(filename, "wb") as f:
                f.write(r.content)
    time.sleep(5) # sleep for 5 seconds to avoid rate limits

'''



'''
xml_content = r.content
print(r.status_code)
# 200 is a success
print(xml_content)#[:500])

'''