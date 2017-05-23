# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 17:24:13 2017

@author: michael
"""

import pickle
import os
import pandas as pd

os.chdir(r"D:\Projects\UFOData")

data = pickle.load(open("reports.p", "rb"))

reports = pd.DataFrame(data).transpose()
reports.columns = [s.strip(' ').strip(':') for s in reports.columns]

#reports.to_csv("raw_data.csv")


#parse occurred
spl = "("
ent_str = "(Entered as :"
reports = reports.join(reports['Occurred '].str.split(spl, 1, expand=True).rename(columns={0:"Occurred", 1:"Entered As"}))
del reports['Occurred ']
reports["Entered As"] = reports["Entered As"].str.strip(ent_str).str.strip("\)")



#parse location
reports = reports.join(reports['Location'].str.split(",", 1, expand=True).rename(columns={0:"City", 1:"State"}))
del reports['Location']
reports["State"] = reports["State"].str.strip(" ").str.upper()
#list of states not in abbrevs
abbrevs = list(pd.read_csv("state_abbrevs.csv")["Abbreviation"])
reports[~reports["State"].isin(abbrevs)]