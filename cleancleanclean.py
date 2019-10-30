import csv
import os
import sys
import numpy as np
import pandas as pd
import random

#this is the data of one day, one hour
filename = 'temporary.csv'

#Filtering for date; 2018-02-09 and hour 5-6 PM
fields = ['LineNo', 'LUID', 'Date', 'Latitude', 'Longitude', 'Floor', 'BuildingID', 'Time']

#Array of dictionary having List of rows in csv file
data = []

with open(filename, 'r') as f:
    csv_f = csv.reader(f)
    fields = next(csv_f)
    mylist = list(csv_f)

for i in range(0, len(mylist)):
    row = mylist[i]
    timesplit = row[7].split(':')
    time = (int(timesplit[0]) * 60 * 60) + (int(timesplit[1]) * 60) + int(timesplit[2])
    row[7] = time
    data.append({fields[j]:row[j] for j in range(0,len(fields))})

print("Length of data = " ,len(data))

pddata = pd.DataFrame(data)
pddata = pddata.drop(columns = 'LineNo')
pdfiltered = pddata.drop_duplicates(subset=('LUID', 'BuildingID', 'Floor', 'Latitude', 'Longitude'), keep="first")
print("Lenth of filtered data = ", pdfiltered.shape[0])
print("Filtered non-duplicate data: ")
print(pdfiltered)