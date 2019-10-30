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

#print(data)
#data is in the following form
#{'LineNo ': '0', 'LUID': '1693c816aabec8cf188172bf3b81a9ea16ea8d8558d9db39243a95aa176273e3', 'Date': '2018-02-09', 'Latitude': '38.991715338701724', 'Longitude': '-76.94267575842309', 'Floor': '6', 'BuildingID': '96', 'Time': 61210}

print("Hello")
copyofdata = data
print(len(copyofdata))
indices =[]
#this is giving a single point for all points which have the same LUID, building and floor
oneclass_compactdata = []
same = 0
counter = 0
c = 0
i = 0
while(counter < (len(data))):
    while(data[c]['LUID'] == data[c+1]['LUID'] and data[c]['BuildingID'] == data[c+1]['BuildingID'] and data[c]['Floor'] == data[c+1]['Floor']):
        if(data[c]['Latitude'] == data[c+1]['Latitude'] and data[c]['Longitude'] == data[c+1]['Longitude']):
            same = same + 1
            indices.append(data[c]['LineNo'])
        c = c + 1
        if(c == (len(data)-1)):
            break
    oneclass_compactdata.append(data[counter])
    i = i + 1
    counter = c + 1
    c = counter

# for i in range(0, len(oneclass_compactdata)):
#     print(oneclass_compactdata[i])
print("Hi")
pddata = pd.DataFrame(copyofdata)
pdfiltered = pddata.drop_duplicates(subset=('LUID', 'BuildingID', 'Floor', 'Latitude', 'Longitude'), keep="first")


pddata['LineNo'] = pddata.LineNo.astype(int)
indexNames = pddata[pddata['LineNo'] == (int(indices[p]) for p in range(len(indices)))].index
print("wohoo")
print(len(indexNames))

pdfiltered = pddata.drop_duplicates(subset=('LUID', 'BuildingID', 'Floor', 'Latitude', 'Longitude'), keep="first")
# res = list(filter(lambda i: int(i['LineNo ']) == (indices[p] for p in range(len(indices))), data)) 
print(pdfiltered.shape[0])
print(pdfiltered)
# c = 0
# for i in range(0, len(copyofdata)):
#     if(copyofdata[i]['LineNo '] == indices[c]):
#         del copyofdata[i]
#         c = c + 1
print("len of indices")
print(len(indices))
print("Same")
print(same)
print("len of copyofdata")
print(len(copyofdata))
print("Number of rows")
print(len(data) - len(indices))

# #this is same as above but plus the time different than 2 min range
# oneclass_compactdata = []

# counter = 0
# c = 0
# i = 0
# flag = 0
# while(counter < (len(data))):
#     while(data[c]['LUID'] == data[c+1]['LUID'] and data[c]['BuildingID'] == data[c+1]['BuildingID'] and data[c]['Floor'] == data[c+1]['Floor']):
#         if(abs(data[c]['Time'] - data[c+1]['Time'])<300):
#             flag = 1
#         c = c + 1
#         if(c == (len(data)-1)):
#             if(flag):
#                 oneclass_compactdata.append(data[counter])
#                 flag = 0
#             break
#     if(flag):
#         oneclass_compactdata.append(data[counter])
#         flag = 0
#     i = i + 1
#     counter = c + 1
#     c = counter

# for i in range(0, len(oneclass_compactdata)):
#     print(oneclass_compactdata[i])

