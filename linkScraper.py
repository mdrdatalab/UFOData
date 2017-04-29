# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 13:18:49 2017

@author: michael
"""

import requests
import csv
import time
from bs4 import BeautifulSoup


base = "http://www.nuforc.org/webreports/"
root = base + "ndxevent.html"

headers = requests.utils.default_headers()
headers.update(
    {
        'From': 'mdrdatalab@gmail.com'    
    }
)

#get links of monthly reports
result = requests.get(root)

soup = BeautifulSoup(result.content, 'html.parser')
links = soup.find_all("a")
monthly = []

for x in links:
    monthly.append(x.attrs['href'])

monthly.pop(0)
with open("month_links.csv", 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(monthly)
    


all_reports = []
n = 0
#get links for individual reports
for month in monthly:
    n+=1
    print(month, str(n)+"/"+str(len(monthly)))
    reports = []
    result = requests.get(base + month)
    soup = BeautifulSoup(result.content, 'html.parser')
    links = soup.find_all("a")
    links.pop(0)
    for x in links:
        reports.append(x.attrs['href'])
    with open("all_links.csv", 'a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(reports)
    all_reports.append(reports)
    time.sleep(2)
#
    



#scrape individual reports
data = []
for report in all_reports:
    print(report)
    result = requests.get(base + report)
    soup = BeautifulSoup(result.content, 'html.parser')
    x = soup.find("tbody").text
    data.append([report.split('.')[0], x])
    time.sleep(2)
    
    
    
#parse reports
def parse_report(report):
    
    #split at each
    splits = ["Reported:","Posted:","Location:","Shape:",
          "Duration:","\n\n\n"]
    
    record = {}
    temp = report.partition("Occurred :")[2]
    curkey = "Occurred :"
    for spl in splits:
        temp = temp.partition(spl)
        record[curkey] = temp[0]
        curkey = temp[1]
        temp = temp[2]
    record["Report:"] = temp
    return record
    
reports = {}
for report in data:
    reports[report[0]] = parse_report(report[1])
    
    
    