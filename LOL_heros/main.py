# -*- coding: utf-8 -*-
# import urlretrieve
from bs4 import BeautifulSoup
import json
import urllib2
import urllib
import re
import requests
from lxml import html
import sys
import os
import pymysql

def readhtmlfile():
    html = ''
    while True:
        try: 
            tmp = raw_input() 
        except: 
            break
        html += tmp + '\n'
    return html

if __name__ == "__main__":
    content = readhtmlfile()
    soup = BeautifulSoup(content, "html.parser", from_encoding="gbk")
    img = soup("img")
    p = soup("p")
    a = soup("a")
    print(""+img[0]["alt"])
    for i in range(len(img)):
        print("{")
        print("\"id\": "+str(i)+",")
        print("\"title\": \""+img[i]["alt"].split(" ")[0]+"\",")
        print("\"name\": \""+img[i]["alt"].split(" ")[1]+"\",")
        print("\"picture\": \""+img[i]["src"]+"\",")
        print("\"count\": 0")
        print("},")