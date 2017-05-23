# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 19:04:03 2017

@author: michael
"""

import pickle
import os
import csv
import requests
import time
from bs4 import BeautifulSoup


base = "http://www.nuforc.org/webreports/"

headers = requests.utils.default_headers()
headers.update(
    {
        'From': 'mdrdatalab@gmail.com'    
    }
)

os.chdir(r"D:\Projects\UFOData")

temp = []
with open("all_links.csv", 'r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        temp.append(row)

all_links = [report for reports in temp for report in reports ]
all_reports = pickle.load(open("reports.p", "rb"))
temp = []
for report in all_reports.keys():
    temp.append(report+".html")
remaining = list(set(all_links)-set(temp))

err = []

def get_reports(number):
    a = time.time()
    for x in range(number+1):
        print(str(x)+"/"+str(number))
        report = remaining[x]
        try:
            result = requests.get(base + report)
            soup = BeautifulSoup(result.content, 'html.parser')
            data = soup.find("tbody").text
            all_reports[report.split('.')[0]] = parse_report(data)
        except:
            err.append(report)
        if x % 10 == 0:
            pickle.dump(all_reports, open("reports.p", "wb"))
            print("saved")
        time.sleep(3)    
    pickle.dump(all_reports, open("reports.p", "wb"))
    print("finished")
    print("Elapsed: ",time.time() - a)
    

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