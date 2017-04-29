# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 17:24:13 2017

@author: michael
"""

import pickle
import csv
import os
import pandas as pd

os.chdir(r"D:\Projects\UFOData")

data = pickle.load(open("reports.p", "rb"))

reports = pd.DataFrame(data).transpose()
reports.columns = [s.strip(' ').strip(':') for s in reports.columns]

reports.to_csv("raw_data.csv")


